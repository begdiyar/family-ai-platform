import logging
import random
from datetime import date, timedelta
from typing import Optional, Union

from apps.users.models import User
from apps.couples.repositories import CoupleRepository
from shared.exceptions import BusinessLogicError
from .models import (
    Practice, DailyAssignment, AssignmentSlot, FamilyDevelopmentPlan,
    COMPLETABLE_SLOTS, SLOT_ORDER, FAMILY_LEVELS, STAGE_BY_LEVEL,
)

logger = logging.getLogger(__name__)

# ── Academy article auto-link ─────────────────────────────────────────────────

PRACTICE_TO_ACADEMY_CATEGORY: dict[str, str] = {
    'communication': 'communication',
    'trust':         'trust',
    'intimacy':      'intimacy',
    'romance':       'love',
    'gratitude':     'love',
    'finances':      'finance',
    'relatives':     'communication',
    'children':      'parenting',
}


def _auto_link_academy_article(practice: Practice) -> None:
    if practice.academy_article_id:
        return
    from apps.academy.models import Article
    academy_cat = PRACTICE_TO_ACADEMY_CATEGORY.get(practice.category)
    if not academy_cat:
        return
    article = Article.objects.filter(category=academy_cat, is_published=True).first()
    if article:
        Practice.objects.filter(pk=practice.pk).update(academy_article=article)
        practice.academy_article_id = article.pk
        practice.academy_article = article


# ── Category selection ────────────────────────────────────────────────────────

ZONE_TO_CATEGORIES: dict[str, list[str]] = {
    'communication': ['communication', 'trust'],
    'trust':         ['trust', 'intimacy'],
    'intimacy':      ['intimacy', 'romance'],
    'conflict':      ['communication', 'trust'],
    'values':        ['gratitude', 'romance'],
    'future':        ['finances', 'relatives'],
}

DEFAULT_CATEGORIES = ['communication', 'gratitude', 'romance']

SLOT_PREFERRED_CATEGORIES: dict[str, Optional[list[str]]] = {
    'main':         None,
    'conversation': ['communication', 'trust', 'intimacy'],
    'gesture':      ['romance', 'gratitude'],
    'activity':     None,
    'ritual':       ['romance', 'gratitude', 'intimacy'],
    'growth':       None,
}


# ── Level helpers ─────────────────────────────────────────────────────────────

def _level_row(level: int) -> tuple:
    for row in FAMILY_LEVELS:
        if row[2] == level:
            return row
    return FAMILY_LEVELS[-1]


def _level_info_for_plan(plan: FamilyDevelopmentPlan) -> dict:
    row = _level_row(plan.current_level)
    min_v, max_v, level, label, emoji = row
    if max_v >= 9999:
        xp_current  = plan.total_completed - min_v
        xp_for_next = 0
        progress    = 100
    else:
        span        = max_v - min_v + 1
        xp_current  = max(0, plan.total_completed - min_v)
        xp_for_next = span
        progress    = round(xp_current / span * 100)
    stage_data = STAGE_BY_LEVEL.get(level, (1, 'Восстановление связи', '🌱'))
    return {
        'level':         level,
        'label':         label,
        'emoji':         emoji,
        'xp_current':   xp_current,
        'xp_for_next':  xp_for_next,
        'progress_pct': progress,
        'stage':        stage_data[0],
        'stage_name':   stage_data[1],
        'stage_emoji':  stage_data[2],
    }


# ── Service ───────────────────────────────────────────────────────────────────

