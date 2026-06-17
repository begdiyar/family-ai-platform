from shared.exceptions import BusinessLogicError, NotFoundError
from apps.users.models import User
from apps.couples.repositories import CoupleRepository
from apps.analytics.repositories import AnalyticsRepository
from .models import RecoveryPlan, PlanTask, TaskCompletion
from .repositories import PlanRepository

WEEK_THEMES = ['Коммуникация', 'Близость', 'Доверие']

DEFAULT_TASKS = [
    # Неделя 1 — Коммуникация (день 1–7)
    {'week_number': 1, 'day_of_week': 1, 'title': '5 минут без телефона',
     'description': 'Проведите 5 минут вместе, убрав телефоны. Просто побудьте рядом.',
     'task_type': 'exercise', 'assigned_to': 'both', 'order_index': 1},
    {'week_number': 1, 'day_of_week': 2, 'title': 'Вопрос дня',
     'description': 'Спросите партнёра: «Что сделало тебя счастливым сегодня?»',
     'task_type': 'question', 'assigned_to': 'both', 'order_index': 2},
    {'week_number': 1, 'day_of_week': 3, 'title': 'Активное слушание',
     'description': 'Дайте партнёру рассказать о своём дне 5 минут, не перебивая и не давая советов.',
     'task_type': 'practice', 'assigned_to': 'both', 'order_index': 3},
    {'week_number': 1, 'day_of_week': 4, 'title': 'Один искренний комплимент',
     'description': 'Скажите партнёру конкретный комплимент: не «ты хороший», а за что-то конкретное.',
     'task_type': 'practice', 'assigned_to': 'both', 'order_index': 4},
    {'week_number': 1, 'day_of_week': 5, 'title': 'Совместная прогулка',
     'description': 'Прогуляйтесь вместе 20 минут без телефонов. Говорите о том, что видите вокруг.',
     'task_type': 'exercise', 'assigned_to': 'both', 'order_index': 5},
    {'week_number': 1, 'day_of_week': 6, 'title': 'Благодарность перед сном',
     'description': 'Скажите партнёру одну вещь, за которую вы ему благодарны сегодня.',
     'task_type': 'practice', 'assigned_to': 'both', 'order_index': 6},
    {'week_number': 1, 'day_of_week': 7, 'title': 'Разговор без критики',
     'description': 'Поговорите 15 минут о том, что вам нравится друг в друге. Только позитив.',
     'task_type': 'question', 'assigned_to': 'both', 'order_index': 7},
    # Неделя 2 — Доверие (день 1–7)
    {'week_number': 2, 'day_of_week': 1, 'title': 'Разговор о мечтах',
     'description': 'Поделитесь с партнёром одной своей мечтой, о которой редко говорите.',
     'task_type': 'question', 'assigned_to': 'both', 'order_index': 1},
    {'week_number': 2, 'day_of_week': 2, 'title': 'Объятие на 20 секунд',
     'description': 'Обнимите партнёра на 20 секунд. Это снижает уровень стресса и укрепляет связь.',
     'task_type': 'practice', 'assigned_to': 'both', 'order_index': 2},
    {'week_number': 2, 'day_of_week': 3, 'title': 'Признание уязвимости',
     'description': 'Поделитесь чем-то, о чём боитесь говорить. Партнёр только слушает, не оценивает.',
     'task_type': 'practice', 'assigned_to': 'both', 'order_index': 3},
    {'week_number': 2, 'day_of_week': 4, 'title': 'Выполнение обещания',
     'description': 'Дайте друг другу одно небольшое обещание и выполните его сегодня.',
     'task_type': 'exercise', 'assigned_to': 'both', 'order_index': 4},
    {'week_number': 2, 'day_of_week': 5, 'title': 'Письмо партнёру',
     'description': 'Напишите партнёру короткое письмо (даже в мессенджере): что цените в нём больше всего.',
     'task_type': 'exercise', 'assigned_to': 'both', 'order_index': 5},
    {'week_number': 2, 'day_of_week': 6, 'title': 'Ужин без экранов',
     'description': 'Приготовьте или закажите ужин и поешьте вместе без телевизора и телефонов.',
     'task_type': 'practice', 'assigned_to': 'both', 'order_index': 6},
    {'week_number': 2, 'day_of_week': 7, 'title': 'Откровенный разговор',
     'description': 'Обсудите: что сейчас мешает вашим отношениям? Говорите спокойно, без обвинений.',
     'task_type': 'question', 'assigned_to': 'both', 'order_index': 7},
    # Неделя 3 — Близость (день 1–7)
    {'week_number': 3, 'day_of_week': 1, 'title': 'Разговор о доверии',
     'description': 'Обсудите: что помогает вам чувствовать доверие? Что его подрывает?',
     'task_type': 'question', 'assigned_to': 'both', 'order_index': 1},
    {'week_number': 3, 'day_of_week': 2, 'title': 'Воспоминание о лучшем моменте',
     'description': 'Вспомните вместе один лучший момент в ваших отношениях и расскажите, почему он важен.',
     'task_type': 'practice', 'assigned_to': 'both', 'order_index': 2},
    {'week_number': 3, 'day_of_week': 3, 'title': 'Поддержка без советов',
     'description': 'Поделитесь чем-то, что вас беспокоит. Партнёр только слушает, не даёт советов.',
     'task_type': 'practice', 'assigned_to': 'both', 'order_index': 3},
    {'week_number': 3, 'day_of_week': 4, 'title': 'Совместное хобби',
     'description': 'Попробуйте вместе что-то новое: приготовьте незнакомое блюдо, сыграйте в настолку, посмотрите новый фильм.',
     'task_type': 'exercise', 'assigned_to': 'both', 'order_index': 4},
    {'week_number': 3, 'day_of_week': 5, 'title': 'Заботливый жест',
     'description': 'Сделайте что-то приятное для партнёра без повода: кофе, записка, маленький подарок.',
     'task_type': 'practice', 'assigned_to': 'both', 'order_index': 5},
    {'week_number': 3, 'day_of_week': 6, 'title': 'Планы на будущее',
     'description': 'Обсудите одну совместную цель на ближайшие полгода. Запишите её.',
     'task_type': 'question', 'assigned_to': 'both', 'order_index': 6},
    {'week_number': 3, 'day_of_week': 7, 'title': 'Итоговый разговор',
     'description': 'Обсудите: что изменилось за 21 день? Что хотите продолжать делать вместе?',
     'task_type': 'question', 'assigned_to': 'both', 'order_index': 7},
]


