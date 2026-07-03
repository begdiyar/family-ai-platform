from datetime import timedelta, date
from django.utils import timezone
from django.db.models import Count, Avg, Q, FloatField, F, Max, ExpressionWrapper
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth, Coalesce
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers

from apps.users.models import User
from apps.couples.models import Couple
from apps.diagnostics.models import DiagnosticSession
from apps.analytics.models import AnalyticsResult, ZoneScore
from apps.practices.models import DailyAssignment, AssignmentSlot, COMPLETABLE_SLOTS
from apps.ai_consultant.models import AIMessage
from .permissions import IsAdminUser


def get_date_range(period='month', count=12):
    today = timezone.now().date()
    if period == 'day':
        return today - timedelta(days=count), today
    if period == 'week':
        return today - timedelta(weeks=count), today
    return today - timedelta(days=count * 30), today


class AdminOverviewView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        now = timezone.now()
        month_ago = now - timedelta(days=30)

        total_users = User.objects.count()
        total_couples = Couple.objects.filter(status='active').count()

        active_couple_ids = (
            DiagnosticSession.objects.filter(created_at__gte=month_ago)
            .values_list('couple_id', flat=True)
            .union(
                DailyAssignment.objects.filter(created_at__gte=month_ago)
                .values_list('couple_id', flat=True)
            )
        )
        active_families = Couple.objects.filter(id__in=active_couple_ids).count()

        completed_diagnostics = DiagnosticSession.objects.filter(status='completed').count()
        completed_practices = AssignmentSlot.objects.filter(
            completed=True, slot_type__in=COMPLETABLE_SLOTS,
        ).count()
        ai_messages = AIMessage.objects.filter(role='user').count()

        avg_score = AnalyticsResult.objects.aggregate(
            avg=Avg('overall_score')
        )['avg']

        new_users_month = User.objects.filter(created_at__gte=month_ago).count()

        # Crisis breakdown
        crisis_counts = dict(
            AnalyticsResult.objects
            .filter(couple__isnull=False)
            .values('crisis_level')
            .annotate(count=Count('id'))
            .values_list('crisis_level', 'count')
        )

        return Response({
            'total_users': total_users,
            'total_couples': total_couples,
            'active_families_30d': active_families,
            'completed_diagnostics': completed_diagnostics,
            'completed_practices': completed_practices,
            'ai_messages': ai_messages,
            'avg_relationship_score': round(float(avg_score), 1) if avg_score else None,
            'new_users_month': new_users_month,
            'crisis_breakdown': {
                'none': crisis_counts.get('none', 0),
                'warning': crisis_counts.get('warning', 0),
                'critical': crisis_counts.get('critical', 0),
            },
        })


class AdminRegistrationsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        period = request.query_params.get('period', 'day')
        count = int(request.query_params.get('count', 30))
        date_from, date_to = get_date_range(period, count)

        trunc_fn = {'day': TruncDay, 'week': TruncWeek, 'month': TruncMonth}.get(period, TruncDay)

        data = (
            User.objects
            .filter(created_at__date__gte=date_from, created_at__date__lte=date_to)
            .annotate(period=trunc_fn('created_at'))
            .values('period')
            .annotate(count=Count('id'))
            .order_by('period')
        )

        return Response([
            {'date': item['period'].date().isoformat(), 'count': item['count']}
            for item in data
        ])


class AdminActivityView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        period = request.query_params.get('period', 'day')
        count = int(request.query_params.get('count', 30))
        date_from, date_to = get_date_range(period, count)

        trunc_fn = {'day': TruncDay, 'week': TruncWeek, 'month': TruncMonth}.get(period, TruncDay)

        diagnostics = (
            DiagnosticSession.objects
            .filter(status='completed', created_at__date__gte=date_from)
            .annotate(period=trunc_fn('created_at'))
            .values('period')
            .annotate(count=Count('id'))
            .order_by('period')
        )

        practices = (
            DailyAssignment.objects
            .filter(
                date__gte=date_from,
                slots__completed=True,
                slots__slot_type__in=COMPLETABLE_SLOTS,
            )
            .values('date')
            .annotate(count=Count('id', distinct=True))
            .order_by('date')
        )

        # Merge by date
        diag_map = {item['period'].date().isoformat(): item['count'] for item in diagnostics}
        prac_map = {item['date'].isoformat(): item['count'] for item in practices}
        all_dates = sorted(set(list(diag_map.keys()) + list(prac_map.keys())))

        return Response([
            {
                'date': d,
                'diagnostics': diag_map.get(d, 0),
                'practices': prac_map.get(d, 0),
            }
            for d in all_dates
        ])


