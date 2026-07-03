import logging
from datetime import date, timedelta

logger = logging.getLogger(__name__)


def _age(birth_date) -> int | None:
    if not birth_date:
        return None
    today = date.today()
    return today.year - birth_date.year - (
        (today.month, today.day) < (birth_date.month, birth_date.day)
    )


def _years_since(d) -> int | None:
    if not d:
        return None
    today = date.today()
    return today.year - d.year - (
        (today.month, today.day) < (d.month, d.day)
    )


class CoupleContext:
    """All AI-relevant data about a couple, loaded once and reused across services."""

    __slots__ = (
        # ── базовые ──
        'partner_a_name',
        'partner_b_name',
        'relationship_index',
        'crisis_level',
        'family_level',
        'zones',
        'weak_zones',
        'strengths',
        'problem_chain',
        'bridge_analysis',
        'priority_zone',
        'completed_practices',
        'family_values',
        'communication_rules',
        # ── профиль партнёра A ──
        'partner_a_gender',
        'partner_a_age',
        'partner_a_occupation',
        'partner_a_education',
        'partner_a_conflict_style',
        'partner_a_support_style',
        # ── профиль партнёра B ──
        'partner_b_gender',
        'partner_b_age',
        'partner_b_occupation',
        'partner_b_education',
        'partner_b_conflict_style',
        'partner_b_support_style',
        # ── профиль пары ──
        'relationship_status',
        'relationship_years',
        'marriage_years',
        'lives_with_parents',
        'relatives_influence_level',
        'religious_traditions_importance',
        'couple_family_values',
        # ── дети ──
        'children',
        # ── динамика ──
        'relationship_delta',
        'zone_deltas',
        # ── зоны по статусу ──
        'strong_zones',
        'growth_zones',
        'attention_zones',
        # ── дополнительные приоритетные зоны ──
        'secondary_zone',
        'tertiary_zone',
    )

    def __init__(self):
        self.partner_a_name: str = ''
        self.partner_b_name: str = ''
        self.relationship_index = None
        self.crisis_level: str = 'none'
        self.family_level: int = 0
        self.zones: list = []
        self.weak_zones: list = []
        self.strengths = None
        self.problem_chain: list = []
        self.bridge_analysis = None
        self.priority_zone: str = ''
        self.completed_practices: list = []
        self.family_values: list = []
        self.communication_rules: list = []
        # ── профиль партнёра A ──
        self.partner_a_gender: str = ''
        self.partner_a_age = None
        self.partner_a_occupation: str = ''
        self.partner_a_education: str = ''
        self.partner_a_conflict_style: str = ''
        self.partner_a_support_style: str = ''
        # ── профиль партнёра B ──
        self.partner_b_gender: str = ''
        self.partner_b_age = None
        self.partner_b_occupation: str = ''
        self.partner_b_education: str = ''
        self.partner_b_conflict_style: str = ''
        self.partner_b_support_style: str = ''
        # ── профиль пары ──
        self.relationship_status: str = ''
        self.relationship_years = None
        self.marriage_years = None
        self.lives_with_parents: bool = False
        self.relatives_influence_level = None
        self.religious_traditions_importance = None
        self.couple_family_values: list = []
        # ── дети ──
        self.children: list = []
        # ── динамика ──
        self.relationship_delta = None
        self.zone_deltas: dict = {}
        # ── зоны по статусу ──
        self.strong_zones: list = []
        self.growth_zones: list = []
        self.attention_zones: list = []
        # ── дополнительные приоритетные зоны ──
        self.secondary_zone: str = ''
        self.tertiary_zone: str = ''


