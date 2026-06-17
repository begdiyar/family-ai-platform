import json
import logging
from datetime import date
from apps.users.models import User
from apps.couples.repositories import CoupleRepository
from shared.exceptions import BusinessLogicError
from shared.utils import get_i18n
from .models import DailyPractice, PracticeCompletion

logger = logging.getLogger(__name__)

PRACTICE_FIELDS = [
    'question_of_day', 'conversation_topic', 'trust_exercise',
    'communication_exercise', 'family_activity', 'romantic_idea',
]

DEFAULT_PRACTICES = {
    'ru': [
        {
            'question_of_day': 'Что сделало тебя счастливым сегодня — даже самое маленькое?',
            'conversation_topic': 'Расскажите друг другу о вашей самой любимой совместной памяти',
            'trust_exercise': 'Скажи партнёру одну вещь, которую ты боишься, но доверяешь ему это знать',
            'communication_exercise': '5 минут без телефонов — просто смотрите друг на друга и говорите',
            'family_activity': 'Приготовьте вместе одно блюдо, которое давно хотели попробовать',
            'romantic_idea': 'Напишите партнёру записку с тремя причинами, почему вы рады быть с ним',
        },
        {
            'question_of_day': 'Что я могу сделать для тебя завтра, чтобы твой день стал лучше?',
            'conversation_topic': 'Какой была ваша первая встреча с точки зрения каждого из вас?',
            'trust_exercise': 'Поделись одной мечтой, о которой редко говоришь вслух',
            'communication_exercise': 'Активное слушание: 10 минут один говорит, другой только слушает без советов',
            'family_activity': 'Посмотрите вместе фотографии из начала ваших отношений',
            'romantic_idea': 'Обнимите друг друга на 20 секунд прямо сейчас',
        },
    ],
    'en': [
        {
            'question_of_day': 'What made you happy today — even the smallest thing?',
            'conversation_topic': 'Tell each other about your favorite shared memory',
            'trust_exercise': 'Tell your partner one thing you are afraid of but trust them to know',
            'communication_exercise': '5 minutes without phones — just look at each other and talk',
            'family_activity': 'Cook together a dish you have been wanting to try for a long time',
            'romantic_idea': 'Write your partner a note with three reasons you are glad to be with them',
        },
        {
            'question_of_day': 'What can I do for you tomorrow to make your day better?',
            'conversation_topic': 'What was your first meeting like from each of your perspectives?',
            'trust_exercise': 'Share one dream you rarely say out loud',
            'communication_exercise': 'Active listening: 10 minutes — one talks, the other only listens without giving advice',
            'family_activity': 'Look together at photos from the beginning of your relationship',
            'romantic_idea': 'Hug each other for 20 seconds right now',
        },
    ],
    'uz': [
        {
            'question_of_day': "Bugun sizni nima baxtli qildi — hatto eng kichik narsa ham?",
            'conversation_topic': "Bir-biringizga eng sevimli umumiy xotirangiz haqida gapirib bering",
            'trust_exercise': "Turmush o'rtoqingizga qo'rqadigan, lekin unga ishonib aytadigan bir narsangizni ayting",
            'communication_exercise': "5 daqiqa telefonsiz — shunchaki bir-biringizga qarab gaplashing",
            'family_activity': "Uzoq vaqtdan beri tatib ko'rmoqchi bo'lgan taomni birga pishiring",
            'romantic_idea': "Turmush o'rtoqingizga u bilan birga bo'lishdan mamnunligingizning uch sababini yozib bering",
        },
        {
            'question_of_day': "Ertaga kuningizni yaxshilash uchun siz uchun nima qila olaman?",
            'conversation_topic': "Birinchi uchrashuvingiz har biringiz nuqtai nazaridan qanday edi?",
            'trust_exercise': "Kamdan-kam ovoz chiqarib aytadigan bir orzuingizni ulashing",
            'communication_exercise': "Faol tinglash: 10 daqiqa — biri gapiradi, ikkinchisi maslahat bermay faqat tinglaydi",
            'family_activity': "Munosabatingiz boshidan qolgan fotosuratlarni birga tomosha qiling",
            'romantic_idea': "Hoziroq 20 soniya bir-biringizni quchoqlang",
        },
    ],
    'uz_cyrl': [
        {
            'question_of_day': "Бугун сизни нима бахтли қилди — ҳатто энг кичик нарса ҳам?",
            'conversation_topic': "Бир-биringizga энг севимли умумий хотирангиз ҳақида гапириб беринг",
            'trust_exercise': "Турмуш ўртоғингизга қўрқадиган, лекин унга ишониб айтадиган бир нарсангизни айтинг",
            'communication_exercise': "5 дақиқа телефонсиз — шунчаки бир-биringizga қараб гаплашинг",
            'family_activity': "Узоқ вақтдан бери татиб кўрмоқчи бўлган таомни бирга пиширинг",
            'romantic_idea': "Турмуш ўртоғингизга у билан бирга бўлишдан мамнунлигингизнинг уч сабабини ёзиб беринг",
        },
        {
            'question_of_day': "Эртага куningizni яхшилаш учун сиз учун нима қила оламан?",
            'conversation_topic': "Биринчи учрашувингиз ҳар биringiz нуқтаи назаридан қандай эди?",
            'trust_exercise': "Камдан-кам овоз чиқариб айтадиган бир орзуingizni улашинг",
            'communication_exercise': "Фаол тинглаш: 10 дақиқа — бири гапиради, иккинчиси маслаҳат бермай фақат тинглайди",
            'family_activity': "Муносабатингиз бошидан қолган фотосуратларни бирга томоша қилинг",
            'romantic_idea': "Ҳозироқ 20 сония бир-биringizni қучоқланг",
        },
    ],
}