class AdminFamiliesView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 20))
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        min_score = request.query_params.get('min_score')
        max_score = request.query_params.get('max_score')
        active_only = request.query_params.get('active') == 'true'
        search = request.query_params.get('search', '').strip()

        qs = Couple.objects.filter(status='active').select_related('partner_a', 'partner_b')

        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)
        if search:
            qs = qs.filter(
                Q(partner_a__first_name__icontains=search) |
                Q(partner_b__first_name__icontains=search) |
                Q(partner_a__email__icontains=search) |
                Q(partner_b__email__icontains=search)
            )

        # Annotate with stats
        month_ago = timezone.now() - timedelta(days=30)
        qs = qs.annotate(
            diagnostics_count=Count('analytics_results', distinct=True),
            practices_count=Count('daily_assignments', distinct=True),
        )

        # Filter by score range
        if min_score or max_score:
            couple_ids_with_score = (
                AnalyticsResult.objects
                .values('couple_id')
                .annotate(latest_score=Avg('overall_score'))
            )
            if min_score:
                couple_ids_with_score = couple_ids_with_score.filter(latest_score__gte=float(min_score))
            if max_score:
                couple_ids_with_score = couple_ids_with_score.filter(latest_score__lte=float(max_score))
            ids = [r['couple_id'] for r in couple_ids_with_score]
            qs = qs.filter(id__in=ids)

        # Active filter
        if active_only:
            active_ids = (
                DiagnosticSession.objects.filter(created_at__gte=month_ago)
                .values_list('couple_id', flat=True)
            )
            qs = qs.filter(id__in=active_ids)

        total = qs.count()
        offset = (page - 1) * page_size
        couples = qs.order_by('-created_at')[offset:offset + page_size]

        # Get latest scores — database-agnostic (first seen per couple after desc sort)
        couple_ids = [c.id for c in couples]
        latest_scores = {}
        if couple_ids:
            for r in (
                AnalyticsResult.objects
                .filter(couple_id__in=couple_ids)
                .order_by('couple_id', '-created_at')
                .values('couple_id', 'overall_score', 'crisis_level')
            ):
                cid = str(r['couple_id'])
                if cid not in latest_scores:
                    latest_scores[cid] = r

        # Last activity
        last_activity = {}
        if couple_ids:
            for r in (
                DiagnosticSession.objects
                .filter(couple_id__in=couple_ids)
                .values('couple_id')
                .annotate(last=Max('created_at'))
            ):
                last_activity[str(r['couple_id'])] = r['last']

        # Pre-compute active couples in one query (avoid N+1)
        active_couple_ids_set = set(
            str(i) for i in DiagnosticSession.objects
            .filter(couple_id__in=couple_ids, created_at__gte=month_ago)
            .values_list('couple_id', flat=True)
            .distinct()
        )

        results = []
        for c in couples:
            cid = str(c.id)
            score_data = latest_scores.get(cid, {})
            score = score_data.get('overall_score')
            results.append({
                'id': cid,
                'partner_a': c.partner_a.first_name if c.partner_a else '',
                'partner_b': c.partner_b.first_name if c.partner_b else '',
                'created_at': c.created_at.date().isoformat(),
                'diagnostics_count': c.diagnostics_count,
                'practices_count': c.practices_count,
                'relationship_score': round(float(score), 1) if score else None,
                'crisis_level': score_data.get('crisis_level', 'none'),
                'last_activity': last_activity.get(cid),
                'is_active': cid in active_couple_ids_set,
            })

        return Response({
            'count': total,
            'page': page,
            'page_size': page_size,
            'total_pages': (total + page_size - 1) // page_size,
            'results': results,
        })


class AdminFamilyDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, couple_id):
        try:
            couple = Couple.objects.select_related('partner_a', 'partner_b').get(id=couple_id)
        except Couple.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)

        month_ago = timezone.now() - timedelta(days=30)

        # Analytics history
        results = (
            AnalyticsResult.objects
            .filter(couple=couple)
            .prefetch_related('zone_scores')
            .order_by('created_at')
        )

        analytics_history = []
        for r in results:
            zone_data = {}
            scores = list(r.zone_scores.all())
            for zone in ['communication', 'trust', 'intimacy', 'conflict', 'values', 'future']:
                zone_scores = [s for s in scores if s.zone == zone]
                if zone_scores:
                    avg_pct = sum(s.percent for s in zone_scores) / len(zone_scores)
                    zone_data[zone] = round(avg_pct, 1)
                else:
                    zone_data[zone] = None
            analytics_history.append({
                'date': r.created_at.date().isoformat(),
                'overall_score': round(float(r.overall_score), 1) if r.overall_score else None,
                'crisis_level': r.crisis_level,
                'zones': zone_data,
            })

        diagnostics_count = DiagnosticSession.objects.filter(couple=couple, status='completed').count()
        practices_count = AssignmentSlot.objects.filter(
            assignment__couple=couple,
            completed=True,
            slot_type__in=COMPLETABLE_SLOTS,
        ).count()

        last_session = (
            DiagnosticSession.objects.filter(couple=couple).order_by('-created_at').first()
        )

        latest = results.last()

        return Response({
            'id': str(couple.id),
            'partner_a': {
                'id': str(couple.partner_a.id),
                'name': couple.partner_a.first_name,
                'email': couple.partner_a.email,
            },
            'partner_b': {
                'id': str(couple.partner_b.id),
                'name': couple.partner_b.first_name,
                'email': couple.partner_b.email,
            } if couple.partner_b else None,
            'created_at': couple.created_at.date().isoformat(),
            'marriage_year': couple.marriage_year,
            'has_children': couple.has_children,
            'children_count': couple.children_count,
            'diagnostics_count': diagnostics_count,
            'practices_count': practices_count,
            'last_activity': last_session.created_at.isoformat() if last_session else None,
            'latest_score': round(float(latest.overall_score), 1) if latest and latest.overall_score else None,
            'latest_crisis': latest.crisis_level if latest else 'none',
            'analytics_history': analytics_history,
        })


class AdminProblemsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        # Latest result per couple — database-agnostic
        latest_by_couple = {}
        for r in (
            AnalyticsResult.objects
            .filter(couple__isnull=False)
            .order_by('couple_id', '-created_at')
            .values('id', 'couple_id')
        ):
            cid = r['couple_id']
            if cid not in latest_by_couple:
                latest_by_couple[cid] = r['id']

        latest_result_ids = list(latest_by_couple.values())
        total = len(latest_result_ids)
        if total == 0:
            return Response({
                'total_families': 0,
                'zones': [],
                'crisis': {'none': 0, 'warning': 0, 'critical': 0},
            })

        # Zone averages from latest results
        _pct_expr = ExpressionWrapper(
            F('score') * 100.0 / F('max_score'),
            output_field=FloatField(),
        )
        zone_stats = (
            ZoneScore.objects
            .filter(result_id__in=latest_result_ids)
            .values('zone')
            .annotate(avg_percent=Avg(_pct_expr))
            .order_by('zone')
        )

        # Crisis distribution
        crisis = dict(
            AnalyticsResult.objects
            .filter(id__in=latest_result_ids)
            .values('crisis_level')
            .annotate(count=Count('id'))
            .values_list('crisis_level', 'count')
        )

        # Low-score families per zone (below 50%)
        zone_problems = []
        for item in zone_stats:
            low_count = (
                ZoneScore.objects
                .filter(result_id__in=latest_result_ids, zone=item['zone'])
                .annotate(pct=ExpressionWrapper(
                    F('score') * 100.0 / F('max_score'),
                    output_field=FloatField(),
                ))
                .filter(pct__lt=50)
                .values('result_id')
                .distinct()
                .count()
            )
            zone_problems.append({
                'zone': item['zone'],
                'avg_percent': round(float(item['avg_percent']), 1),
                'low_count': low_count,
                'low_percent': round(low_count / total * 100, 1) if total else 0,
            })

        return Response({
            'total_families': total,
            'zones': zone_problems,
            'crisis': {
                'none': crisis.get('none', 0),
                'warning': crisis.get('warning', 0),
                'critical': crisis.get('critical', 0),
            },
        })