class ContextBuilder:
    """
    Single source of truth for couple context used by AI services.

    Usage:
        ctx = ContextBuilder.build(couple)
        # ctx.relationship_index, ctx.weak_zones, ctx.family_values, …
    """

    @staticmethod
    def build(couple) -> CoupleContext:
        ctx = CoupleContext()

        if not couple:
            return ctx

        ctx.partner_a_name = couple.partner_a.first_name
        ctx.partner_b_name = (
            couple.partner_b.first_name if couple.partner_b else 'партнёр'
        )

        ContextBuilder._load_analytics(ctx, couple)
        ContextBuilder._load_journey(ctx, couple)
        ContextBuilder._load_plan(ctx, couple)
        ContextBuilder._load_practices(ctx, couple)
        ContextBuilder._load_constitution(ctx, couple)
        ContextBuilder._load_user_profile(ctx, couple.partner_a, 'partner_a')
        ContextBuilder._load_user_profile(ctx, couple.partner_b, 'partner_b')
        ContextBuilder._load_couple_profile(ctx, couple)
        ContextBuilder._load_children(ctx, couple)

        return ctx

    # ── Private loaders ───────────────────────────────────────────────────

    @staticmethod
    def _load_analytics(ctx: CoupleContext, couple) -> None:
        try:
            from apps.analytics.repositories import AnalyticsRepository
            from apps.analytics.services import AnalyticsService

            result = AnalyticsRepository.get_latest_for_couple(couple)
            if not result:
                return

            ctx.relationship_index = round(float(result.overall_score))
            ctx.crisis_level = result.crisis_level or 'none'
            ctx.bridge_analysis = result.bridge_analysis
            ctx.strengths = result.strengths_summary
            ctx.problem_chain = result.problem_chain or []

            zones = AnalyticsService.get_zone_detail_for_result(result)
            ctx.zones = zones
            ctx.weak_zones = [z for z in zones if z['status'] == 'attention']
            ctx.strong_zones = [z for z in zones if z['status'] == 'strong']
            ctx.growth_zones = [z for z in zones if z['status'] == 'growth']
            ctx.attention_zones = ctx.weak_zones  # alias for clarity

            # Dynamics: compare with previous result
            prev = AnalyticsRepository.get_previous_for_couple(couple, exclude_id=result.id)
            if prev:
                prev_score = round(float(prev.overall_score))
                ctx.relationship_delta = ctx.relationship_index - prev_score

                prev_zones = AnalyticsService.get_zone_detail_for_result(prev)
                prev_by_key = {z['zone']: z['couple_avg'] for z in prev_zones}
                deltas = {}
                for z in zones:
                    key = z['zone']
                    if key in prev_by_key:
                        deltas[key] = {
                            'prev': round(prev_by_key[key]),
                            'curr': round(z['couple_avg']),
                            'delta': round(z['couple_avg'] - prev_by_key[key]),
                        }
                ctx.zone_deltas = deltas

        except Exception as e:
            logger.warning('ContextBuilder._load_analytics failed: %s', e)

    @staticmethod
    def _load_journey(ctx: CoupleContext, couple) -> None:
        try:
            from apps.diagnostics.models import FamilyJourney

            journey = FamilyJourney.objects.filter(couple=couple).first()
            if journey:
                ctx.family_level = journey.last_completed_level or 0
        except Exception as e:
            logger.warning('ContextBuilder._load_journey failed: %s', e)

    @staticmethod
    def _load_plan(ctx: CoupleContext, couple) -> None:
        try:
            from apps.practices.models import FamilyDevelopmentPlan

            plan = FamilyDevelopmentPlan.objects.filter(couple=couple).first()
            if plan:
                ctx.priority_zone = plan.priority_zone or ''
                ctx.secondary_zone = plan.secondary_zone or ''
                ctx.tertiary_zone = plan.tertiary_zone or ''
        except Exception as e:
            logger.warning('ContextBuilder._load_plan failed: %s', e)

    @staticmethod
    def _load_practices(ctx: CoupleContext, couple) -> None:
        try:
            from apps.practices.models import DailyAssignment

            since = date.today() - timedelta(days=7)
            assignments = list(
                DailyAssignment.objects
                .filter(couple=couple, date__gte=since)
                .prefetch_related('slots__practice')
                .order_by('-date')[:10]
            )

            titles = []
            for assignment in assignments:
                if assignment.is_fully_completed:
                    for slot in assignment.slots.all():
                        if slot.practice and slot.completed:
                            titles.append(slot.practice.title)
            ctx.completed_practices = titles[:5]

        except Exception as e:
            logger.warning('ContextBuilder._load_practices failed: %s', e)

    @staticmethod
    def _load_constitution(ctx: CoupleContext, couple) -> None:
        try:
            from apps.constitution.models import FamilyConstitution

            const = FamilyConstitution.objects.filter(couple=couple).first()
            if const:
                ctx.family_values = const.values or []
                ctx.communication_rules = const.communication_rules or []
        except Exception as e:
            logger.warning('ContextBuilder._load_constitution failed: %s', e)

    @staticmethod
    def _load_user_profile(ctx: CoupleContext, user, prefix: str) -> None:
        if not user:
            return
        try:
            setattr(ctx, f'{prefix}_gender', user.gender or '')
            setattr(ctx, f'{prefix}_age', _age(user.birth_date))
            setattr(ctx, f'{prefix}_occupation', user.occupation or '')
            setattr(ctx, f'{prefix}_education', user.education_level or '')
            pref = getattr(user, 'communication_pref', None)
            if pref:
                setattr(ctx, f'{prefix}_conflict_style', pref.conflict_style or '')
                setattr(ctx, f'{prefix}_support_style', pref.support_style or '')
        except Exception as e:
            logger.warning('ContextBuilder._load_user_profile(%s) failed: %s', prefix, e)

    @staticmethod
    def _load_couple_profile(ctx: CoupleContext, couple) -> None:
        try:
            ctx.relationship_status = couple.relationship_status or ''
            ctx.relationship_years = _years_since(couple.relationship_start_date)
            ctx.marriage_years = _years_since(couple.marriage_date)
            ctx.lives_with_parents = couple.lives_with_parents
            ctx.relatives_influence_level = couple.relatives_influence_level
            ctx.religious_traditions_importance = couple.religious_traditions_importance
            ctx.couple_family_values = list(
                couple.family_values.values_list('slug', flat=True)
            )
        except Exception as e:
            logger.warning('ContextBuilder._load_couple_profile failed: %s', e)

    @staticmethod
    def _load_children(ctx: CoupleContext, couple) -> None:
        try:
            from apps.couples.models import Child

            children = Child.objects.filter(couple=couple).order_by('birth_date')
            ctx.children = [
                {'age': _age(c.birth_date), 'gender': c.gender or ''}
                for c in children
            ]
        except Exception as e:
            logger.warning('ContextBuilder._load_children failed: %s', e)