class DailyPracticeService:
    @staticmethod
    def get_today(user: User, language: str = 'ru') -> DailyPractice | None:
        couple = CoupleRepository.get_active_for_user(user)
        if not couple:
            raise BusinessLogicError('NO_COUPLE', 'Нет активной пары')
        today = date.today()
        practice = DailyPractice.objects.filter(couple=couple, date=today).first()
        if not practice:
            practice = DailyPracticeService.generate_for_couple(couple, today)
        return practice

    @staticmethod
    def generate_for_couple(couple, target_date: date) -> DailyPractice:
        try:
            return DailyPracticeService._generate_ai(couple, target_date)
        except Exception as e:
            logger.warning(f"AI practice generation failed, using default: {e}")
            return DailyPracticeService._generate_default(couple, target_date)

    @staticmethod
    def _generate_ai(couple, target_date: date) -> DailyPractice:
        from apps.ai_consultant.providers import AIProviderFactory

        name_a = couple.partner_a.first_name
        name_b = couple.partner_b.first_name if couple.partner_b else 'партнёр'

        context = ""
        from apps.analytics.repositories import AnalyticsRepository
        result = AnalyticsRepository.get_latest_for_couple(couple)
        if result:
            from apps.analytics.services import AnalyticsService
            zones = AnalyticsService.get_zone_detail_for_result(result)
            attention = [z['label'] for z in zones if z['status'] == 'attention']
            if attention:
                context = f"\nФокус на зонах: {', '.join(attention[:2])}"

        prompt = f"""Создай ежедневные семейные практики для пары {name_a} и {name_b} на {target_date.strftime('%d.%m.%Y')}.{context}

Практики должны быть тёплыми, конкретными, реалистичными (занять не больше 20 минут).

Верни JSON со всеми 4 языками:
{{
  "ru": {{
    "question_of_day": "Вопрос для глубокого разговора",
    "conversation_topic": "Тема для разговора",
    "trust_exercise": "Упражнение на доверие (конкретное действие)",
    "communication_exercise": "Упражнение на коммуникацию (конкретное действие)",
    "family_activity": "Семейная активность (что делать вместе)",
    "romantic_idea": "Романтическая идея (небольшой жест)"
  }},
  "en": {{ ... то же самое на английском ... }},
  "uz": {{ ... то же самое на узбекском латиницей ... }},
  "uz_cyrl": {{ ... то же самое на узбекском кириллицей ... }}
}}"""

        provider = AIProviderFactory.get()
        response = provider.complete([
            {'role': 'system', 'content': 'Верни только валидный JSON с ключами ru, en, uz, uz_cyrl.'},
            {'role': 'user', 'content': prompt},
        ])
        start, end = response.find('{'), response.rfind('}') + 1
        if start < 0 or end <= start:
            raise ValueError('Invalid JSON response')

        data = json.loads(response[start:end])
        ru_data = data.get('ru', {})

        return DailyPractice.objects.create(
            couple=couple,
            date=target_date,
            is_ai_generated=True,
            i18n={lang: data[lang] for lang in ('en', 'uz', 'uz_cyrl') if lang in data},
            **{k: ru_data.get(k, '') for k in PRACTICE_FIELDS}
        )

    @staticmethod
    def _generate_default(couple, target_date: date) -> DailyPractice:
        idx = target_date.toordinal() % len(DEFAULT_PRACTICES['ru'])
        ru_data = DEFAULT_PRACTICES['ru'][idx]
        i18n_data = {
            lang: DEFAULT_PRACTICES[lang][idx]
            for lang in ('en', 'uz', 'uz_cyrl')
        }
        practice, _ = DailyPractice.objects.get_or_create(
            couple=couple, date=target_date,
            defaults={**ru_data, 'is_ai_generated': False, 'i18n': i18n_data}
        )
        return practice

    @staticmethod
    def mark_complete(user: User, practice: DailyPractice, field_name: str) -> None:
        allowed = set(PRACTICE_FIELDS)
        if field_name not in allowed:
            raise BusinessLogicError('INVALID_FIELD', 'Неверное поле практики')
        PracticeCompletion.objects.get_or_create(practice=practice, user=user, field_name=field_name)

    @staticmethod
    def get_completions(user: User, practice: DailyPractice) -> set:
        return set(
            PracticeCompletion.objects.filter(practice=practice, user=user).values_list('field_name', flat=True)
        )