class PlanService:
    @staticmethod
    def create_plan(user: User, result_id: str = None) -> RecoveryPlan:
        couple = CoupleRepository.get_active_for_user(user)
        if not couple:
            raise BusinessLogicError('NO_COUPLE', 'Нет активной пары')

        existing = PlanRepository.get_active_for_couple(couple)
        if existing:
            raise BusinessLogicError('PLAN_ALREADY_EXISTS', 'У вашей пары уже есть активный план')

        result = None
        if result_id:
            result = AnalyticsRepository.get_by_id(result_id)
        else:
            result = AnalyticsRepository.get_latest_for_couple(couple)

        plan = PlanRepository.create(couple=couple, user=user, result=result)
        PlanRepository.bulk_create_tasks(plan, DEFAULT_TASKS)
        return plan

    @staticmethod
    def complete_task(user: User, plan_id: str, task_id: str, note: str = None) -> dict:
        plan = RecoveryPlan.objects.filter(id=plan_id).first()
        if not plan:
            raise NotFoundError('PLAN_NOT_FOUND', 'План не найден')
        task = PlanRepository.get_task(task_id, plan_id)
        if not task:
            raise NotFoundError('TASK_NOT_FOUND', 'Задание не найдено')
        completion = PlanRepository.create_completion(task, user, note)
        progress = PlanRepository.get_week_progress(plan, task.week_number, user)

        couple = plan.couple
        partner = couple.get_partner(user)
        partner_completed = TaskCompletion.objects.filter(task=task, user=partner).exists() if partner else False

        return {
            'task_id': str(task.id),
            'completed_at': completion.created_at,
            'partner_completed': partner_completed,
            'week_progress': progress['percent'],
        }

    @staticmethod
    def undo_task(user: User, task_id: str, plan_id: str) -> None:
        task = PlanRepository.get_task(task_id, plan_id)
        if not task:
            raise NotFoundError('TASK_NOT_FOUND', 'Задание не найдено')
        PlanRepository.delete_completion(task, user)
