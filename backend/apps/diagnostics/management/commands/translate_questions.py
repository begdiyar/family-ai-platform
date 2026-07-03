from django.core.management.base import BaseCommand
from apps.diagnostics.models import Question

# Translations keyed by (level_number, order_index)
TRANSLATIONS = {
    # ── Level 1 ────────────────────────────────────────────────────────────────
    (1, 1): {
        'en': 'How satisfied are you overall with the way you communicate with your partner?',
        'uz': 'Umuman olganda, sherigingiz bilan qanday muloqot qilishingizdan qanchalik mamnunsiz?',
    },
    (1, 2): {
        'en': 'How much do you trust your partner on important life matters?',
        'uz': 'Muhim hayotiy masalalarda sherigingizga qanchalik ishonasiz?',
    },
    (1, 3): {
        'en': 'How emotionally close do you feel to your partner right now?',
        'uz': 'Hozirgi vaqtda sherigingizga qanchalik hissiy yaqinlik his qilasiz?',
    },
    (1, 4): {
        'en': 'How often do you and your partner find a solution after a conflict?',
        'uz': 'Siz va sherigingiz ziddiyatdan keyin qanchalik tez-tez yechim topasiz?',
    },
    (1, 5): {
        'en': 'How much do your life values align with your partner\'s?',
        'uz': 'Sizning hayotiy qadriyatlaringiz sherigingizning qadriyatlari bilan qanchalik mos keladi?',
    },
    (1, 6): {
        'en': 'How confident are you in the future of your relationship?',
        'uz': 'Munosabatlaringizning kelajagiga qanchalik ishonchli qaraysiz?',
    },
    (1, 7): {
        'en': 'How much do you feel heard and understood by your partner?',
        'uz': 'Sherigingiz sizni qanchalik eshitadi va tushunadi deb his qilasiz?',
    },
    (1, 8): {
        'en': 'How satisfied are you with your relationship overall right now?',
        'uz': 'Hozir umuman munosabatlaringizdan qanchalik mamnunsiz?',
    },
    # ── Level 2 ────────────────────────────────────────────────────────────────
    (2, 1): {
        'en': 'How easy is it for you to start a difficult conversation with your partner?',
        'uz': 'Sherigingiz bilan qiyin suhbatni boshlash siz uchun qanchalik oson?',
    },
    (2, 2): {
        'en': 'How often do you listen attentively to your partner without interrupting?',
        'uz': 'Sherigingizni bo\'lmasdan diqqat bilan qanchalik tez-tez tinglaysiz?',
    },
    (2, 3): {
        'en': 'How openly do you share your thoughts and feelings with your partner?',
        'uz': 'O\'z fikr va his-tuyg\'ularingizni sherigingiz bilan qanchalik ochiq ulashaysiz?',
    },
    (2, 4): {
        'en': 'How often do you and your partner discuss problems instead of staying silent?',
        'uz': 'Siz va sherigingiz muammolarni nechog\'lik muhokama qilasiz, jimib qolmaysiz?',
    },
    (2, 5): {
        'en': 'How well does your partner understand you without extra explanation?',
        'uz': 'Sherigingiz sizni qo\'shimcha tushuntirmasdan qanchalik tushunadi?',
    },
    (2, 6): {
        'en': 'How much do you feel your opinions and views are respected by your partner?',
        'uz': 'Sherigingiz sizning fikr va qarashlaringizni qanchalik hurmat qiladi deb his qilasiz?',
    },
    # ── Level 3 ────────────────────────────────────────────────────────────────
    (3, 1): {
        'en': 'How confident are you in your partner\'s honesty toward you?',
        'uz': 'Sherigingizning sizga nisbatan halolligiga qanchalik ishonasiz?',
    },
    (3, 2): {
        'en': 'How safe do you feel around your partner?',
        'uz': 'Sherigingiz yonida o\'zingizni qanchalik xavfsiz his qilasiz?',
    },
    (3, 3): {
        'en': 'How often does your partner keep the promises they make to you?',
        'uz': 'Sherigingiz sizga bergan va\'dalarini qanchalik tez-tez bajaradi?',
    },
    (3, 4): {
        'en': 'How much can you be yourself — without masks or fear of judgment — around your partner?',
        'uz': 'Sherigingiz oldida niqobsiz va hukm qilinish qo\'rquvisiz o\'zingiz bo\'la olasizmi?',
    },
    (3, 5): {
        'en': 'How much do you trust your partner\'s decisions in situations where you\'re not present?',
        'uz': 'O\'zingiz bo\'lmaganingizda sherigingizning qarorlariga qanchalik ishonasiz?',
    },
    (3, 6): {
        'en': 'How confident are you that your partner won\'t betray you in a difficult moment?',
        'uz': 'Qiyin lahzada sherigingiz sizni xiyonat qilmasligiga qanchalik ishonasiz?',
    },
    # ── Level 4 ────────────────────────────────────────────────────────────────
    (4, 1): {
        'en': 'How well does your partner understand your emotions and inner experiences?',
        'uz': 'Sherigingiz sizning his-tuyg\'ularingiz va ichki kechinmalaringizni qanchalik yaxshi tushunadi?',
    },
    (4, 2): {
        'en': 'How often does your partner support you in difficult moments without judgment?',
        'uz': 'Sherigingiz qiyin paytlarda sizni hukmsiz qanchalik tez-tez qo\'llab-quvvatlaydi?',
    },
    (4, 3): {
        'en': 'How much do you feel your partner accepts you for who you are?',
        'uz': 'Sherigingiz sizni borligicha qabul qiladi deb qanchalik his qilasiz?',
    },
    (4, 4): {
        'en': 'How often do you share your most personal things — fears, dreams, vulnerabilities — with your partner?',
        'uz': 'Eng shaxsiy narsalar — qo\'rquvlar, orzular, zaifliklarni — sherigingiz bilan qanchalik tez-tez ulashaysiz?',
    },
    (4, 5): {
        'en': 'How much do you feel that you and your partner are one team?',
        'uz': 'Siz va sherigingiz bitta jamoa ekanligini qanchalik his qilasiz?',
    },
    (4, 6): {
        'en': 'How much do you feel your partner genuinely cares about your well-being?',
        'uz': 'Sherigingiz sizning farovonligingiz haqida chin dildan qayg\'uradi deb qanchalik his qilasiz?',
    },
    # ── Level 5 ────────────────────────────────────────────────────────────────
    (5, 1): {
        'en': 'How constructively do you and your partner resolve disagreements?',
        'uz': 'Siz va sherigingiz kelishmovchiliklarni qanchalik konstruktiv hal qilasiz?',
    },
    (5, 2): {
        'en': 'How often do conflicts end in reconciliation and understanding?',
        'uz': 'Ziddiyatlar yarashish va tushunish bilan qanchalik tez-tez yakunlanadi?',
    },
    (5, 3): {
        'en': 'How well can you maintain respect for your partner even during an argument?',
        'uz': 'Tortishuvda ham sherigingizga hurmat saqlashni qanchalik uddalaysiz?',
    },
    (5, 4): {
        'en': 'How much do you feel that old grievances don\'t affect your relationship now?',
        'uz': 'Eski ranjishlar hozirgi munosabatlaringizga xalal bermasligi haqida qanchalik his qilasiz?',
    },
    (5, 5): {
        'en': 'How often do you seek a compromise rather than trying to "win"?',
        'uz': '"G\'alaba qilish" o\'rniga kompromis izlashni qanchalik tez-tez qilasiz?',
    },
    (5, 6): {
        'en': 'How quickly do you restore your relationship after a fight?',
        'uz': 'Janjaldan keyin munosabatlaringizni qanchalik tez tiklaysiz?',
    },
    # ── Level 6 ────────────────────────────────────────────────────────────────
    (6, 1): {
        'en': 'How often do you make romantic surprises or thoughtful gestures for your partner?',
        'uz': 'Sherigingizga qanchalik tez-tez romantik kutilmagan sovg\'alar yoki e\'tibor ko\'rsatasiz?',
    },
    (6, 2): {
        'en': 'How much do you feel your partner values romance and tenderness in the relationship?',
        'uz': 'Sherigingiz munosabatda romantika va mehribonlikni qadrlaydi deb qanchalik his qilasiz?',
    },
    (6, 3): {
        'en': 'How often do you spend time together — without children, phones, or routine?',
        'uz': 'Bolalar, telefonlar va kundalik hayotsiz ikkovingiz qanchalik tez-tez vaqt o\'tkazasiz?',
    },
    (6, 4): {
        'en': 'How satisfied are you with physical intimacy in your relationship?',
        'uz': 'Munosabatingizdagi jismoniy yaqinlikdan qanchalik mamnunsiz?',
    },
    (6, 5): {
        'en': 'How often does your partner show tenderness and affection without a special reason?',
        'uz': 'Sherigingiz maxsus sababsiz qanchalik tez-tez mehrini ko\'rsatadi?',
    },
    (6, 6): {
        'en': 'How much do you feel the attraction and romance between you is still alive?',
        'uz': 'Sizlar orasidagi tortishish va romantika saqlanib qolayotganini qanchalik his qilasiz?',
    },
    # ── Level 7 ────────────────────────────────────────────────────────────────
    (7, 1): {
        'en': 'How satisfied are you with how financial decisions are made in your family?',
        'uz': 'Oilangizda moliyaviy qarorlar qanday qabul qilinishidan qanchalik mamnunsiz?',
    },
    (7, 2): {
        'en': 'How often do you and your partner openly discuss the family budget and expenses?',
        'uz': 'Siz va sherigingiz oilaviy byudjet va xarajatlar haqida qanchalik ochiq gaplashasiz?',
    },
    (7, 3): {
        'en': 'How much do your views on spending, saving, and financial priorities align?',
        'uz': 'Xarajatlar, jamg\'arma va moliyaviy ustuvorliklar bo\'yicha qarashlaringiz qanchalik mos keladi?',
    },
    (7, 4): {
        'en': 'How much do you feel there is financial transparency and honesty between you?',
        'uz': 'Sizlar orasida moliyaviy shaffoflik va halollik borligini qanchalik his qilasiz?',
    },
    (7, 5): {
        'en': 'How confident are you in your family\'s financial stability in the future?',
        'uz': 'Oilangizning kelajakdagi moliyaviy barqarorligiga qanchalik ishonasiz?',
    },
    (7, 6): {
        'en': 'How rarely do financial disagreements become a source of serious conflict?',
        'uz': 'Moliyaviy kelishmovchiliklar jiddiy ziddiyat manbaiga qanchalik kam aylanadi?',
    },
    # ── Level 8 ────────────────────────────────────────────────────────────────
    (8, 1): {
        'en': 'How much does your partner help you maintain healthy boundaries with your relatives?',
        'uz': 'Sherigingiz qarindoshlaringiz bilan sog\'lom chegara saqlashga qanchalik yordam beradi?',
    },
    (8, 2): {
        'en': 'How rarely does relatives\' interference create tension between you?',
        'uz': 'Qarindoshlarning aralashuvi sizlar orasida taranglikni qanchalik kam keltirib chiqaradi?',
    },
    (8, 3): {
        'en': 'How united are you and your partner on matters involving your families?',
        'uz': 'Oilalaringizga oid masalalarda siz va sherigingiz qanchalik fikrdosh?',
    },
    (8, 4): {
        'en': 'How comfortable do you feel in your relationship with your partner\'s family?',
        'uz': 'Sherigingizning oilasi bilan munosabatda o\'zingizni qanchalik qulay his qilasiz?',
    },
    (8, 5): {
        'en': 'How much does your couple feel like an independent unit — not dependent on relatives\' opinions?',
        'uz': 'Juftliginiz qarindoshlar fikriga bog\'liq bo\'lmagan mustaqil bir bo\'lak ekanligini qanchalik his qilasiz?',
    },
    (8, 6): {
        'en': 'How often do you and your partner discuss and set boundaries for relatives?',
        'uz': 'Siz va sherigingiz qarindoshlar uchun chegara belgilashni qanchalik tez-tez muhokama qilasiz?',
    },
    # ── Level 9 ────────────────────────────────────────────────────────────────
    (9, 1): {
        'en': 'How much do you and your partner agree on approaches to raising children?',
        'uz': 'Bolalarni tarbiyalash yondashuvlarida siz va sherigingiz qanchalik kelishasiz?',
    },
    (9, 2): {
        'en': 'How do you rate the distribution of parental responsibilities between you?',
        'uz': 'Sizlar orasidagi ota-onalik vazifalarining taqsimlanishini qanday baholaysiz?',
    },
    (9, 3): {
        'en': 'How much do you feel children see a model of a healthy relationship in your family?',
        'uz': 'Bolalar oilada sog\'lom munosabatlar namunasini ko\'radi deb qanchalik his qilasiz?',
    },
    (9, 4): {
        'en': 'How often do you and your partner openly discuss questions related to children?',
        'uz': 'Siz va sherigingiz bolalarga oid masalalarni qanchalik tez-tez ochiq muhokama qilasiz?',
    },
    (9, 5): {
        'en': 'How satisfied are you with the atmosphere at home — warmth, safety, joy?',
        'uz': 'Uyda muhitdan — iliqlik, xavfsizlik, quvonchdan — qanchalik mamnunsiz?',
    },
    (9, 6): {
        'en': 'How smoothly do you work as a team in your role as parents?',
        'uz': 'Ota-ona sifatida ikkovingiz jamoa bo\'lib qanchalik uyg\'un ishlaysiz?',
    },
    # ── Level 10 ───────────────────────────────────────────────────────────────
    (10, 1): {
        'en': 'How clearly do you envision your family\'s shared future?',
        'uz': 'Oilangizning umumiy kelajagini qanchalik aniq tasavvur qilasiz?',
    },
    (10, 2): {
        'en': 'How well do your long-term goals and dreams align with your partner\'s?',
        'uz': 'Uzoq muddatli maqsad va orzularingiz sherigingiznikiga qanchalik mos keladi?',
    },
    (10, 3): {
        'en': 'How often do you and your partner talk about dreams, plans, and what you want to achieve?',
        'uz': 'Siz va sherigingiz orzular, rejalar va erishmoqchi bo\'lgan narsalar haqida qanchalik tez-tez gaplashasiz?',
    },
    (10, 4): {
        'en': 'How much do you feel unity in key life values — family, career, health?',
        'uz': 'Asosiy hayotiy qadriyatlarda — oila, martaba, sog\'liq — birlikni qanchalik his qilasiz?',
    },
    (10, 5): {
        'en': 'How confident are you that you and your partner are moving in the same direction?',
        'uz': 'Siz va sherigingiz bir yo\'nalishda harakatlanayotganiga qanchalik ishonasiz?',
    },
    (10, 6): {
        'en': 'How much do you feel your family continues to grow and develop?',
        'uz': 'Oilangiz rivojlanib va o\'sib borayotganini qanchalik his qilasiz?',
    },
}


class Command(BaseCommand):
    help = 'Populate i18n translations for all diagnostic questions'

    def handle(self, *args, **options):
        updated = 0
        skipped = 0

        for (level, order), langs in TRANSLATIONS.items():
            i18n_value = {lang: {'text': text} for lang, text in langs.items()}
            qs = Question.objects.filter(level_number=level, order_index=order)
            count = qs.count()
            if count == 0:
                self.stdout.write(self.style.WARNING(
                    f'Question not found: level={level}, order={order}'
                ))
                skipped += 1
            else:
                for q in qs:
                    q.i18n = i18n_value
                    q.save(update_fields=['i18n'])
                updated += count

        self.stdout.write(self.style.SUCCESS(
            f'Done: {updated} questions translated, {skipped} skipped'
        ))
