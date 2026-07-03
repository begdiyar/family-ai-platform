from django.core.management.base import BaseCommand
from apps.practices.models import Practice


RITUAL_TRANSLATIONS = {
    'Утренний вопрос дня': {
        'en': {
            'title': 'Morning Question of the Day',
            'description': 'Start the day with a simple question that brings you closer.',
        },
        'uz': {
            'title': 'Kunning ertalabki savoli',
            'description': 'Kunni sizlarni yaqinlashtiruvchi oddiy savol bilan boshlang.',
        },
    },
    'Вечерняя благодарность': {
        'en': {
            'title': 'Evening Gratitude',
            'description': 'Share one thing you are grateful for about your partner today.',
        },
        'uz': {
            'title': 'Kechki minnatdorlik',
            'description': 'Bugun sheringingiz haqida minnatdor ekanligingiz bir narsani ayting.',
        },
    },
    'Совместный чай без телефонов': {
        'en': {
            'title': 'Tea Time Without Phones',
            'description': 'Have tea or coffee together with phones put away. Talk about anything or simply enjoy the silence together.',
        },
        'uz': {
            'title': 'Telefonsiz birgalikdagi choy',
            'description': 'Telefonlarni chetga qoyib, birgalikda choy yoki kofe iching. Istalgan narsa haqida gaplashing yoki shunchaki jim turing.',
        },
    },
    'Прощальный поцелуй': {
        'en': {
            'title': 'Farewell Kiss',
            'description': 'Kiss your partner every time you part, even briefly. A small gesture that says: you matter to me.',
        },
        'uz': {
            'title': 'Xayrlashuv opichi',
            'description': 'Har safar xayrlashayotganingizda sheringizni opayting. Kichik imo: siz men uchun muhimsiz.',
        },
    },
    'Три слова перед сном': {
        'en': {
            'title': 'Three Words Before Sleep',
            'description': 'Before falling asleep, say three words that describe how you feel about your partner today.',
        },
        'uz': {
            'title': 'Uxlashdan oldin uch soz',
            'description': 'Uxlashdan oldin, bugun sheringingiz haqida his qilgan uch sozni ayting.',
        },
    },
    'Утреннее объятие': {
        'en': {
            'title': 'Morning Hug',
            'description': 'Hug your partner for at least 20 seconds every morning. This simple ritual reduces stress and strengthens your bond.',
        },
        'uz': {
            'title': 'Ertalabki quchoqlashuv',
            'description': 'Har ertalab sheringizni kamida 20 soniya quchoqlang. Bu oddiy ritual stressni kamaytiradi va rishta mustahkamlaydi.',
        },
    },
}


class Command(BaseCommand):
    help = 'Add missing i18n translations for ritual practices.'

    def handle(self, *args, **options):
        updated = 0
        for title, i18n in RITUAL_TRANSLATIONS.items():
            try:
                p = Practice.objects.get(title=title, slot_type='ritual')
                p.i18n = i18n
                p.save(update_fields=['i18n'])
                updated += 1
                self.stdout.write(f'  OK: {title}')
            except Practice.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'  NOT FOUND: {title}'))

        self.stdout.write(self.style.SUCCESS(f'Done. Updated {updated} practices.'))