class AdminTrendsView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        period = request.query_params.get('period', 'day')
        count = int(request.query_params.get('count', 30))
        date_from, _ = get_date_range(period, count)
        trunc_fn = {'day': TruncDay, 'week': TruncWeek, 'month': TruncMonth}.get(period, TruncDay)

        # Average relationship score trend over time
        score_trend = (
            AnalyticsResult.objects
            .filter(created_at__date__gte=date_from)
            .annotate(period=trunc_fn('created_at'))
            .values('period')
            .annotate(avg_score=Avg('overall_score'))
            .order_by('period')
        )

        # Score distribution — latest result per couple
        latest: dict = {}
        for r in (
            AnalyticsResult.objects
            .filter(couple__isnull=False)
            .order_by('couple_id', '-created_at')
            .values('couple_id', 'overall_score')
        ):
            if r['couple_id'] not in latest:
                latest[r['couple_id']] = r['overall_score']

        dist = {'0–25': 0, '25–50': 0, '50–75': 0, '75–100': 0}
        for score in latest.values():
            if score is None:
                continue
            s = float(score)
            if s < 25:
                dist['0–25'] += 1
            elif s < 50:
                dist['25–50'] += 1
            elif s < 75:
                dist['50–75'] += 1
            else:
                dist['75–100'] += 1

        return Response({
            'score_trend': [
                {
                    'date': item['period'].date().isoformat(),
                    'avg_score': round(float(item['avg_score']), 1),
                }
                for item in score_trend
            ],
            'score_distribution': [
                {'range': k, 'count': v, 'color': c}
                for (k, v), c in zip(
                    dist.items(),
                    ['#843048', '#886028', '#385C8A', '#386858'],
                )
            ],
        })


class AdminExportView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        from apps.diagnostics.models import DiagnosticSession, LEVEL_NUMBERS

        couples = (
            Couple.objects
            .filter(status='active')
            .select_related('partner_a', 'partner_b')
            .order_by('-created_at')
        )
        couple_ids = [c.id for c in couples]

        # Latest analytics result per couple
        latest_scores: dict = {}
        for r in (
            AnalyticsResult.objects
            .filter(couple_id__in=couple_ids)
            .order_by('couple_id', '-created_at')
            .values('couple_id', 'overall_score', 'crisis_level')
        ):
            cid = r['couple_id']
            if cid not in latest_scores:
                latest_scores[cid] = r

        # Completed diagnostics per couple per level
        diag_raw = (
            DiagnosticSession.objects
            .filter(couple_id__in=couple_ids, status='completed')
            .values('couple_id', 'level_number')
            .annotate(count=Count('id'))
        )
        diag_map: dict = {}
        for row in diag_raw:
            cid = row['couple_id']
            if cid not in diag_map:
                diag_map[cid] = {}
            diag_map[cid][row['level_number']] = row['count']

        # Completed practices per couple
        prac_raw = (
            AssignmentSlot.objects
            .filter(
                assignment__couple_id__in=couple_ids,
                completed=True,
                slot_type__in=COMPLETABLE_SLOTS,
            )
            .values('assignment__couple_id')
            .annotate(count=Count('id'))
        )
        prac_map = {r['assignment__couple_id']: r['count'] for r in prac_raw}

        # Crisis summary
        crisis_counts = {'none': 0, 'warning': 0, 'critical': 0}
        for v in latest_scores.values():
            cl = v.get('crisis_level', 'none')
            crisis_counts[cl] = crisis_counts.get(cl, 0) + 1

        results = []
        for c in couples:
            cid = c.id
            score_data = latest_scores.get(cid, {})
            score = score_data.get('overall_score')
            level_diag = diag_map.get(cid, {})
            results.append({
                'id': str(cid),
                # Partner A
                'a_first_name': c.partner_a.first_name if c.partner_a else '',
                'a_last_name':  c.partner_a.last_name  if c.partner_a else '',
                'a_phone':      c.partner_a.phone       if c.partner_a else '',
                # Partner B
                'b_first_name': c.partner_b.first_name if c.partner_b else '',
                'b_last_name':  c.partner_b.last_name  if c.partner_b else '',
                'b_phone':      c.partner_b.phone       if c.partner_b else '',
                'created_at': c.created_at.date().isoformat(),
                # Diagnostics per level
                'diagnostics_per_level': {lvl: level_diag.get(lvl, 0) for lvl in LEVEL_NUMBERS},
                'diagnostics_total': sum(level_diag.values()),
                'practices_count': prac_map.get(cid, 0),
                'relationship_score': round(float(score), 1) if score else None,
                'crisis_level': score_data.get('crisis_level', 'none'),
            })

        return Response({
            'results': results,
            'total': len(results),
            'summary': {
                'total': len(results),
                'normal': crisis_counts.get('none', 0),
                'warning': crisis_counts.get('warning', 0),
                'critical': crisis_counts.get('critical', 0),
            },
            'level_numbers': LEVEL_NUMBERS,
        })
