from django.core.management.base import BaseCommand
from apps.diagnostics.models import Question

QUESTIONS = [
    # ── Level 1: Основа отношений (zone разнообразен — baseline по всем зонам) ──
    dict(level_number=1, zone='communication', order_index=1, question_type='scale',
         text='Насколько вы в целом довольны тем, как вы общаетесь с партнёром?'),
    dict(level_number=1, zone='trust', order_index=2, question_type='scale',
         text='Насколько вы доверяете своему партнёру в важных жизненных вопросах?'),
    dict(level_number=1, zone='intimacy', order_index=3, question_type='scale',
         text='Насколько вы чувствуете эмоциональную близость с партнёром прямо сейчас?'),
    dict(level_number=1, zone='conflict', order_index=4, question_type='scale',
         text='Как часто вы с партнёром находите решение после конфликта?'),
    dict(level_number=1, zone='values', order_index=5, question_type='scale',
         text='Насколько ваши жизненные ценности совпадают с ценностями партнёра?'),
    dict(level_number=1, zone='future', order_index=6, question_type='scale',
         text='Насколько вы уверены в будущем ваших отношений?'),
    dict(level_number=1, zone='communication', order_index=7, question_type='scale',
         text='Насколько вы чувствуете себя услышанным и понятым партнёром?'),
    dict(level_number=1, zone='intimacy', order_index=8, question_type='scale',
         text='Насколько вы удовлетворены своими отношениями в целом прямо сейчас?'),

    # ── Level 2: Коммуникация ─────────────────────────────────────────────────
    dict(level_number=2, zone='communication', order_index=1, question_type='scale',
         text='Насколько легко вам начать сложный разговор с партнёром?'),
    dict(level_number=2, zone='communication', order_index=2, question_type='scale',
         text='Как часто вы внимательно слушаете партнёра, не перебивая?'),
    dict(level_number=2, zone='communication', order_index=3, question_type='scale',
         text='Насколько открыто вы делитесь своими мыслями и чувствами с партнёром?'),
    dict(level_number=2, zone='communication', order_index=4, question_type='scale',
         text='Как часто вы с партнёром обсуждаете проблемы, а не замалчиваете их?'),
    dict(level_number=2, zone='communication', order_index=5, question_type='scale',
         text='Насколько хорошо партнёр понимает вас без лишних объяснений?'),
    dict(level_number=2, zone='communication', order_index=6, question_type='scale',
         text='Насколько вы чувствуете, что ваши мнения и взгляды уважаются партнёром?'),

    # ── Level 3: Доверие ──────────────────────────────────────────────────────
    dict(level_number=3, zone='trust', order_index=1, question_type='scale',
         text='Насколько вы уверены в честности партнёра по отношению к вам?'),
    dict(level_number=3, zone='trust', order_index=2, question_type='scale',
         text='Насколько вы чувствуете себя в безопасности рядом с партнёром?'),
    dict(level_number=3, zone='trust', order_index=3, question_type='scale',
         text='Как часто партнёр выполняет данные вам обещания?'),
    dict(level_number=3, zone='trust', order_index=4, question_type='scale',
         text='Насколько вы можете быть собой — без масок и страха осуждения — рядом с партнёром?'),
    dict(level_number=3, zone='trust', order_index=5, question_type='scale',
         text='Насколько вы доверяете решениям партнёра в ситуациях, где вы не присутствуете?'),
    dict(level_number=3, zone='trust', order_index=6, question_type='scale',
         text='Насколько вы уверены, что партнёр не предаст вас в трудный момент?'),

    # ── Level 4: Эмоциональная близость ──────────────────────────────────────
    dict(level_number=4, zone='intimacy', order_index=1, question_type='scale',
         text='Насколько хорошо партнёр понимает ваши эмоции и внутренние переживания?'),
    dict(level_number=4, zone='intimacy', order_index=2, question_type='scale',
         text='Как часто партнёр поддерживает вас в трудные моменты без осуждения?'),
    dict(level_number=4, zone='intimacy', order_index=3, question_type='scale',
         text='Насколько вы чувствуете, что партнёр принимает вас таким(ой), какой вы есть?'),
    dict(level_number=4, zone='intimacy', order_index=4, question_type='scale',
         text='Как часто вы делитесь с партнёром самым личным — страхами, мечтами, уязвимостью?'),
    dict(level_number=4, zone='intimacy', order_index=5, question_type='scale',
         text='Насколько вы чувствуете, что вы и партнёр — одна команда?'),
    dict(level_number=4, zone='intimacy', order_index=6, question_type='scale',
         text='Насколько вы чувствуете, что партнёр искренне заботится о вашем благополучии?'),

    # ── Level 5: Конфликты ────────────────────────────────────────────────────
    dict(level_number=5, zone='conflict', order_index=1, question_type='scale',
         text='Насколько конструктивно вы с партнёром разрешаете разногласия?'),
    dict(level_number=5, zone='conflict', order_index=2, question_type='scale',
         text='Как часто конфликты у вас завершаются примирением и пониманием?'),
    dict(level_number=5, zone='conflict', order_index=3, question_type='scale',
         text='Насколько вы умеете сохранять уважение к партнёру даже в споре?'),
    dict(level_number=5, zone='conflict', order_index=4, question_type='scale',
         text='Насколько вы чувствуете, что старые обиды не мешают вашим отношениям сейчас?'),
    dict(level_number=5, zone='conflict', order_index=5, question_type='scale',
         text='Как часто вы с партнёром ищете компромисс, а не стремитесь «победить»?'),
    dict(level_number=5, zone='conflict', order_index=6, question_type='scale',
         text='Насколько быстро вы восстанавливаете отношения после ссоры?'),

    # ── Level 6: Романтика (zone=intimacy) ───────────────────────────────────
    dict(level_number=6, zone='intimacy', order_index=1, question_type='scale',
         text='Как часто вы делаете романтические сюрпризы или жесты внимания партнёру?'),
    dict(level_number=6, zone='intimacy', order_index=2, question_type='scale',
         text='Насколько вы чувствуете, что партнёр ценит романтику и нежность в отношениях?'),
    dict(level_number=6, zone='intimacy', order_index=3, question_type='scale',
         text='Как часто вы проводите время вдвоём — без детей, телефонов и рутины?'),
    dict(level_number=6, zone='intimacy', order_index=4, question_type='scale',
         text='Насколько вы удовлетворены физической близостью в ваших отношениях?'),
    dict(level_number=6, zone='intimacy', order_index=5, question_type='scale',
         text='Как часто партнёр проявляет нежность и ласку без особого повода?'),
    dict(level_number=6, zone='intimacy', order_index=6, question_type='scale',
         text='Насколько вы чувствуете, что притяжение и романтика между вами сохраняются?'),

    # ── Level 7: Финансы (zone=finance) ──────────────────────────────────────
    dict(level_number=7, zone='finance', order_index=1, question_type='scale',
         text='Насколько вы довольны тем, как в вашей семье принимаются финансовые решения?'),
    dict(level_number=7, zone='finance', order_index=2, question_type='scale',
         text='Как часто вы с партнёром открыто обсуждаете семейный бюджет и расходы?'),
    dict(level_number=7, zone='finance', order_index=3, question_type='scale',
         text='Насколько ваши взгляды на траты, накопления и финансовые приоритеты совпадают?'),
    dict(level_number=7, zone='finance', order_index=4, question_type='scale',
         text='Насколько вы чувствуете финансовую прозрачность и честность между вами?'),
    dict(level_number=7, zone='finance', order_index=5, question_type='scale',
         text='Насколько вы уверены в финансовой стабильности вашей семьи в будущем?'),
    dict(level_number=7, zone='finance', order_index=6, question_type='scale',
         text='Насколько редко финансовые разногласия становятся источником серьёзных конфликтов?'),

    # ── Level 8: Родственники (zone=relatives) ────────────────────────────────
    dict(level_number=8, zone='relatives', order_index=1, question_type='scale',
         text='Насколько партнёр помогает вам сохранять здоровые границы с вашими родственниками?'),
    dict(level_number=8, zone='relatives', order_index=2, question_type='scale',
         text='Как редко вмешательство родных создаёт напряжение между вами?'),
    dict(level_number=8, zone='relatives', order_index=3, question_type='scale',
         text='Насколько вы с партнёром единодушны в вопросах, касающихся ваших семей?'),
    dict(level_number=8, zone='relatives', order_index=4, question_type='scale',
         text='Насколько комфортно вы себя чувствуете в отношениях с семьёй партнёра?'),
    dict(level_number=8, zone='relatives', order_index=5, question_type='scale',
         text='Насколько ваша пара чувствует себя самостоятельной ячейкой — не зависимой от мнения родных?'),
    dict(level_number=8, zone='relatives', order_index=6, question_type='scale',
         text='Как часто вы вместе с партнёром обсуждаете и устанавливаете границы для родственников?'),

    # ── Level 9: Дети (zone=future) ──────────────────────────────────────────
    dict(level_number=9, zone='future', order_index=1, question_type='scale',
         text='Насколько вы согласны с партнёром в подходах к воспитанию детей?'),
    dict(level_number=9, zone='future', order_index=2, question_type='scale',
         text='Как вы оцениваете распределение родительских обязанностей между вами?'),
    dict(level_number=9, zone='future', order_index=3, question_type='scale',
         text='Насколько вы чувствуете, что дети видят в семье пример здоровых отношений?'),
    dict(level_number=9, zone='future', order_index=4, question_type='scale',
         text='Как часто вы с партнёром открыто обсуждаете вопросы, связанные с детьми?'),
    dict(level_number=9, zone='future', order_index=5, question_type='scale',
         text='Насколько вы удовлетворены атмосферой в семье — теплотой, безопасностью, радостью?'),
    dict(level_number=9, zone='future', order_index=6, question_type='scale',
         text='Насколько слаженно вы работаете как команда в роли родителей?'),

    # ── Level 10: Будущее семьи (zone=future + values) ────────────────────────
    dict(level_number=10, zone='future', order_index=1, question_type='scale',
         text='Насколько ясно вы представляете общее будущее вашей семьи?'),
    dict(level_number=10, zone='future', order_index=2, question_type='scale',
         text='Насколько ваши долгосрочные цели и мечты совпадают с целями партнёра?'),
    dict(level_number=10, zone='future', order_index=3, question_type='scale',
         text='Как часто вы с партнёром говорите о мечтах, планах и том, чего хотите достичь?'),
    dict(level_number=10, zone='values', order_index=4, question_type='scale',
         text='Насколько вы чувствуете единство в ключевых жизненных ценностях — семья, карьера, здоровье?'),
    dict(level_number=10, zone='values', order_index=5, question_type='scale',
         text='Насколько вы уверены, что вы и партнёр движетесь в одном направлении?'),
    dict(level_number=10, zone='future', order_index=6, question_type='scale',
         text='Насколько вы ощущаете, что ваша семья продолжает развиваться и расти?'),
]


class Command(BaseCommand):
    help = 'Seed diagnostic questions for all 10 levels'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Delete existing questions before seeding',
        )

    def handle(self, *args, **options):
        if options['reset']:
            deleted, _ = Question.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {deleted} existing questions'))

        created = 0
        updated = 0
        for q in QUESTIONS:
            obj, was_created = Question.objects.update_or_create(
                level_number=q['level_number'],
                zone=q['zone'],
                order_index=q['order_index'],
                defaults={
                    'text': q['text'],
                    'question_type': q.get('question_type', 'scale'),
                    'options': q.get('options'),
                    'is_active': True,
                },
            )
            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done: {created} created, {updated} updated. Total questions: {len(QUESTIONS)}'
        ))

        # Показываем сводку по уровням
        from django.db.models import Count
        for row in (
            Question.objects.values('level_number')
            .annotate(count=Count('id'))
            .order_by('level_number')
        ):
            self.stdout.write(f"  Level {row['level_number']}: {row['count']} questions")
