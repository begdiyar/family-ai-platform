from rest_framework import serializers
from .models import RecoveryPlan, PlanTask, TaskCompletion


class TaskSerializer(serializers.ModelSerializer):
    completed_by_me = serializers.SerializerMethodField()
    completed_by_partner = serializers.SerializerMethodField()

    def get_completed_by_me(self, obj):
        completed_ids = self.context.get('my_completed_ids', set())
        return str(obj.id) in completed_ids

    def get_completed_by_partner(self, obj):
        completed_ids = self.context.get('partner_completed_ids', set())
        return str(obj.id) in completed_ids

    class Meta:
        model = PlanTask
        fields = ['id', 'week_number', 'day_of_week', 'title', 'description',
                  'task_type', 'assigned_to', 'order_index',
                  'completed_by_me', 'completed_by_partner']


class PlanDetailSerializer(serializers.ModelSerializer):
    weeks = serializers.SerializerMethodField()
    overall_progress = serializers.SerializerMethodField()
    current_week = serializers.SerializerMethodField()

    WEEK_THEMES = ['Коммуникация', 'Близость', 'Доверие']

    def _get_completion_sets(self, obj):
        if 'my_completed_ids' not in self.context:
            user = self.context.get('user')
            couple = self.context.get('couple')
            partner = couple.get_partner(user) if couple and user else None

            my_ids = set(
                str(tid) for tid in
                TaskCompletion.objects.filter(task__plan=obj, user=user).values_list('task_id', flat=True)
            ) if user else set()

            partner_ids = set(
                str(tid) for tid in
                TaskCompletion.objects.filter(task__plan=obj, user=partner).values_list('task_id', flat=True)
            ) if partner else set()

            self.context['my_completed_ids'] = my_ids
            self.context['partner_completed_ids'] = partner_ids

        return self.context['my_completed_ids'], self.context['partner_completed_ids']

    def get_weeks(self, obj):
        my_ids, partner_ids = self._get_completion_sets(obj)
        task_ctx = {**self.context, 'my_completed_ids': my_ids, 'partner_completed_ids': partner_ids}

        weeks = []
        all_tasks = list(obj.tasks.all())
        tasks_by_week: dict[int, list] = {}
        for t in all_tasks:
            tasks_by_week.setdefault(t.week_number, []).append(t)

        for w in range(1, obj.duration_weeks + 1):
            tasks = tasks_by_week.get(w, [])
            week_tasks = TaskSerializer(tasks, many=True, context=task_ctx).data
            completed_count = sum(1 for t in tasks if str(t.id) in my_ids)
            total = len(tasks)
            progress = round(completed_count / total * 100) if total else 0
            unlocked = w == 1 or self._prev_week_done(tasks_by_week.get(w - 1, []), my_ids)
            weeks.append({
                'week': w,
                'theme': self.WEEK_THEMES[w - 1] if w <= len(self.WEEK_THEMES) else f'Неделя {w}',
                'tasks': week_tasks,
                'progress': progress,
                'locked': not unlocked,
            })
        return weeks

    def _prev_week_done(self, prev_tasks: list, my_ids: set) -> bool:
        if not prev_tasks:
            return True
        return all(str(t.id) in my_ids for t in prev_tasks)

    def get_overall_progress(self, obj):
        my_ids, _ = self._get_completion_sets(obj)
        total = obj.tasks.count()
        return round(len(my_ids) / total * 100) if total else 0

    def get_current_week(self, obj):
        my_ids, _ = self._get_completion_sets(obj)
        all_tasks = list(obj.tasks.all())
        tasks_by_week: dict[int, list] = {}
        for t in all_tasks:
            tasks_by_week.setdefault(t.week_number, []).append(t)

        for w in range(1, obj.duration_weeks + 1):
            tasks = tasks_by_week.get(w, [])
            if any(str(t.id) not in my_ids for t in tasks):
                return w
        return obj.duration_weeks

    class Meta:
        model = RecoveryPlan
        fields = ['id', 'title', 'status', 'duration_weeks', 'started_at',
                  'overall_progress', 'current_week', 'weeks']


class CompleteTaskSerializer(serializers.Serializer):
    note = serializers.CharField(required=False, allow_null=True, allow_blank=True)


class CreatePlanSerializer(serializers.Serializer):
    result_id = serializers.UUIDField(required=False, allow_null=True)
