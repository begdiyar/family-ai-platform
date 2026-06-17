from typing import Optional, List
from apps.couples.models import Couple
from apps.users.models import User
from .models import RecoveryPlan, PlanTask, TaskCompletion


class PlanRepository:
    @staticmethod
    def get_active_for_couple(couple: Couple) -> Optional[RecoveryPlan]:
        return RecoveryPlan.objects.filter(
            couple=couple, status=RecoveryPlan.STATUS_ACTIVE
        ).prefetch_related('tasks__completions').first()

    @staticmethod
    def create(couple: Couple, user: User, result=None, title: str = 'Ваш план восстановления',
               duration_weeks: int = 3) -> RecoveryPlan:
        return RecoveryPlan.objects.create(
            couple=couple,
            created_by=user,
            result=result,
            title=title,
            duration_weeks=duration_weeks,
        )

    @staticmethod
    def bulk_create_tasks(plan: RecoveryPlan, tasks_data: list) -> None:
        PlanTask.objects.bulk_create([
            PlanTask(
                plan=plan,
                week_number=t['week_number'],
                day_of_week=t.get('day_of_week'),
                title=t['title'],
                description=t.get('description'),
                task_type=t.get('task_type', PlanTask.TASK_TYPE_EXERCISE),
                assigned_to=t.get('assigned_to', PlanTask.ASSIGNED_BOTH),
                order_index=t.get('order_index', 0),
            )
            for t in tasks_data
        ])

    @staticmethod
    def get_task(task_id, plan_id) -> Optional[PlanTask]:
        return PlanTask.objects.filter(id=task_id, plan_id=plan_id).first()

    @staticmethod
    def create_completion(task: PlanTask, user: User, note: str = None) -> TaskCompletion:
        completion, _ = TaskCompletion.objects.get_or_create(
            task=task,
            user=user,
            defaults={'note': note},
        )
        return completion

    @staticmethod
    def delete_completion(task: PlanTask, user: User) -> None:
        TaskCompletion.objects.filter(task=task, user=user).delete()

    @staticmethod
    def get_week_progress(plan: RecoveryPlan, week: int, user: User) -> dict:
        tasks = PlanTask.objects.filter(plan=plan, week_number=week)
        total = tasks.count()
        completed = TaskCompletion.objects.filter(task__in=tasks, user=user).count()
        return {'week': week, 'total': total, 'completed': completed,
                'percent': round(completed / total * 100) if total else 0}