class PracticeService:

    # ── Public API ────────────────────────────────────────────────────────────

    @staticmethod
    def get_today(user: User) -> Union[dict, tuple]:
        """
        Returns:
          dict  — if diagnostics gate blocks (requires_diagnostics: True)
          (DailyAssignment, FamilyDevelopmentPlan) — normal case
        """
        couple = CoupleRepository.require_full_couple(user)

        gate = PracticeService._check_diagnostics_gate(couple)
        if gate:
            return gate

        plan  = PracticeService._get_or_create_plan(couple)
        today = date.today()
        assignment, created = DailyAssignment.objects.get_or_create(couple=couple, date=today)
        existing_slots = set(
            AssignmentSlot.objects.filter(assignment=assignment).values_list('slot_type', flat=True)
        )
        if created or not existing_slots:
            PracticeService._fill_assignment(couple, assignment, plan)

        assignment = (
            DailyAssignment.objects
            .prefetch_related('slots__practice', 'slots__practice__academy_article')
            .get(pk=assignment.pk)
        )
        return assignment, plan

    @staticmethod
    def complete_slot(user: User, assignment_id: str, slot: str) -> Union[dict, tuple]:
        if slot not in COMPLETABLE_SLOTS:
            raise BusinessLogicError(
                'INVALID_SLOT',
                f'Допустимые слоты: {", ".join(COMPLETABLE_SLOTS)}',
            )
        couple = CoupleRepository.require_full_couple(user)
        try:
            assignment = DailyAssignment.objects.get(id=assignment_id, couple=couple)
        except DailyAssignment.DoesNotExist:
            raise BusinessLogicError('NOT_FOUND', 'Задание не найдено')
        try:
            slot_obj = AssignmentSlot.objects.get(assignment=assignment, slot_type=slot)
        except AssignmentSlot.DoesNotExist:
            raise BusinessLogicError('NOT_FOUND', 'Слот не найден')

        if not slot_obj.completed:
            from django.utils import timezone
            slot_obj.completed    = True
            slot_obj.completed_at = timezone.now()
            slot_obj.save(update_fields=['completed', 'completed_at', 'updated_at'])
            PracticeService._increment_plan(couple)

        plan = PracticeService._get_or_create_plan(couple)
        assignment = (
            DailyAssignment.objects
            .prefetch_related('slots__practice', 'slots__practice__academy_article')
            .get(pk=assignment.pk)
        )
        return assignment, plan

    @staticmethod
    def get_plan(user: User) -> Union[dict, FamilyDevelopmentPlan]:
        couple = CoupleRepository.require_full_couple(user)
        gate = PracticeService._check_diagnostics_gate(couple)
        if gate:
            return gate
        return PracticeService._get_or_create_plan(couple)

    @staticmethod
    def get_stats(user: User) -> dict:
        couple = CoupleRepository.require_full_couple(user)

        slots_qs = (
            AssignmentSlot.objects
            .filter(assignment__couple=couple, slot_type__in=COMPLETABLE_SLOTS)
            .select_related('practice')
        )

        total_slots     = slots_qs.count()
        total_completed = slots_qs.filter(completed=True).count()

        category_stats: dict = {}
        for slot in slots_qs:
            if not slot.practice:
                continue
            cat       = slot.practice.category
            cat_label = slot.practice.get_category_display()
            if cat not in category_stats:
                category_stats[cat] = {'label': cat_label, 'assigned': 0, 'completed': 0}
            category_stats[cat]['assigned'] += 1
            if slot.completed:
                category_stats[cat]['completed'] += 1

        fav = max(
            category_stats,
            key=lambda c: category_stats[c]['completed'],
            default=None,
        )

        streak = PracticeService._calc_streak(couple)

        # Use plan for level info if available
        plan = FamilyDevelopmentPlan.objects.filter(couple=couple).first()
        if plan:
            level_info = _level_info_for_plan(plan)
        else:
            level_info = _level_info_for_plan(
                FamilyDevelopmentPlan(couple=couple, total_completed=total_completed)
            )

        return {
            'total_completed':   total_completed,
            'total_slots':       total_slots,
            'completion_rate':   round(total_completed / total_slots * 100) if total_slots else 0,
            'current_streak':    streak,
            'favorite_category': fav,
            'category_progress': category_stats,
            'family_level':      level_info,
        }

    @staticmethod
    def get_history(user: User, limit: int = 14) -> list:
        couple = CoupleRepository.require_full_couple(user)
        return list(
            DailyAssignment.objects
            .filter(couple=couple)
            .prefetch_related('slots__practice', 'slots__practice__academy_article')
            .order_by('-date')[:limit]
        )

    @staticmethod
    def update_plan_from_analytics(couple, analytics_result) -> None:
        """Called after analytics are calculated to refresh zone priorities."""
        try:
            from apps.analytics.services import AnalyticsService
            zones = AnalyticsService.get_zone_detail_for_result(analytics_result)
            weak  = sorted(
                zones,
                key=lambda z: z['couple_avg'],
            )

            priority  = weak[0]['zone'] if len(weak) > 0 else 'communication'
            secondary = weak[1]['zone'] if len(weak) > 1 else 'trust'
            tertiary  = weak[2]['zone'] if len(weak) > 2 else 'intimacy'

            from django.utils import timezone
            now  = timezone.now()
            plan, created = FamilyDevelopmentPlan.objects.get_or_create(couple=couple)

            if created:
                count = AssignmentSlot.objects.filter(
                    assignment__couple=couple,
                    slot_type__in=COMPLETABLE_SLOTS,
                    completed=True,
                ).count()
                plan.total_completed = count

            plan.priority_zone     = priority
            plan.secondary_zone    = secondary
            plan.tertiary_zone     = tertiary
            plan.last_diagnostic_at = now
            plan.next_diagnostic_at = now + timedelta(days=14)
            plan.recalculate_level()
            plan.save()
        except Exception:
            logger.exception('update_plan_from_analytics failed')

    # ── Internal ──────────────────────────────────────────────────────────────

    @staticmethod
    def _check_diagnostics_gate(couple) -> Optional[dict]:
        from apps.diagnostics.repositories import DiagnosticRepository, JourneyRepository

        # Определяем текущий уровень семьи из FamilyJourney
        journey = JourneyRepository.get_for_couple(couple)
        if not journey:
            # Journey ещё не создан — создаём и требуем диагностику уровня 1
            JourneyRepository.get_or_create(couple)
            return {
                'requires_diagnostics': True,
                'partner_a_done': False,
                'partner_b_done': False,
                'current_level': 1,
                'locked': True,
                'reason': 'waiting_partner',
            }

        current_level = journey.max_unlocked_level
        status = DiagnosticRepository.get_couple_completion_status(couple, current_level)

        if status['partner_a_completed'] and status['partner_b_completed']:
            return None  # доступ разрешён

        reason = 'waiting_partner' if status['partner_a_completed'] else 'not_started'
        return {
            'requires_diagnostics': True,
            'locked': True,
            'reason': reason,
            'current_level': current_level,
            'partner_a_done': status['partner_a_completed'],
            'partner_b_done': status['partner_b_completed'],
        }

    @staticmethod
    def _get_or_create_plan(couple) -> FamilyDevelopmentPlan:
        plan, created = FamilyDevelopmentPlan.objects.get_or_create(couple=couple)
        if created:
            count = AssignmentSlot.objects.filter(
                assignment__couple=couple,
                slot_type__in=COMPLETABLE_SLOTS,
                completed=True,
            ).count()
            plan.total_completed = count
            plan.recalculate_level()
            plan.save()
        return plan

    @staticmethod
    def _increment_plan(couple) -> None:
        from django.db.models import F
        updated = FamilyDevelopmentPlan.objects.filter(couple=couple).update(
            total_completed=F('total_completed') + 1,
        )
        if updated:
            plan = FamilyDevelopmentPlan.objects.get(couple=couple)
            old_level = plan.current_level
            plan.recalculate_level()
            plan.save(update_fields=['current_level', 'current_stage', 'updated_at'])

            # Проверяем разблокировку следующего уровня диагностики при смене XP-уровня
            if plan.current_level != old_level:
                try:
                    from apps.diagnostics.services import JourneyService
                    JourneyService.check_and_unlock_next_level(couple)
                except Exception:
                    logger.warning("Failed to unlock next diagnostics level for couple %s", couple.id, exc_info=True)

    @staticmethod
    def _fill_assignment(couple, assignment: DailyAssignment, plan: Optional[FamilyDevelopmentPlan] = None) -> None:
        categories  = PracticeService._get_target_categories(couple, plan)
        exclude_ids = PracticeService._get_recent_ids(couple, assignment.date)

        slots_to_create = []
        for slot_type in SLOT_ORDER:
            preferred = SLOT_PREFERRED_CATEGORIES.get(slot_type)
            pick_cats = preferred if preferred else categories
            practice  = PracticeService._pick(slot_type, pick_cats, exclude_ids)
            if practice:
                exclude_ids.add(str(practice.pk))
                if slot_type == 'growth':
                    _auto_link_academy_article(practice)
            slots_to_create.append(
                AssignmentSlot(
                    assignment=assignment,
                    slot_type=slot_type,
                    practice=practice,
                    completed=False,
                )
            )

        AssignmentSlot.objects.bulk_create(slots_to_create, ignore_conflicts=True)
        assignment.categories_used = categories
        assignment.save(update_fields=['categories_used', 'updated_at'])

    @staticmethod
    def _get_target_categories(couple, plan: Optional[FamilyDevelopmentPlan] = None) -> list[str]:
        # Use plan priority zones if available
        if plan and plan.priority_zone:
            cats: list[str] = []
            for zone in [plan.priority_zone, plan.secondary_zone, plan.tertiary_zone]:
                if not zone:
                    continue
                for cat in ZONE_TO_CATEGORIES.get(zone, []):
                    if cat not in cats:
                        cats.append(cat)
                if len(cats) >= 3:
                    break
            if cats:
                return cats[:3]

        # Fallback: compute from latest analytics
        try:
            from apps.analytics.repositories import AnalyticsRepository
            from apps.analytics.services import AnalyticsService
            result = AnalyticsRepository.get_latest_for_couple(couple)
            if not result:
                return list(DEFAULT_CATEGORIES)

            zones = AnalyticsService.get_zone_detail_for_result(result)
            weak  = sorted(
                [z for z in zones if z['couple_avg'] < 60],
                key=lambda z: z['couple_avg'],
            )

            cats = []
            for z in weak:
                for cat in ZONE_TO_CATEGORIES.get(z['zone'], []):
                    if cat not in cats:
                        cats.append(cat)
                if len(cats) >= 3:
                    break

            return cats[:3] if cats else ['gratitude', 'romance', 'intimacy']
        except Exception:
            logger.exception('Could not get analytics for practice selection')
            return list(DEFAULT_CATEGORIES)

    @staticmethod
    def _get_recent_ids(couple, today: date) -> set:
        cutoff = today - timedelta(days=30)
        ids = (
            AssignmentSlot.objects
            .filter(
                assignment__couple=couple,
                assignment__date__gte=cutoff,
                assignment__date__lt=today,
            )
            .exclude(practice__isnull=True)
            .values_list('practice_id', flat=True)
        )
        return {str(pid) for pid in ids}

    @staticmethod
    def _pick(slot_type: str, categories: list[str], exclude_ids: set) -> Optional[Practice]:
        base = Practice.objects.filter(is_active=True, slot_type=slot_type)

        q = base.filter(category__in=categories)
        if exclude_ids:
            q = q.exclude(id__in=list(exclude_ids))
        p = PracticeService._random(q)
        if p:
            return p

        q2 = base
        if exclude_ids:
            q2 = q2.exclude(id__in=list(exclude_ids))
        p2 = PracticeService._random(q2)
        if p2:
            return p2

        return PracticeService._random(base)

    @staticmethod
    def _random(qs) -> Optional[Practice]:
        count = qs.count()
        if count == 0:
            return None
        return qs[random.randint(0, count - 1)]

    @staticmethod
    def _calc_streak(couple) -> int:
        today = date.today()
        completed_dates = set(
            AssignmentSlot.objects
            .filter(
                assignment__couple=couple,
                slot_type__in=COMPLETABLE_SLOTS,
                completed=True,
            )
            .values_list('assignment__date', flat=True)
            .distinct()
        )
        streak = 0
        for i in range(365):
            if (today - timedelta(days=i)) in completed_dates:
                streak += 1
            elif i > 0:
                break
        return streak

    @staticmethod
    def _empty_stats() -> dict:
        from .models import FamilyDevelopmentPlan
        dummy = FamilyDevelopmentPlan(total_completed=0, current_level=1, current_stage=1)
        return {
            'total_completed':   0,
            'total_slots':       0,
            'completion_rate':   0,
            'current_streak':    0,
            'favorite_category': None,
            'category_progress': {},
            'family_level':      _level_info_for_plan(dummy),
        }
