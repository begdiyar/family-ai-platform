"""
python manage.py seed_academy

Заполняет базу данных начальным контентом Семейной Академии:
- Источники (исследователи, организации)
- Статьи (14 категорий × 3-4 статьи)
- Тренировки (7 навыков)
- Программы развития (7/14/21/30 дней) с днями
- Микро-практики
- Достижения
"""
from django.core.management.base import BaseCommand
from apps.academy.models import (
    ArticleSource, Article, Training, Program, ProgramDay,
    AcademyMicroPractice, Achievement,
)


SOURCES = [
    {'name': 'Джон Готтман', 'source_type': 'researcher', 'trust_level': 'high', 'url': 'https://gottman.com'},
    {'name': 'Джули Готтман', 'source_type': 'researcher', 'trust_level': 'high'},
    {'name': 'Сью Джонсон', 'source_type': 'researcher', 'trust_level': 'high'},
    {'name': 'Гэри Чепмен', 'source_type': 'researcher', 'trust_level': 'high'},
    {'name': 'APA (American Psychological Association)', 'source_type': 'organization', 'trust_level': 'high', 'url': 'https://apa.org'},
    {'name': 'NIH (National Institutes of Health)', 'source_type': 'organization', 'trust_level': 'high', 'url': 'https://nih.gov'},
    {'name': 'Journal of Marriage and Family', 'source_type': 'journal', 'trust_level': 'high'},
    {'name': 'Харвилл Хендрикс', 'source_type': 'researcher', 'trust_level': 'high'},
]

ARTICLES = [
    # --- Общение ---
    {
        'slug': 'active-listening-basics',
        'category': 'communication',
        'title': 'Основы активного слушания в паре',
        'brief': 'Почему большинство конфликтов возникает не из-за разногласий, а из-за того, что партнёр чувствует себя неуслышанным.',
        'body': '''## Что такое активное слушание

Активное слушание — это не молчание, пока партнёр говорит. Это полное присутствие: телесное, эмоциональное и когнитивное.

Исследования Джона Готтмана показывают, что пары, в которых оба партнёра практикуют активное слушание, на 67% реже расходятся.

## Четыре компонента

**1. Телесное присутствие.** Отложите телефон. Повернитесь лицом. Поддерживайте зрительный контакт без давления.

**2. Отражение содержания.** Перефразируйте то, что услышали: «Правильно ли я понял, что ты чувствуешь...»

**3. Отражение эмоций.** Называйте то, что вы видите: «Похоже, это тебя очень расстроило».

**4. Проверка.** Спросите: «Я правильно тебя понял?»

## Чего избегать

- Перебивать, чтобы защититься
- Готовить ответ, пока партнёр ещё говорит
- Давать советы, когда просят просто выслушать
- Обесценивать: «Это не так важно»

## Практика

Попробуйте правило «5 минут»: один говорит без перебиваний, другой только слушает и задаёт уточняющие вопросы. Затем меняетесь.''',
        'i18n': {
            'en': {
                'title': 'The Basics of Active Listening in a Couple',
                'brief': 'Why most conflicts arise not from disagreements, but from a partner feeling unheard.',
                'body': '''## What is active listening

Active listening is not silence while your partner talks. It is full presence: physical, emotional, and cognitive.

Research by John Gottman shows that couples where both partners practice active listening are 67% less likely to split up.

## Four Components

**1. Physical presence.** Put down your phone. Turn to face each other. Maintain eye contact without pressure.

**2. Reflecting content.** Paraphrase what you heard: "Do I understand correctly that you feel..."

**3. Reflecting emotions.** Name what you see: "It seems like this really upset you."

**4. Checking.** Ask: "Did I understand you correctly?"

## What to avoid

- Interrupting to defend yourself
- Preparing your response while your partner is still speaking
- Giving advice when they just want to be heard
- Dismissing: "That's not important"

## Practice

Try the "5-minute rule": one person speaks without interruptions, the other only listens and asks clarifying questions. Then switch.''',
            },
            'uz': {
                'title': "Juftlikda faol tinglashning asoslari",
                'brief': "Nima uchun ko'plab nizolar kelishmovchiliklar tufayli emas, balki sherik o'zini eshitilmagan his qilgani uchun yuzaga keladi.",
                'body': '''## Faol tinglash nima

Faol tinglash — sherik gapirganida jim turish emas. Bu to\'liq hozirlik: jismoniy, hissiy va kognitiv.

Jon Gottmanning tadqiqotlari shuni ko\'rsatadiki, ikkalasi ham faol tinglashni amaliyotga tatbiq etadigan juftliklar 67% kamroq ajrashadi.

## To\'rtta komponent

**1. Jismoniy hozirlik.** Telefonni qo\'ying. Yuzma-yuz o\'tiring. Bosim sezdirilmasdan ko\'z aloqasini saqlang.

**2. Mazmunni aks ettirish.** Eshitganingizni qayta so\'zlang: «To\'g\'ri tushundimmi, siz...ni his qilyapsizmi»

**3. Hissiyotlarni aks ettirish.** Ko\'rganingizni nomlang: «Bu sizni juda xafa qilganday tuyulmoqda».

**4. Tekshirish.** So\'rang: «Men sizni to\'g\'ri tushundimmi?»

## Nima qilmaslik kerak

- O\'zingizni himoya qilish uchun so\'zni bo\'lish
- Sherik gapirganida javob tayyorlash
- Faqat eshitishni so\'raganda maslahat berish
- Kamsitish: «Bu uncha muhim emas»

## Amaliyot

«5 daqiqa» qoidasini sinab ko\'ring: biri to\'xtatilmasdan gapiradi, ikkinchisi faqat tinglaydi va aniqlovchi savollar beradi. Keyin almashing.''',
            },
            'uz_cyrl': {
                'title': 'Жуфтликда фаол тинглашнинг асослари',
                'brief': 'Нима учун кўплаб низолар келишмовчиликлар туфайли эмас, балки шерик ўзини эшитилмаган ҳис қилгани учун юзага келади.',
                'body': '''## Фаол тинглаш нима

Фаол тинглаш — шерик гапирганида жим туриш эмас. Бу тўлиқ ҳозирлик: жисмоний, ҳиссий ва когнитив.

Жон Готтманнинг тадқиқотлари шуни кўрсатадики, иккаласи ҳам фаол тинглашни амалиётга татбиқ этадиган жуфтликлар 67% камроқ ажрашади.

## Тўртта компонент

**1. Жисмоний ҳозирлик.** Телефонни қўйинг. Юзма-юз ўтиринг. Босим сездирилмасдан кўз алоқасини сақланг.

**2. Мазмунни акс эттириш.** Эшитганингизни қайта сўзланг: «Тўғри тушундимми, сиз...ни ҳис қиляпсизми»

**3. Ҳиссиётларни акс эттириш.** Кўрганингизни номланг: «Бу сизни жуда хафа қилгандай туюлмоқда».

**4. Текшириш.** Сўранг: «Мен сизни тўғри тушундимми?»

## Нима қилмаслик керак

- Ўзингизни ҳимоя қилиш учун сўзни бўлиш
- Шерик гапирганида жавоб тайёрлаш
- Фақат эшитишни сўраганда маслаҳат бериш
- Камситиш: «Бу унча муҳим эмас»

## Амалиёт

«5 дақиқа» қоидасини синаб кўринг: бири тўхтатилмасдан гапиради, иккинчиси фақат тинглайди ва аниқловчи саволлар беради. Кейин алмашинг.''',
            },
        },
        'read_time_minutes': 6,
        'difficulty': 'beginner',
        'tags': ['слушание', 'коммуникация', 'эмпатия'],
        'sources': ['Джон Готтман', 'APA (American Psychological Association)'],
        'order_index': 1,
    },
    {
        'slug': 'nonviolent-communication',
        'category': 'communication',
        'title': 'Ненасильственное общение: говорить о нуждах, а не обвинять',
        'brief': 'Метод Маршалла Розенберга, который переводит разговор с уровня претензий на уровень потребностей.',
        'body': '''## Что такое ННО

Ненасильственное общение (ННО) — методология, разработанная психологом Маршаллом Розенбергом. Основана на четырёх шагах.

## Четыре шага ННО

**Наблюдение** (без оценки): «Когда я вижу, что посуда не помыта...»

**Чувство**: «...я чувствую усталость и разочарование...»

**Потребность**: «...потому что для меня важен порядок в доме как способ расслабиться...»

**Просьба** (конкретная и выполнимая): «...не мог бы ты помыть посуду после ужина?»

## Разница между наблюдением и оценкой

| Оценка (триггер конфликта) | Наблюдение (нейтральный факт) |
|---|---|
| «Ты всегда опаздываешь» | «В этот раз ты пришёл на 20 минут позже» |
| «Тебе всё равно» | «Ты не позвонил, когда задержался» |
| «Ты слишком много тратишь» | «В этом месяце расходы превысили бюджет на 15%» |

## Ключевой принцип

Все действия людей — попытка удовлетворить потребность. Конфликт возникает не из-за потребностей (они у всех разные), а из-за стратегий их удовлетворения.''',
        'i18n': {
            'en': {
                'title': 'Nonviolent Communication: Speaking About Needs, Not Blame',
                'brief': "Marshall Rosenberg's method that shifts conversation from accusations to needs.",
                'body': '''## What is NVC

Nonviolent Communication (NVC) is a methodology developed by psychologist Marshall Rosenberg. It is based on four steps.

## The Four Steps of NVC

**Observation** (without evaluation): "When I see that the dishes are not washed..."

**Feeling**: "...I feel tired and disappointed..."

**Need**: "...because order at home is important to me as a way to relax..."

**Request** (specific and actionable): "...could you please wash the dishes after dinner?"

## The Difference Between Observation and Evaluation

| Evaluation (conflict trigger) | Observation (neutral fact) |
|---|---|
| "You are always late" | "This time you arrived 20 minutes late" |
| "You don\'t care" | "You didn\'t call when you were running late" |
| "You spend too much" | "This month spending exceeded budget by 15%" |

## The Key Principle

All human actions are attempts to meet a need. Conflict arises not from needs (everyone has different ones) but from the strategies used to meet them.''',
            },
            'uz': {
                'title': "Zo'rliksiz muloqot: ayblovlar emas, ehtiyojlar haqida gapirish",
                'brief': "Marshall Rosenbergning suhbatni da'volar darajasidan ehtiyojlar darajasiga o'tkazadigan usuli.",
                'body': '''## ZM nima

Zo\'rliksiz muloqot (ZM) — psixolog Marshall Rosenberg tomonidan ishlab chiqilgan metodologiya. To\'rt qadamga asoslanadi.

## ZMning to\'rt qadami

**Kuzatuv** (baholashsiz): «Idishlar yuvulmagan ko\'rganimda...»

**Tuyg\'u**: «...men charchagan va xafaman...»

**Ehtiyoj**: «...chunki uy tartibi men uchun dam olish yo\'li sifatida muhim...»

**So\'rov** (aniq va bajarilishi mumkin): «...kechki ovqatdan keyin idishlarni yuvib qo\'ya olasanmi?»

## Kuzatuv va baholash o\'rtasidagi farq

| Baholash (nizo triggeri) | Kuzatuv (neytral fakt) |
|---|---|
| «Siz har doim kechikasiz» | «Bu safar 20 daqiqa kech keldingiz» |
| «Sizga bari bir» | «Kechikib qolganingizda qo\'ng\'iroq qilmadingiz» |
| «Siz juda ko\'p sarflaysiz» | «Bu oy xarajatlar byudjetdan 15% oshib ketdi» |

## Asosiy tamoyil

Odamlarning barcha harakatlari — ehtiyojlarni qondirish urinishi. Nizo ehtiyojlar tufayli emas (ularning hammasi har xil), balki ularni qondirish strategiyalari tufayli yuzaga keladi.''',
            },
            'uz_cyrl': {
                'title': "Зўрликсиз мулоқот: айбловлар эмас, эҳтиёжлар ҳақида гапириш",
                'brief': "Маршалл Розенбергнинг суҳбатни да'волар даражасидан эҳтиёжлар даражасига ўтказадиган усули.",
                'body': '''## ЗМ нима

Зўрликсиз мулоқот (ЗМ) — психолог Маршалл Розенберг томонидан ишлаб чиқилган методология. Тўрт қадамга асосланади.

## ЗМнинг тўрт қадами

**Кузатув** (баҳолашсиз): «Идишлар юvilмаган кўрганимда...»

**Туйғу**: «...мен чарчаган ва хафаман...»

**Эҳтиёж**: «...чунки уй тартиби мен учун дам олиш йўли сифатида муҳим...»

**Сўров** (аниқ ва бажарилиши мумкин): «...кечки овқатдан кейин идишларни ювиб қўя оласанми?»

## Кузатув ва баҳолаш ўртасидаги фарқ

| Баҳолаш (низо триггери) | Кузатув (нейтрал факт) |
|---|---|
| «Сиз ҳар доим кечикасиз» | «Бу сафар 20 дақиқа кеч келдингиз» |
| «Сизга бари бир» | «Кечикиб қолганингизда қўнғироқ қилмадингиз» |
| «Сиз жуда кўп сарфлайсиз» | «Бу ой харажатлар бюджетдан 15% ошиб кетди» |

## Асосий тамойил

Одамларнинг барча ҳаракатлари — эҳтиёжларни қондириш уриниши. Низо эҳтиёжлар туфайли эмас (уларнинг ҳаммаси ҳар хил), балки уларни қондириш стратегиялари туфайли юзага келади.''',
            },
        },
        'read_time_minutes': 8,
        'difficulty': 'intermediate',
        'tags': ['ненасильственное общение', 'потребности', 'конфликт'],
        'sources': ['APA (American Psychological Association)'],
        'order_index': 2,
    },
    {
        'slug': 'four-horsemen-gottman',
        'category': 'communication',
        'title': '«Четыре всадника» Готтмана: предсказатели развода',
        'brief': 'Джон Готтман определил четыре паттерна общения, которые с точностью 93% предсказывают расставание.',
        'body': '''## Исследование Готтмана

В течение 40 лет Джон Готтман наблюдал тысячи пар в своей «Лаборатории любви». Он обнаружил четыре деструктивных паттерна, которые он назвал «Четырьмя всадниками Апокалипсиса».

## Всадник 1: Критика

**Что это:** Атака на личность, а не на поступок.
- Деструктивно: «Ты такой эгоист, тебе всегда всё равно»
- Конструктивно: «Мне было грустно, что ты не спросил, как мой день»

## Всадник 2: Презрение

**Что это:** Послание «ты хуже меня». Сарказм, насмешки, закатывание глаз.
Готтман называет его самым опасным. Предсказывает не только развод, но и снижение иммунитета у партнёра.

Антидот: культура благодарности и уважения.

## Всадник 3: Защитная реакция

**Что это:** Отрицание ответственности, перекладывание вины.
- «Это не моя проблема, это ты всегда...»

Антидот: принять хотя бы часть ответственности. «Да, в этом есть и моя роль».

## Всадник 4: Блокирование (стоунволлинг)

**Что это:** Эмоциональный уход из разговора — молчание, избегание.
Возникает при физиологическом перевозбуждении (пульс > 100 уд/мин).

Антидот: взять паузу на 20-30 минут и вернуться к разговору.''',
        'i18n': {
            'en': {
                'title': "Gottman's 'Four Horsemen': Predictors of Divorce",
                'brief': 'John Gottman identified four communication patterns that predict separation with 93% accuracy.',
                'body': '''## Gottman\'s Research

Over 40 years, John Gottman observed thousands of couples in his "Love Lab." He discovered four destructive patterns he called the "Four Horsemen of the Apocalypse."

## Horseman 1: Criticism

**What it is:** An attack on the person, not the behavior.
- Destructive: "You\'re such a selfish person, you never care"
- Constructive: "I felt sad that you didn\'t ask how my day went"

## Horseman 2: Contempt

**What it is:** The message "you are inferior to me." Sarcasm, mockery, eye-rolling.
Gottman calls it the most dangerous. It predicts not only divorce but also a decline in the partner\'s immune health.

Antidote: a culture of gratitude and respect.

## Horseman 3: Defensiveness

**What it is:** Denying responsibility, shifting blame.
- "That\'s not my problem, you always..."

Antidote: accept at least some responsibility. "Yes, I played a part in this too."

## Horseman 4: Stonewalling

**What it is:** Emotional withdrawal from the conversation — silence, avoidance.
Occurs when physiologically flooded (pulse > 100 bpm).

Antidote: take a 20–30 minute break and return to the conversation.''',
            },
            'uz': {
                'title': "Gottmanning 'To\'rt Chavandoz'i: ajrashish prognozchilari",
                'brief': "Jon Gottman ajrashishni 93% aniqlik bilan bashorat qiladigan to'rtta muloqot naqshini aniqladi.",
                'body': '''## Gottman tadqiqoti

40 yil davomida Jon Gottman o'zining «Muhabbat laboratoriyasi»da minglab juftliklarni kuzatdi. U «Apokalipsisning To\'rt Chavandozi» deb atagan to\'rtta destruktiv naqshni aniqladi.

## 1-chavandoz: Tanqid

**Nima u:** Xatti-harakatga emas, shaxsga hujum.
- Destruktiv: «Siz shunday xudbinsiz, sizga hech narsa ahamiyatli emas»
- Konstruktiv: «Kunim qanday o\'tganini so\'ramaganingizda xafa bo\'ldim»

## 2-chavandoz: Nafrat

**Nima u:** «Siz mendan pastroqsiz» xabari. Kinoya, masxara, ko\'z olmalarini aylantirish.
Gottman uni eng xavfli deb ataydi. U nafaqat ajrashishni, balki sherikda immunitetning pasayishini ham bashorat qiladi.

Zidpanzir: minnatdorlik va hurmat madaniyati.

## 3-chavandoz: Mudofaa

**Nima u:** Mas\'uliyatni inkor etish, aybni boshqaga yuklash.
- «Bu mening muammom emas, siz doim...»

Zidpanzir: hech bo\'lmasa bir qism mas\'uliyatni qabul qiling. «Ha, bu yerda mening ham o\'rnim bor».

## 4-chavandoz: Muloqotni bloklash (stounvalling)

**Nima u:** Suhbatdan hissiy chiqish — sukut, qochish.
Fiziologik haddan oshganda yuzaga keladi (puls > 100 urish/daqiqa).

Zidpanzir: 20-30 daqiqa tanaffus oling va suhbatga qayting.''',
            },
            'uz_cyrl': {
                'title': "Готтманнинг 'Тўрт Чавандози': ажрашиш прогнозчилари",
                'brief': "Жон Готтман ажрашишни 93% аниқлик билан башорат қиладиган тўртта мулоқот нақшини аниқлади.",
                'body': '''## Готтман тадқиқоти

40 йил давомида Жон Готтман ўзининг «Муҳаббат лабораторияси»да минглаб жуфтликларни кузатди. У «Апокалипсиснинг Тўрт Чавандози» деб атаган тўртта деструктив нақшни аниқлади.

## 1-чавандоз: Танқид

**Нима у:** Хатти-ҳаракатга эмас, шахсга ҳужум.
- Деструктив: «Сиз шундай худбинсиз, сизга ҳеч нарса аҳамиятли эмас»
- Конструктив: «Куним қандай ўтганини сўрамаганингизда хафа бўлдим»

## 2-чавандоз: Нафрат

**Нима у:** «Сиз мендан пастроқсиз» хабари. Кинoya, масхара, кўз олмаларини айлантириш.
Готтман уни энг хавфли деб атайди. У нафақат ажрашишни, балки шерикда иммунитетнинг пасайишини ҳам башорат қилади.

Зидпанзир: миннатдорлик ва ҳурмат маданияти.

## 3-чавандоз: Мудофаа

**Нима у:** Масъулиятни инкор этиш, айбни бошқага юклаш.
- «Бу менинг муаммом эмас, сиз доим...»

Зидпанзир: ҳеч бўлмаса бир қисм масъулиятни қабул қилинг. «Ҳа, бу ерда менинг ҳам ўрним бор».

## 4-чавандоз: Мулоқотни блоклаш (стоунваллинг)

**Нима у:** Суҳбатдан ҳиссий чиқиш — сукут, қочиш.
Физиологик ҳаддан ошганда юзага келади (пулс > 100 уриш/дақиқа).

Зидпанзир: 20-30 дақиқа танаффус олинг ва суҳбатга қайтинг.''',
            },
        },
        'read_time_minutes': 10,
        'difficulty': 'beginner',
        'tags': ['Готтман', 'паттерны', 'критика', 'презрение'],
        'sources': ['Джон Готтман', 'Journal of Marriage and Family'],
        'order_index': 3,
    },

    # --- Доверие ---
    {
        'slug': 'trust-building-foundations',
        'category': 'trust',
        'title': 'Научные основы доверия в паре',
        'brief': 'Что такое доверие с точки зрения психологии и нейронауки, и как оно строится и разрушается.',
        'body': '''## Что такое доверие

Доверие — это не чувство и не решение. Это накопленный опыт надёжности партнёра в малом и большом.

Исследования Брене Браун показывают: доверие строится в «мелких моментах», а не в грандиозных жестах.

## Модель BRAVING (Браун)

- **B** — Boundaries (Границы): я уважаю твои и говорю о своих
- **R** — Reliability (Надёжность): я делаю то, что обещал
- **A** — Accountability (Ответственность): я признаю ошибки
- **V** — Vault (Хранилище): я не делюсь тем, что ты мне доверил
- **I** — Integrity (Честность): я выбираю правильное, а не лёгкое
- **N** — Non-judgment (Без осуждения): ты можешь просить о помощи
- **G** — Generosity (Великодушие): я трактую твои действия в лучшую сторону

## Нейронаука доверия

Окситоцин — «гормон доверия» — выделяется при прикосновении, похвале, совместном смехе. Его уровень снижается при стрессе, критике и ощущении небезопасности.

## Что разрушает доверие быстрее всего

1. Ложь (даже «белая»)
2. Нарушение конфиденциальности
3. Непоследовательность слов и действий
4. Критика перед третьими лицами''',
        'i18n': {
            'en': {
                'title': 'The Science of Trust in a Couple',
                'brief': 'What trust is from a psychological and neuroscience perspective, and how it is built and broken.',
                'body': '''## What is trust

Trust is not a feeling or a decision. It is an accumulated experience of a partner\'s reliability in small and large things.

Research by Brené Brown shows: trust is built in "small moments," not in grand gestures.

## The BRAVING Model (Brown)

- **B** — Boundaries: I respect yours and speak up about mine
- **R** — Reliability: I do what I promise
- **A** — Accountability: I own my mistakes
- **V** — Vault: I don\'t share what you confided in me
- **I** — Integrity: I choose what\'s right over what\'s easy
- **N** — Non-judgment: You can ask for help without fear
- **G** — Generosity: I interpret your actions charitably

## The Neuroscience of Trust

Oxytocin — the "trust hormone" — is released through touch, praise, and shared laughter. Its level drops under stress, criticism, and a sense of unsafety.

## What destroys trust fastest

1. Lies (even "white" ones)
2. Breaching confidentiality
3. Inconsistency between words and actions
4. Criticism in front of others''',
            },
            'uz': {
                'title': "Juftlikda ishonchning ilmiy asoslari",
                'brief': "Psixologiya va nevrologiya nuqtai nazaridan ishonch nima va u qanday quriladi va yemiriladi.",
                'body': '''## Ishonch nima

Ishonch — bu his-tuyg\'u ham, qaror ham emas. Bu kichik va katta ishlarda sherikningizning ishonchliligidan to\'plangan tajriba.

Brene Braunning tadqiqotlari ko\'rsatadiki: ishonch «kichik lahzalar»da, katta imo-ishoralarda emas, quriladi.

## BRAVING modeli (Braun)

- **B** — Boundaries (Chegaralar): men siznikini hurmat qilaman va o\'zimnikini aytaman
- **R** — Reliability (Ishonchlilik): men va\'da berganimi bajaraman
- **A** — Accountability (Mas\'uliyat): men xatolarimni tan olaman
- **V** — Vault (Sir saqlash): men sizning sirlaringizni oshkor qilmayman
- **I** — Integrity (Halollik): men oson yo\'l emas, to\'g\'ri yo\'lni tanlayman
- **N** — Non-judgment (Hukmsizlik): siz yordam so\'rashdan qo\'rqmasangiz bo\'ladi
- **G** — Generosity (Saxiylik): men sizning harakatlaringizni yaxshilik nuqtai nazaridan talqin qilaman

## Ishonchning nevrologiyasi

Oksitotsin — «ishonch gormoni» — teginish, maqtash, birgalikda kulishda ajralib chiqadi. Uning darajasi stress, tanqid va xavfsizlik yo\'q bo\'lganda pasayadi.

## Ishonchni tezroq yo\'q qiladigan narsalar

1. Yolg\'on (hatto «oq» yolg\'on ham)
2. Maxfiylikni buzish
3. So\'z va harakatlar o\'rtasidagi ziddiyat
4. Uchinchi shaxslar oldida tanqid qilish''',
            },
            'uz_cyrl': {
                'title': "Жуфтликда ишончнинг илмий асослари",
                'brief': "Психология ва неврология нуқтаи назаридан ишонч нима ва у қандай қурилади ва йемирилади.",
                'body': '''## Ишонч нима

Ишонч — бу ҳис-туйғу ҳам, қарор ҳам эмас. Бу кичик ва катта ишларда шерикнинг ишончлилигидан тўпланган тажриба.

Брене Браunnинг тадқиқотлари кўрсатадики: ишонч «кичик лаҳзалар»да, катта имо-ишораларда эмас, қурилади.

## BRAVING модели (Браун)

- **B** — Boundaries (Чегаралар): мен сизникини ҳурмат қиламан ва ўзимникини айтаман
- **R** — Reliability (Ишончлилик): мен ва'да берганимни бажараман
- **A** — Accountability (Масъулият): мен хатоларимни тан оламан
- **V** — Vault (Сир сақлаш): мен сизнинг сирларингизни ошкор қилмайман
- **I** — Integrity (Ҳалоллик): мен осон йўл эмас, тўғри йўлни танлайман
- **N** — Non-judgment (Ҳукмсизлик): сиз ёрдам сўрашдан қўрқмасангиз бўлади
- **G** — Generosity (Саҳийлик): мен сизнинг ҳаракатларингизни яхшилик нуқтаи назаридан талқин қиламан

## Ишончнинг неврологияси

Окситотсин — «ишонч гормони» — тегиниш, мақташ, биргаликда кулишда ажралиб чиқади. Унинг даражаси стресс, танқид ва хавфсизлик йўқ бўлганда пасаяди.

## Ишончни тезроқ йўқ қиладиган нарсалар

1. Ёлғон (ҳатто «оқ» ёлғон ҳам)
2. Махфийликни бузиш
3. Сўз ва ҳаракатлар ўртасидаги зиддият
4. Учинчи шахслар олдида танқид қилиш''',
            },
        },
        'read_time_minutes': 7,
        'difficulty': 'beginner',
        'tags': ['доверие', 'надёжность', 'окситоцин'],
        'sources': ['APA (American Psychological Association)', 'NIH (National Institutes of Health)'],
        'order_index': 1,
    },
    {
        'slug': 'trust-after-betrayal',
        'category': 'trust',
        'title': 'Восстановление доверия после предательства',
        'brief': 'Научно обоснованный процесс восстановления доверия — от принятия боли до нового договора.',
        'body': '''## Предательство — это не только измена

Предательством может быть: ложь, сокрытие важного, нарушение финансовых договорённостей, разглашение секретов.

## Три фазы восстановления (по Готтман)

### Фаза 1: Атонемент (искупление)
Виновная сторона берёт полную ответственность без «но».
- «Я солгал. Это было неправильно. Я понимаю, как тебе больно.»
- Без объяснений причин (это будет позже)

### Фаза 2: Attunement (настройка)
Открытый диалог о боли: партнёр рассказывает, что именно причинило боль, виновный слушает без защиты.

Инструмент: «Встреча с честностью» — структурированный разговор с конкретными вопросами.

### Фаза 3: Attachment (новая привязанность)
Создание новых правил и договорённостей. Это не возврат к прошлому, а построение новых отношений.

## Признаки, что восстановление идёт правильно

- Виновный перестал защищаться
- Оба говорят о случившемся без эскалации
- Появляются новые совместные позитивные переживания
- Пострадавший начинает видеть будущее''',
        'i18n': {
            'en': {
                'title': 'Rebuilding Trust After Betrayal',
                'brief': 'A scientifically grounded process for rebuilding trust — from accepting pain to a new agreement.',
                'body': '''## Betrayal is not only infidelity

Betrayal can include: lies, hiding important information, breaking financial agreements, revealing secrets.

## Three Phases of Recovery (Gottman)

### Phase 1: Atonement
The offending partner takes full responsibility — no "buts."
- "I lied. That was wrong. I understand how much this hurts you."
- No explaining reasons (that comes later)

### Phase 2: Attunement
Open dialogue about the pain: the hurt partner shares what caused pain; the offending partner listens without defensiveness.

Tool: "The Honesty Meeting" — a structured conversation with specific questions.

### Phase 3: Attachment (new bond)
Creating new rules and agreements. This is not a return to the past, but building something new.

## Signs that recovery is going well

- The offending partner has stopped being defensive
- Both can speak about what happened without escalation
- New shared positive experiences are emerging
- The hurt partner begins to see a future''',
            },
            'uz': {
                'title': "Xiyonatdan keyin ishonchni tiklash",
                'brief': "Ishonchni tiklashning ilmiy asoslangan jarayoni — og'riqni qabul qilishdan yangi shartnomaga qadar.",
                'body': '''## Xiyonat faqat aldov emas

Xiyonat quyidagilarni o\'z ichiga olishi mumkin: yolg\'on, muhim ma\'lumotni yashirish, moliyaviy kelishuvlarni buzish, sirlarni oshkor qilish.

## Tiklashning uch bosqichi (Gottman)

### 1-bosqich: Tavba (Atonement)
Aybdor tomon to\'liq mas\'uliyatni oladi — «lekin»siz.
- «Men yolg\'on gapirdim. Bu noto\'g\'ri edi. Sening og\'riqingni tushunaman.»
- Sabab-oqibatlarni tushuntirmasdan (bu keyinroq bo\'ladi)

### 2-bosqich: Moslashish (Attunement)
Og\'riq haqida ochiq muloqot: jabrlanuvchi nima og\'riq berganini aytadi, aybdor mudofaasiz tinglaydi.

Vosita: «Halollik uchrashuvi» — aniq savollar bilan tuzilgan suhbat.

### 3-bosqich: Yangi bog\'liqlik (Attachment)
Yangi qoidalar va kelishuvlar yaratish. Bu o\'tmishga qaytish emas, balki yangi narsa qurishdir.

## Tiklash to\'g\'ri ketayotganining belgilari

- Aybdor tomon himoyalanishni to\'xtatdi
- Ikkalasi ham bo\'lgan narsalar haqida eskalatsiyasiz gaplasha oladi
- Yangi umumiy ijobiy tajribalar paydo bo\'lmoqda
- Jabrlanuvchi kelajakni ko\'ra boshladi''',
            },
            'uz_cyrl': {
                'title': "Хиёнатдан кейин ишончни тиклаш",
                'brief': "Ишончни тиклашнинг илмий асосланган жараёни — оғриқни қабул қилишдан янги шартномага қадар.",
                'body': '''## Хиёнат фақат алдов эмас

Хиёнат қуйидагиларни ўз ичига олиши мумкин: ёлғон, муҳим маълумотни яшириш, молиявий келишувларни бузиш, сирларни ошкор қилиш.

## Тиклашнинг уч босқичи (Готтман)

### 1-босқич: Тавба (Atonement)
Айбдор тамон тўлиқ масъулиятни олади — «лекин»сиз.
- «Мен ёлғон гапирдим. Бу нотўғри эди. Сенинг оғриқингни тушунаман.»
- Сабаб-оқибатларни тушунтирмасдан (бу кейинроқ бўлади)

### 2-босқич: Мослашиш (Attunement)
Оғриқ ҳақида очиқ мулоқот: жабрланувчи нима оғриқ берганини айтади, айбдор мудофаасиз тинглайди.

Восита: «Ҳалоллик учрашуви» — аниқ саволлар билан тузилган суҳбат.

### 3-босқич: Янги боғлиқлик (Attachment)
Янги қоидалар ва келишувлар яратиш. Бу ўтмишга қайтиш эмас, балки янги нарса қуришдир.

## Тиклаш тўғри кетаётганининг белгилари

- Айбдор тамон ҳимояланишни тўхтатди
- Иккаласи ҳам бўлган нарсалар ҳақида эскалацияsиз гаплаша олади
- Янги умумий ижобий тажрибалар пайдо бўлмоқда
- Жабрланувчи келажакни кўра бошлади''',
            },
        },
        'read_time_minutes': 9,
        'difficulty': 'advanced',
        'tags': ['предательство', 'прощение', 'восстановление'],
        'sources': ['Джон Готтман', 'Джули Готтман'],
        'order_index': 2,
    },

    # --- Конфликты ---
    {
        'slug': 'conflict-solvable-vs-perpetual',
        'category': 'conflict',
        'title': 'Решаемые и вечные конфликты: в чём разница',
        'brief': 'Готтман обнаружил, что 69% конфликтов в паре — вечные. Их нельзя решить. Но с ними можно научиться жить.',
        'body': '''## Открытие Готтмана

В ходе многолетних исследований Джон Готтман установил: примерно 69% разногласий в паре — это «вечные конфликты», основанные на фундаментальных различиях в личности или потребностях.

## Что такое вечный конфликт

Вечный конфликт — это разногласие, которое повторяется снова и снова вне зависимости от того, сколько раз вы его «обсуждали».

Примеры:
- Один интроверт, другой экстраверт
- Разное отношение к деньгам как к безопасности vs. инструменту радости
- Разные потребности в близости и личном пространстве

## Цель с вечными конфликтами — не решить, а управлять

Счастливые пары не решают эти конфликты. Они:
1. Смеются над ними
2. Выработали «временные соглашения»
3. Глубоко поняли мечты и ценности друг друга, стоящие за позицией

## Как понять, что за позицией

Спросите: «Что для тебя самое важное в этом? Какая твоя мечта или страх связан с этим?»

## Решаемые конфликты

Это ситуативные разногласия без глубинного смысла: кто моет посуду, куда ехать в отпуск. Их решают через переговоры и компромисс.''',
        'i18n': {
            'en': {
                'title': 'Solvable vs. Perpetual Conflicts: What\'s the Difference',
                'brief': 'Gottman found that 69% of couple conflicts are perpetual. They cannot be solved. But you can learn to live with them.',
                'body': '''## Gottman\'s Discovery

After years of research, John Gottman found: roughly 69% of couple disagreements are "perpetual conflicts" rooted in fundamental differences in personality or needs.

## What is a perpetual conflict

A perpetual conflict is a disagreement that recurs again and again regardless of how many times you have "discussed" it.

Examples:
- One is introverted, the other extroverted
- Different attitudes toward money as security vs. a tool for joy
- Different needs for closeness and personal space

## The goal with perpetual conflicts — not to solve, but to manage

Happy couples don\'t resolve these conflicts. They:
1. Laugh about them
2. Have developed "temporary agreements"
3. Deeply understood the dreams and values behind each other\'s positions

## How to understand what is behind a position

Ask: "What matters most to you about this? What dream or fear do you connect with this?"

## Solvable conflicts

These are situational disagreements with no deeper meaning: who washes the dishes, where to vacation. They are resolved through negotiation and compromise.''',
            },
            'uz': {
                'title': "Hal qilinadigan va abadiy nizolar: farqi nima",
                'brief': "Gottman juftlikdagi nizolarning 69% abadiy ekanini aniqladi. Ularni hal qilib bo\'lmaydi. Ammo ular bilan yashashni o\'rganish mumkin.",
                'body': '''## Gottman kashfiyoti

Ko\'p yillik tadqiqotlar natijasida Jon Gottman aniqladi: juftlik kelishmovchiligining taxminan 69% shaxs yoki ehtiyojlardagi fundamental farqlarga asoslangan «abadiy nizolar»dir.

## Abadiy nizo nima

Abadiy nizo — qancha «muhokama qilganingizdan» qat\'i nazar qayta-qayta takrorlanadigan kelishmovchilik.

Misollar:
- Biri introver, ikkinchisi ekstraver
- Pulga munosabatning farqi: xavfsizlik vs. quvonch vositasi
- Yaqinlik va shaxsiy makon ehtiyojlarining farqi

## Abadiy nizolardagi maqsad — hal qilish emas, boshqarish

Baxtli juftliklar bu nizolarni hal qilmaydi. Ular:
1. Ular ustidan kulishadi
2. «Vaqtinchalik kelishuvlar» ishlab chiqarishgan
3. Bir-birining pozitsiyasi orqasidagi orzular va qadriyatlarni chuqur tushunishgan

## Pozitsiya ortida nima borligini qanday tushunish mumkin

So\'rang: «Bu borada siz uchun eng muhimi nima? Qanday orzu yoki qo\'rquv bilan bog\'liq?»

## Hal qilinadigan nizolar

Bular chuqur ma\'nosiz vaziyatli kelishmovchiliklar: kim idish yuvadi, ta\'tilni qayerda o\'tkazish. Ular muzokaralar va murosasozlik orqali hal qilinadi.''',
            },
            'uz_cyrl': {
                'title': "Ҳал қилинадиган ва абадий низолар: фарқи нима",
                'brief': "Готтман жуфтликдаги низоларнинг 69% абадий эканини аниқлади. Уларни ҳал қилиб бўлмайди. Аммо улар билан яшашни ўрганиш мумкин.",
                'body': '''## Готтман кашфиёти

Кўп йиллик тадқиқотлар натижасида Жон Готтман аниқлади: жуфтлик келишмовчилигининг тахминан 69% шахс ёки эҳтиёжлардаги фундаментал фарқларга асосланган «абадий низолар»дир.

## Абадий низо нима

Абадий низо — қанча «муҳокама қилганингиздан» қатъи назар қайта-қайта такрорланадиган келишмовчилик.

Мисоллар:
- Бири интровер, иккинчиси экстравер
- Пулга муносабатнинг фарқи: хавфсизлик vs. қувонч воситаси
- Яқинлик ва шахсий макон эҳтиёжларининг фарқи

## Абадий низолардаги мақсад — ҳал қилиш эмас, бошқариш

Бахтли жуфтликлар бу низоларни ҳал қилмайди. Улар:
1. Улар устидан куладилар
2. «Вақтинчалик келишувлар» ишлаб чиқаришган
3. Бир-бирининг позицияси ортидаги орзулар ва қадриятларни чуқур тушунишган

## Позиция ортида нима борлигини қандай тушуниш мумкин

Сўранг: «Бу борада сиз учун энг муҳими нима? Қандай орзу ёки қўрқув билан боғлиқ?»

## Ҳал қилинадиган низолар

Булар чуқур маъносиз вазиятли келишмовчиликлар: ким идиш ювади, та\'тилни қаерда ўтказиш. Улар музокаралар ва мурoсасозлик орқали ҳал қилинади.''',
            },
        },
        'read_time_minutes': 8,
        'difficulty': 'intermediate',
        'tags': ['конфликт', 'компромисс', 'переговоры'],
        'sources': ['Джон Готтман', 'Journal of Marriage and Family'],
        'order_index': 1,
    },
    {
        'slug': 'repair-attempts',
        'category': 'conflict',
        'title': 'Попытки примирения: как остановить эскалацию',
        'brief': 'Готтман назвал «попытки примирения» самым важным предиктором успешных отношений.',
        'body': '''## Что такое попытка примирения

Попытка примирения — любой жест, слово или действие, которое останавливает нарастание напряжения во время конфликта.

Это может быть:
- Юмор (осторожный)
- «Стоп, мне нужна пауза»
- «Я знаю, что это важно для тебя»
- Лёгкое прикосновение
- «Прости, я сказал это грубо»

## Почему это так важно

В счастливых парах попытки примирения **принимаются** обоими. В несчастных — отвергаются даже хорошие попытки, потому что накопилось слишком много обиды.

## Как выработать общий язык примирения

1. В спокойное время обсудите, что помогает каждому из вас остановиться
2. Создайте кодовое слово или жест
3. Договоритесь: когда один произносит кодовое слово — пауза обязательна

## Физиология конфликта

Когда пульс превышает 100 уд/мин, кора головного мозга («мыслящий мозг») отключается. В этом состоянии невозможно слышать партнёра. Пауза 20-30 минут позволяет восстановиться физиологически.''',
        'i18n': {
            'en': {
                'title': 'Repair Attempts: How to Stop Escalation',
                'brief': "Gottman called 'repair attempts' the most important predictor of successful relationships.",
                'body': '''## What is a repair attempt

A repair attempt is any gesture, word, or action that stops the rising tension during a conflict.

This can be:
- Humor (used carefully)
- "Stop, I need a break"
- "I know this matters to you"
- A gentle touch
- "Sorry, I said that harshly"

## Why this matters so much

In happy couples, repair attempts are **accepted** by both partners. In unhappy couples, even good attempts are rejected because too much resentment has built up.

## How to develop a shared language of repair

1. In a calm moment, discuss what helps each of you to stop
2. Create a code word or gesture
3. Agree: when one person says the code word — a pause is mandatory

## The physiology of conflict

When heart rate exceeds 100 bpm, the cerebral cortex ("thinking brain") shuts down. In this state, it is impossible to hear your partner. A 20–30 minute pause allows physiological recovery.''',
            },
            'uz': {
                'title': "Yarashish urinishlari: eskalatsiyani qanday to'xtatish mumkin",
                'brief': "Gottman 'yarashish urinishlari'ni munosabatlar muvaffaqiyatining eng muhim ko'rsatkichi deb atadi.",
                'body': '''## Yarashish urinishi nima

Yarashish urinishi — nizo paytida zo\'riqishning ortib borishini to\'xtatadigan har qanday imo-ishora, so\'z yoki harakat.

Bu bo\'lishi mumkin:
- Hazil (ehtiyotkorlik bilan)
- «To\'xta, menga tanaffus kerak»
- «Bilaman, bu siz uchun muhim»
- Yengil teginish
- «Kechirasiz, buni qo\'polroq aytdim»

## Bu nima uchun bu qadar muhim

Baxtli juftliklarda yarashish urinishlari ikkalasi tomonidan ham **qabul qilinadi**. Baxtsizdagida — juda ko\'p nafrat to\'plangani uchun hatto yaxshi urinishlar ham rad etiladi.

## Yarashishning umumiy tilini qanday shakllantirish

1. Tinch vaqtda har biringizni to\'xtatishga nima yordam berishini muhokama qiling
2. Shifr so\'z yoki imo-ishora o\'ylab toping
3. Kelishing: biri shifr so\'zni aytsa — tanaffus majburiy

## Nizoning fiziologiyasi

Puls 100 ud/daqiqadan oshganda, miya po\'stlog\'i («fikrlovchi miya») o\'chadi. Bu holatda sherikni eshitish mumkin emas. 20-30 daqiqalik tanaffus fiziologik tiklanishga imkon beradi.''',
            },
            'uz_cyrl': {
                'title': "Ярашиш уринишлари: эскалацияни қандай тўхтатиш мумкин",
                'brief': "Готтман 'ярашиш уринишлари'ни муносабатлар муваффақиятининг энг муҳим кўрсаткичи деб атади.",
                'body': '''## Ярашиш уринишлари нима

Ярашиш уринишлари — низо пайтида зўриқишнинг ортиб боришини тўхтатадиган ҳар қандай имо-ишора, сўз ёки ҳаракат.

Бу бўлиши мумкин:
- Ҳазил (эҳтиёткорлик билан)
- «Тўхта, менга танаффус керак»
- «Биламан, бу сиз учун муҳим»
- Енгил тегиниш
- «Кечирасиз, буни қўполроқ айтдим»

## Бу нима учун бу қадар муҳим

Бахтли жуфтликларда ярашиш уринишлари иккаласи томонидан ҳам **қабул қилинади**. Бахтсизларда — жуда кўп нафрат тўпланганлиги учун ҳатто яхши уринишлар ҳам рад этилади.

## Ярашишнинг умумий тилини қандай шакллантириш

1. Тинч вақтда ҳар биринглизни тўхтатишга нима ёрдам беришини муҳокама қилинг
2. Шифр сўз ёки имо-ишора ўйлаб топинг
3. Келишинг: бири шифр сўзни айтса — танаффус мажбурий

## Низонинг физиологияси

Пулс 100 уд/дақиқадан ошганда, мия пўстлоғи («фикрловчи мия») ўчади. Бу ҳолатда шерикни эшитиш мумкин эмас. 20-30 дақиқалик танаффус физиологик тикланишга имкон беради.''',
            },
        },
        'read_time_minutes': 7,
        'difficulty': 'beginner',
        'tags': ['конфликт', 'примирение', 'эскалация'],
        'sources': ['Джон Готтман', 'APA (American Psychological Association)'],
        'order_index': 2,
    },

    # --- Эмоциональная близость ---
    {
        'slug': 'emotional-intimacy-science',
        'category': 'intimacy',
        'title': 'Что такое эмоциональная близость и как её строить',
        'brief': 'Эмоциональная близость — это не влюблённость. Это навык, который строится через маленькие ежедневные действия.',
        'body': '''## Близость — это не романтика

Большинство людей путают эмоциональную близость с романтическими чувствами. Но влюблённость — это нейрохимическое состояние, которое длится 18-36 месяцев. Близость — это то, что остаётся и растёт дальше.

## Теория привязанности (Джон Боулби, Сью Джонсон)

Взрослые, как и дети, нуждаются в безопасной привязанности. Основной вопрос, который мы задаём партнёру: «Ты здесь? Я могу на тебя рассчитывать? Я важен для тебя?»

Эмоционально-фокусированная терапия (EFT) Сью Джонсон показывает: большинство конфликтов — это крики о близости, замаскированные под претензии.

## Четыре уровня близости

1. **Информационный** — знаем факты друг о друге
2. **Мнений** — делимся взглядами без страха осуждения
3. **Чувств** — говорим об эмоциях, уязвимости
4. **Потребностей** — открываем то, что нам действительно нужно от другого

## Практика: «Карта любви» (Готтман)

Регулярно обновляйте знания о внутреннем мире друг друга:
- Какой страх твой самый большой прямо сейчас?
- Что тебя больше всего радует в этот период жизни?
- Какая мечта у тебя есть, о которой я, возможно, не знаю?''',
        'i18n': {
            'en': {
                'title': 'What Emotional Intimacy Is and How to Build It',
                'brief': 'Emotional intimacy is not being in love. It is a skill built through small daily actions.',
                'body': '''## Intimacy is not romance

Most people confuse emotional intimacy with romantic feelings. But being in love is a neurochemical state that lasts 18–36 months. Intimacy is what remains and grows beyond that.

## Attachment Theory (John Bowlby, Sue Johnson)

Adults, like children, need secure attachment. The core question we ask our partner: "Are you there? Can I count on you? Do I matter to you?"

Sue Johnson\'s Emotionally Focused Therapy (EFT) shows: most conflicts are cries for intimacy disguised as complaints.

## Four Levels of Intimacy

1. **Informational** — we know facts about each other
2. **Opinions** — we share views without fear of judgment
3. **Feelings** — we speak about emotions, vulnerability
4. **Needs** — we reveal what we truly need from the other

## Practice: "Love Map" (Gottman)

Regularly update your knowledge of each other\'s inner world:
- What is your biggest fear right now?
- What brings you the most joy in this period of your life?
- What dream do you have that I might not know about?''',
            },
            'uz': {
                'title': "Hissiy yaqinlik nima va uni qanday qurish mumkin",
                'brief': "Hissiy yaqinlik — sevgi emas. Bu kichik kundalik harakatlar orqali quriladigan ko'nikma.",
                'body': '''## Yaqinlik — bu romantika emas

Ko\'pchilik hissiy yaqinlikni romantik his-tuyg\'ular bilan adashtiradi. Ammo oshiqlik — 18-36 oy davom etadigan neyrochemiyaviy holat. Yaqinlik — undan keyin qoladigan va o\'sadigan narsadir.

## Ilova nazariyasi (Jon Bowlby, Syu Johnson)

Kattalar ham, bolalar kabi, xavfsiz ilova kerak. Sherigimizga beradigan asosiy savol: «Siz bu yerdamidiz? Sizga tayanish mumkinmi? Men siz uchun muhimmanmi?»

Syu Johnsonning hissiy-markazlashgan terapiyasi (EFT) ko\'rsatadiki: ko\'pchilik nizolar shikoyatlar niqobidagi yaqinlik uchun faryodlardir.

## Yaqinlikning to\'rtta darajasi

1. **Axborot** — biz bir-birimiz haqida faktlarni bilamiz
2. **Fikrlar** — biz hukm qo\'rquvisiz fikrlarimizni baham ko\'ramiz
3. **Hissiyotlar** — hissiyotlar, zaiflik haqida gaplashamiz
4. **Ehtiyojlar** — biz ikkinchisidan haqiqatan nima kerakligini ochib beramiz

## Amaliyot: «Sevgi xaritasi» (Gottman)

Bir-biriningizning ichki dunyosi haqidagi bilimlarni muntazam yangilang:
- Hozir sizning eng katta qo\'rquvingiz nima?
- Hayotning bu davrida sizni eng ko\'p nima quvontiradi?
- Menga ma\'lum bo\'lmagan orzuyingiz bormi?''',
            },
            'uz_cyrl': {
                'title': "Ҳиссий яқинлик нима ва уни қандай қуриш мумкин",
                'brief': "Ҳиссий яқинлик — севги эмас. Бу кичик кундалик ҳаракатлар орқали қуриладиган кўникма.",
                'body': '''## Яқинлик — бу романтика эмас

Кўпчилик ҳиссий яқинликни романтик ҳис-туйғулар билан адаштиради. Аммо ошиқлик — 18-36 ой давом этадиган нейрохимиявий ҳолат. Яқинлик — ундан кейин қоладиган ва ўсадиган нарсадир.

## Илова назарияси (Жон Боулби, Сью Жонсон)

Катталар ҳам, болалар каби, хавфсиз илова керак. Шерик мизга берадиган асосий савол: «Сиз бу ердамизсиз? Сизга таяниш мумкинми? Мен сиз учун муҳимманми?»

Сью Жонсоннинг ҳиссий-марказлашган терапияси (EFT) кўрсатадики: кўпчилик низолар шикоятлар ниқобидаги яқинлик учун фарёдлардир.

## Яқинликнинг тўртта даражаси

1. **Ахборот** — биз бир-биримиз ҳақида фактларни биламиз
2. **Фикрлар** — биз ҳукм қўрқувисиз фикрларимизни баҳам кўрамиз
3. **Ҳиссиётлар** — ҳиссиётлар, заифлик ҳақида гаплашамиз
4. **Эҳтиёжлар** — биз иккинчисидан ҳақиқатан нима кераклигини очиб берамиз

## Амалиёт: «Севги харитаси» (Готтман)

Бир-бирингизнинг ички дунёси ҳақидаги билимларни мунтазам янгиланг:
- Ҳозир сизнинг энг катта қўрқувингиз нима?
- Ҳаётнинг бу даврида сизни энг кўп нима қувонтиради?
- Менга маълум бўлмаган орзуингиз борми?''',
            },
        },
        'read_time_minutes': 8,
        'difficulty': 'beginner',
        'tags': ['близость', 'привязанность', 'EFT', 'уязвимость'],
        'sources': ['Сью Джонсон', 'Джон Готтман'],
        'order_index': 1,
    },

    # --- Любовь и уважение ---
    {
        'slug': 'five-love-languages',
        'category': 'love',
        'title': 'Пять языков любви: как говорить на языке партнёра',
        'brief': 'Концепция Гэри Чепмена о том, что люди выражают и воспринимают любовь по-разному.',
        'body': '''## Почему «я тебя люблю» может не работать

Если партнёр не чувствует вашей любви несмотря на то, что вы любите его — возможно, вы говорите на разных «языках любви».

## Пять языков (Гэри Чепмен)

### 1. Слова поддержки
Человек чувствует любовь через словесное подтверждение: похвалу, признательность, слова ободрения.
«Ты отлично справился», «Я горжусь тобой», «Ты важен для меня».

### 2. Время вместе
Не просто присутствие, а качественное внимание: отложенные телефоны, совместные занятия, разговоры «в глаза».

### 3. Подарки
Не обязательно дорогие. Это символы внимания: «я думал о тебе, когда это увидел».

### 4. Помощь и служение
Конкретные действия, облегчающие жизнь: приготовить ужин, записать к врачу, отвезти.

### 5. Прикосновения
Объятия, поглаживания, физический контакт (не только сексуальный).

## Как узнать язык партнёра

1. Замечайте, как он сам выражает любовь (обычно так, как хочет получать)
2. Обратите внимание, на что он жалуется чаще всего
3. Спросите напрямую: «Что заставляет тебя чувствовать себя любимым?»

## Важное предупреждение

Чепмен — теолог, а не исследователь. Его модель популярна, но научных доказательств именно этой классификации мало. Ценность — в идее, что люди действительно разные, и нужно учиться языку партнёра.''',
        'i18n': {
            'en': {
                'title': "Five Love Languages: How to Speak Your Partner's Language",
                'brief': "Gary Chapman's concept that people express and receive love differently.",
                'body': '''## Why "I love you" may not work

If your partner doesn\'t feel your love despite the fact that you love them — perhaps you\'re speaking different "love languages."

## The Five Languages (Gary Chapman)

### 1. Words of Affirmation
A person feels love through verbal confirmation: praise, appreciation, words of encouragement.
"You did great," "I\'m proud of you," "You matter to me."

### 2. Quality Time
Not just presence, but focused attention: phones put away, doing things together, conversations eye-to-eye.

### 3. Gifts
Not necessarily expensive. These are symbols of attention: "I was thinking of you when I saw this."

### 4. Acts of Service
Specific actions that make life easier: cooking dinner, booking an appointment, giving a ride.

### 5. Physical Touch
Hugs, caresses, physical contact (not only sexual).

## How to discover your partner\'s language

1. Notice how they express love themselves (usually how they want to receive it)
2. Pay attention to what they complain about most often
3. Ask directly: "What makes you feel loved?"

## An important caveat

Chapman is a theologian, not a researcher. His model is popular, but there is little scientific evidence for exactly this classification. The value lies in the idea that people are genuinely different, and you need to learn your partner\'s language.''',
            },
            'uz': {
                'title': "Beshta sevgi tili: sheringiz tilida qanday gapirish",
                'brief': "Geri Chapmenning odamlar sevgini har xil ifodalashi va qabul qilishi haqidagi kontseptsiyasi.",
                'body': '''## Nima uchun «Seni sevaman» ishlamasligi mumkin

Agar sherik sizi sevayotganingizga qaramay sevgingizni his qilmasa — ehtimol siz har xil «sevgi tillari»da gapiraysiz.

## Besh til (Geri Chapman)

### 1. Tasdiq so\'zlari
Inson verbal tasdiqlash orqali sevgini his qiladi: maqtash, minnatdorlik, rag\'batlantirish so\'zlari.
«Siz ajoyib qildingiz», «Men sizdan faxrlanaman», «Siz men uchun muhimсиз».

### 2. Sifatli vaqt
Shunchaki hozirlik emas, diqqatli e\'tibor: telefonsiz, birgalikdagi mashg\'ulotlar, ko\'zma-ko\'z suhbatlar.

### 3. Sovg\'alar
Albatta qimmat emas. Bular diqqatning ramzlari: «Buni ko\'rganda siz haqingizda o\'yladim».

### 4. Xizmat ko\'rsatish
Hayotni engillashtiruvchi aniq harakatlar: kechki ovqat pishirish, shifokorga yozilish, olib borish.

### 5. Jismoniy teginish
Quchoqlash, sipalash, jismoniy aloqa (faqat seksual emas).

## Sheringiz tilini qanday aniqlash

1. U sevgini o\'zi qanday ifodalashiga e\'tibor bering (odatda qabul qilishni xohlagan usulda)
2. U ko\'pincha nimadan shikoyat qilishiga e\'tibor bering
3. To\'g\'ridan-to\'g\'ri so\'rang: «Seni sevimli his qiladigan narsa nima?»

## Muhim eslatma

Chapman — ilohiyotchi, tadqiqotchi emas. Uning modeli mashhur, lekin aynan bu tasnif uchun ilmiy dalillar oz. Qadriyat — odamlar haqiqatan har xil bo\'lganligi va sheringizning tilini o\'rganish kerakligi g\'oyasida.''',
            },
            'uz_cyrl': {
                'title': "Бешта севги тили: шерингиз тилида қандай гапириш",
                'brief': "Гери Чапменнинг одамлар севгини ҳар хил ифодалаши ва қабул қилиши ҳақидаги концепцияси.",
                'body': '''## Нима учун «Сени севаман» ишламаслиги мумкин

Агар шерик сизни севаётганингизга қарамай севгингизни ҳис қилмаса — эҳтимол сиз ҳар хил «севги тиллари»да гапирасиз.

## Беш тил (Гери Чапмен)

### 1. Тасдиқ сўзлари
Инсон вербал тасдиқлаш орқали севгини ҳис қилади: мақташ, миннатдорлик, рағбатлантириш сўзлари.
«Сиз ажойиб қилдингиз», «Мен сиздан фахрланаман», «Сиз мен учун муҳимсиз».

### 2. Сифатли вақт
Шунчаки ҳозирлик эмас, диқкатли эьтибор: телефонсиз, биргаликдаги машғулотлар, кўзма-кўз суҳбатлар.

### 3. Совғалар
Албатта қиммат эмас. Булар диқкатнинг рамзлари: «Буни кўрганда сиз ҳақингизда ўйладим».

### 4. Хизмат кўрсатиш
Ҳаётни енгиллаштирувчи аниқ ҳаракатлар: кечки овқат пишириш, шифокорга ёзилиш, олиб бориш.

### 5. Жисмоний тегиниш
Қучоқлаш, сипалаш, жисмоний алоқа (фақат сексуал эмас).

## Шерингиз тилини қандай аниқлаш

1. У севгини ўзи қандай ифодалашига эьтибор беринг (одатда қабул қилишни хоҳлаган усулда)
2. У кўпинча нимадан шикоят қилишига эьтибор беринг
3. Тўғридан-тўғри сўранг: «Сени севимли ҳис қиладиган нарса нима?»

## Муҳим эслатма

Чапмен — илоҳиётчи, тадқиқотчи эмас. Унинг модели машҳур, лекин айнан бу тасниф учун илмий далиллар оз. Қадрият — одамлар ҳақиқатан ҳар хил бўлганлиги ва шерингизнинг тилини ўрганиш кераклиги ғоясида.''',
            },
        },
        'read_time_minutes': 9,
        'difficulty': 'beginner',
        'tags': ['языки любви', 'Чепмен', 'признание'],
        'sources': ['Гэри Чепмен'],
        'order_index': 1,
    },

    # --- Финансы ---
    {
        'slug': 'couples-and-money',
        'category': 'finance',
        'title': 'Деньги в паре: как избежать самых частых конфликтов',
        'brief': 'Финансовые разногласия — одна из главных причин разводов. Не из-за денег, а из-за ценностей, которые за ними стоят.',
        'body': '''## Деньги — это не математика

Исследования APA показывают: финансы входят в тройку главных источников стресса в паре. Но суть конфликтов редко в деньгах. За ними стоят:

- Ощущение безопасности (накопления)
- Чувство свободы (трата)
- Власть и контроль
- Ценности и приоритеты

## Три системы управления финансами в паре

**1. Полное объединение.** Один общий счёт. Все доходы и расходы вместе.
*Плюс:* прозрачность. *Минус:* требует высокого доверия.

**2. Раздельные финансы.** Каждый управляет своим. Общие расходы делятся по договорённости.
*Плюс:* автономия. *Минус:* может создавать ощущение раздельности.

**3. Гибридная система.** Общий счёт для семейных расходов + личные счёта для «карманных денег».
Исследования показывают, что это наиболее распространённая рабочая модель.

## Как провести «финансовый разговор»

1. Выберите подходящее время (не в момент стресса)
2. Поговорите об отношении к деньгам в семье каждого из вас
3. Определите общие цели (квартира, отпуск, образование детей)
4. Договоритесь о «лимите самостоятельных трат» — суммой, до которой не нужно советоваться
5. Назначьте регулярный «финансовый митинг»''',
        'i18n': {
            'en': {
                'title': 'Money in a Couple: How to Avoid the Most Common Conflicts',
                'brief': 'Financial disagreements are one of the leading causes of divorce. Not because of money, but because of the values behind it.',
                'body': '''## Money is not math

APA research shows: finances rank among the top three sources of stress in a couple. But the heart of conflicts is rarely money itself. Behind it lie:

- A sense of security (savings)
- A feeling of freedom (spending)
- Power and control
- Values and priorities

## Three Financial Systems in a Couple

**1. Full merger.** One joint account. All income and expenses together.
*Pro:* transparency. *Con:* requires high trust.

**2. Separate finances.** Each manages their own. Shared expenses split by agreement.
*Pro:* autonomy. *Con:* can create a sense of separation.

**3. Hybrid system.** A joint account for family expenses + personal accounts for "pocket money."
Research shows this is the most common working model.

## How to have a "financial conversation"

1. Choose a good time (not during stress)
2. Talk about each of your relationships with money growing up
3. Identify shared goals (apartment, vacation, children\'s education)
4. Agree on a "personal spending limit" — an amount below which you don\'t need to consult each other
5. Set a regular "financial meeting"''',
            },
            'uz': {
                'title': "Juftlikda pul: eng ko'p uchraydigan nizolardan qanday qochish",
                'brief': "Moliyaviy kelishmovchiliklar ajrashishning asosiy sabablaridan biri. Pul tufayli emas, uning ortidagi qadriyatlar tufayli.",
                'body': '''## Pul — bu matematika emas

APA tadqiqotlari ko\'rsatadiki: moliya juftlikda stress manbasining dastlabki uchtasiga kiradi. Ammo nizolarning mohiyati kamdan-kam hollarda pulda bo\'ladi. Uning ortida:

- Xavfsizlik hissi (jamg\'arma)
- Erkinlik hissi (sarflash)
- Hokimiyat va nazorat
- Qadriyatlar va ustuvorliklar

## Juftlikda uch moliyaviy tizim

**1. To\'liq birlashtirish.** Bitta umumiy hisob. Barcha daromad va xarajatlar birgalikda.
*Ijobiy:* shaffoflik. *Salbiy:* yuqori ishonchni talab qiladi.

**2. Alohida moliya.** Har biri o\'z moliyasini boshqaradi. Umumiy xarajatlar kelishilgan tarzda bo\'linadi.
*Ijobiy:* mustaqillik. *Salbiy:* alohidalilik hissini yaratishi mumkin.

**3. Gibrid tizim.** Oilaviy xarajatlar uchun umumiy hisob + «cho\'ntak puli» uchun shaxsiy hisoblar.
Tadqiqotlar shuni ko\'rsatadiki, bu eng ko\'p ishlatiladigan model.

## «Moliyaviy suhbat»ni qanday o\'tkazish

1. Mos vaqt tanlang (stress paytida emas)
2. Har biringizning oilangizda pulga munosabat haqida gaplashing
3. Umumiy maqsadlarni belgilang (kvartira, ta\'til, bolalar ta\'limi)
4. «Mustaqil sarflash limiti»ni belgilang — kengashmasdan sarflash mumkin bo\'lgan miqdor
5. Muntazam «moliyaviy yig\'ilish» belgilang''',
            },
            'uz_cyrl': {
                'title': "Жуфтликда пул: энг кўп учрайдиган низолардан қандай қочиш",
                'brief': "Молиявий келишмовчиликлар ажрашишнинг асосий сабабларидан бири. Пул туфайли эмас, унинг ортидаги қадриятлар туфайли.",
                'body': '''## Пул — бу математика эмас

APA тадқиқотлари кўрсатадики: молия жуфтликда стресс манбасининг дастлабки учтасига киради. Аммо низоларнинг моҳияти камдан-кам ҳолларда пулда бўлади. Унинг ортида:

- Хавфсизлик ҳисси (жамғарма)
- Эркинлик ҳисси (сарфлаш)
- Ҳокимият ва назорат
- Қадриятлар ва устуворликлар

## Жуфтликда уч молиявий тизим

**1. Тўлиқ бирлаштириш.** Битта умумий ҳисоб. Барча даромад ва харажатлар биргаликда.
*Ижобий:* шаффофлик. *Салбий:* юқори ишончни талаб қилади.

**2. Алоҳида молия.** Ҳар бири ўз молиясини бошқаради. Умумий харажатлар келишилган тарзда бўлинади.
*Ижобий:* мустақиллик. *Салбий:* алоҳидалик ҳиссини яратиши мумкин.

**3. Гибрид тизим.** Оилавий харажатлар учун умумий ҳисоб + «чўнтак пули» учун шахсий ҳисоблар.
Тадқиқотлар шуни кўрсатадики, бу энг кўп ишлатиладиган модел.

## «Молиявий суҳбат»ни қандай ўтказиш

1. Мос вақт танланг (стресс пайтида эмас)
2. Ҳар биринглизнинг оилангизда пулга муносабат ҳақида гаплашинг
3. Умумий мақсадларни белгиланг (квартира, та\'тил, болалар та\'лими)
4. «Мустақил сарфлаш лимити»ни белгиланг — кенгашмасдан сарфлаш мумкин бўлган миқдор
5. Мунтазам «молиявий йиғилиш» белгиланг''',
            },
        },
        'read_time_minutes': 8,
        'difficulty': 'intermediate',
        'tags': ['финансы', 'бюджет', 'доверие'],
        'sources': ['APA (American Psychological Association)', 'Journal of Marriage and Family'],
        'order_index': 1,
    },

    # --- Стресс и выгорание ---
    {
        'slug': 'stress-and-relationship',
        'category': 'stress',
        'title': 'Как стресс разрушает отношения и что с этим делать',
        'brief': 'Внешний стресс — работа, деньги, здоровье — попадает в отношения. Но пара может стать буфером стресса, а не его усилителем.',
        'body': '''## Стресс «перетекает» в отношения

Эффект «перелива» (stress spillover) — когда стресс на работе или из внешней жизни прямо влияет на качество взаимодействия с партнёром.

Исследования NIH показывают: высокий уровень кортизола (гормона стресса) связан с более негативным восприятием поведения партнёра. Мы становимся менее терпимыми и более реактивными.

## Пара как «буфер стресса»

Готтман обнаружил, что поддержка партнёра снижает физиологические маркеры стресса (уровень кортизола, артериальное давление) сильнее, чем любые другие методы.

Ключевое условие: партнёр должен **сначала выслушать**, а не сразу решать проблему.

## Четыре стадии выгорания (по Фрейденбергу)

1. Избыточный энтузиазм
2. Стагнация (работа перестаёт приносить удовлетворение)
3. Фрустрация
4. Апатия

Партнёр на 3-4 стадии кажется «холодным» или «отстранённым» — это симптом истощения, а не охлаждения чувств.

## Что помогает

- Вечерний ритуал «разгрузки» (15 минут, где каждый говорит о дне без советов)
- Физическое прикосновение снижает кортизол
- Общие восстанавливающие практики (прогулки, совместный ужин без гаджетов)
- Прямо говорить: «Я сейчас на нулях, мне нужно просто побыть рядом»''',
        'i18n': {
            'en': {
                'title': 'How Stress Destroys Relationships and What to Do About It',
                'brief': 'External stress — work, money, health — enters relationships. But a couple can become a buffer against stress, not an amplifier.',
                'body': '''## Stress "spills over" into relationships

The "stress spillover" effect — when stress from work or outside life directly affects the quality of interaction with your partner.

NIH research shows: high cortisol levels (the stress hormone) are linked to a more negative perception of a partner\'s behavior. We become less tolerant and more reactive.

## The couple as a "stress buffer"

Gottman found that partner support reduces physiological stress markers (cortisol levels, blood pressure) more than any other method.

Key condition: the partner must **first listen**, not immediately problem-solve.

## Four Stages of Burnout (Freudenberger)

1. Excessive enthusiasm
2. Stagnation (work stops being fulfilling)
3. Frustration
4. Apathy

A partner at stages 3–4 may seem "cold" or "distant" — this is a symptom of exhaustion, not cooling feelings.

## What helps

- An evening "decompression" ritual (15 minutes where each person talks about their day without advice)
- Physical touch lowers cortisol
- Shared restorative practices (walks, dinner together without devices)
- Saying directly: "I\'m running on empty right now, I just need you nearby"''',
            },
            'uz': {
                'title': "Stres munosabatlarni qanday buzadi va u bilan nima qilish kerak",
                'brief': "Tashqi stres — ish, pul, salomatlik — munosabatlarga kiradi. Ammo juftlik stresning kuchaytirgichi emas, buferga aylanishi mumkin.",
                'body': '''## Stres munosabatlarga «o\'tib ketadi»

«Stres o\'tishi» ta\'siri — ishdagi yoki tashqi hayotdagi stres sherik bilan o\'zaro ta\'sirning sifatiga bevosita ta\'sir qilganda.

NIH tadqiqotlari ko\'rsatadiki: yuqori kortizol darajasi (stres gormoni) sherik xatti-harakatini yanada salbiy idrok etish bilan bog\'liq. Biz kamroq toqatli va ko\'proq reaktiv bo\'lib qolamiz.

## Juftlik stresning «buferi» sifatida

Gottman sherik ko\'magining fiziologik stres ko\'rsatkichlarini (kortizol darajasi, qon bosimi) boshqa usullardan ko\'ra ko\'proq pasaytirishini aniqladi.

Asosiy shart: sherik **avval eshitishi** kerak, darhol muammoni hal qilishga o\'tmasligi kerak.

## To\'yinib ketishning to\'rtta bosqichi (Freudenberger)

1. Haddan tashqari g\'ayrat
2. Stagnatsiya (ish qoniqarli bo\'lishdan to\'xtaydi)
3. Frustrasiya
4. Apatiya

3-4 bosqichdagi sherik «sovuq» yoki «chetga tortgan» ko\'rinishi mumkin — bu his-tuyg\'ularning sovishining emas, charchoqning belgisidir.

## Nima yordam beradi

- Kechki «yukni tushirish» rituali (15 daqiqa, unda har bir kishi maslahat bermasdan kuni haqida gapiradi)
- Jismoniy teginish kortizolni kamaytiradi
- Birgalikdagi tiklovchi amaliyotlar (sayrlar, gadgetsiz birgalikdagi kechki ovqat)
- To\'g\'ridan-to\'g\'ri aytish: «Hozir bo\'sh qoldim, shunchaki yoningizda bo\'lishim kerak»''',
            },
            'uz_cyrl': {
                'title': "Стрес муносабатларни қандай бузади ва у билан нима қилиш керак",
                'brief': "Ташқи стрес — иш, пул, саломатлик — муносабатларга киради. Аммо жуфтлик стреснинг кучайтиргичи эмас, буферга айланиши мумкин.",
                'body': '''## Стрес муносабатларга «ўтиб кетади»

«Стрес ўтиши» таъсири — исhdаги ёки ташқи ҳаётдаги стрес шерик билан ўзаро таъсирнинг сифатига бевосита таъсир қилганда.

NIH тадқиқотлари кўрсатадики: юқори кортизол даражаси (стрес гормони) шерик хатти-ҳаракатини янада салбий идрок этиш билан боғлиқ. Биз камроқ тоқатли ва кўпроқ реактив бўлиб қоламиз.

## Жуфтлик стреснинг «buferi» сифатида

Готтман шерик кўмагининг физиологик стрес кўрсаткичларини (кортизол даражаси, қон босими) бошқа усуллардан кўра кўпроқ пасайтиришини аниқлади.

Асосий шарт: шерик **аввал эшитиши** керак, дарҳол муаммони ҳал қилишга ўтмаслиги керак.

## Тўйиниб кетишнинг тўртта босқичи (Фройденбергер)

1. Ҳаддан ташқари ғайрат
2. Стагнация (иш қониқарли бўлишдан тўхтайди)
3. Фрустрасия
4. Апатия

3-4 босқичдаги шерик «совуқ» ёки «четга тортган» кўриниши мумкин — бу ҳис-туйғуларнинг совишининг эмас, чарчоқнинг белгисидир.

## Нима ёрдам беради

- Кечки «юкни тушириш» rituali (15 дақиқа, унда ҳар бир киши маслаҳат бермасдан куни ҳақида гапиради)
- Жисмоний тегиниш кортизолни камайтиради
- Биргаликдаги тикловчи амалиётлар (сайрлар, гаджетсиз биргаликдаги кечки овқат)
- Тўғридан-тўғри айтиш: «Ҳозир бўш қолдим, шунчаки ёнингизда бўлишим керак»''',
            },
        },
        'read_time_minutes': 8,
        'difficulty': 'intermediate',
        'tags': ['стресс', 'выгорание', 'поддержка', 'кортизол'],
        'sources': ['NIH (National Institutes of Health)', 'APA (American Psychological Association)'],
        'order_index': 1,
    },

    # --- Воспитание детей ---
    {
        'slug': 'parenting-as-team',
        'category': 'parenting',
        'title': 'Воспитание как команда: как не потерять пару с рождением ребёнка',
        'brief': 'Исследования показывают резкое снижение удовлетворённости браком после рождения первого ребёнка. Как этого избежать.',
        'body': '''## Рождение ребёнка — кризис для пары

Исследования Готтмана показывают: у 67% пар удовлетворённость браком значительно снижается в первые три года после рождения ребёнка.

Это **нормально**, но не неизбежно.

## Что происходит

- Резко возрастает нагрузка и недосып
- Уменьшается время для пары
- Появляются разногласия в подходах к воспитанию
- Один из партнёров может чувствовать себя «исключённым»

## Три ключевых навыка

**1. Оставаться командой в разногласиях.**
Ребёнок не должен видеть, что родители подрывают авторитет друг друга. Разногласия обсуждайте без ребёнка.

**2. Защищать отношения как приоритет.**
Регулярное время вдвоём — не роскошь, а необходимость. Дети, выросшие в счастливых браках, психологически здоровее.

**3. Распределение нагрузки.**
Исследования показывают: ощущение несправедливого распределения домашних обязанностей — главный источник конфликтов у молодых родителей. Обсуждайте это открыто и регулярно.

## Стили воспитания (Диана Баумринд)

- **Авторитетный** (тёплый + требовательный) — оптимальный
- **Авторитарный** (холодный + требовательный)
- **Попустительский** (тёплый + нетребовательный)
- **Безразличный** (холодный + нетребовательный)

Важно, чтобы оба партнёра понимали, к какому стилю они склонны, и обсуждали подход.''',
        'i18n': {
            'en': {
                'title': 'Parenting as a Team: How Not to Lose the Couple After Having a Child',
                'brief': 'Research shows a sharp decline in marital satisfaction after the birth of the first child. How to avoid this.',
                'body': '''## The birth of a child is a crisis for the couple

Gottman\'s research shows: 67% of couples experience a significant decline in marital satisfaction within the first three years after having a child.

This is **normal**, but not inevitable.

## What happens

- Workload and sleep deprivation increase sharply
- Time for the couple diminishes
- Disagreements about parenting approaches arise
- One partner may feel "left out"

## Three Key Skills

**1. Stay a team through disagreements.**
Children should not see parents undermining each other\'s authority. Discuss disagreements away from the child.

**2. Protect the relationship as a priority.**
Regular time together as a couple is not a luxury — it is a necessity. Children raised in happy marriages are psychologically healthier.

**3. Distribute the load.**
Research shows: a sense of unfair distribution of household duties is the main source of conflict for young parents. Discuss this openly and regularly.

## Parenting Styles (Diana Baumrind)

- **Authoritative** (warm + demanding) — optimal
- **Authoritarian** (cold + demanding)
- **Permissive** (warm + undemanding)
- **Uninvolved** (cold + undemanding)

It is important for both partners to understand which style they tend toward and to discuss their approach.''',
            },
            'uz': {
                'title': "Jamoaviy tarbiya: farzand tug'ilgach juftlikni yo'qotmaslik",
                'brief': "Tadqiqotlar birinchi farzand tug'ilgandan keyin nikoh qoniqarliligi keskin pasayishini ko'rsatadi. Buning oldini qanday olish.",
                'body': '''## Farzand tug'ilishi juftlik uchun inqirozdir

Gottman tadqiqotlari ko\'rsatadiki: juftliklarning 67% da farzand tug'ilgandan keyingi dastlabki uch yil ichida nikoh qoniqarliligi sezilarli darajada pasayadi.

Bu **normal**, lekin muqarrar emas.

## Nima bo'ladi

- Yuk va uyqusizlik keskin ortadi
- Juftlik uchun vaqt qisqaradi
- Tarbiya yondashuvlaridagi kelishmovchiliklar paydo bo\'ladi
- Sherikdan biri «chetga qolgan» his qilishi mumkin

## Uch asosiy ko\'nikma

**1. Kelishmovchiliklarda ham jamoaviy bo\'lish.**
Bolalar ota-onaning bir-birining obro\'sini tushirishini ko\'rmasligi kerak. Kelishmovchiliklarni bola oldida emas, alohida muhokama qiling.

**2. Munosabatlarni ustuvorlik sifatida himoya qilish.**
Juftlik sifatida muntazam vaqt — hashamat emas, zaruriyat. Baxtli oilalarda katta bo\'lgan bolalar psixologik jihatdan sog\'lom.

**3. Yukni taqsimlash.**
Tadqiqotlar ko\'rsatadiki: uy vazifalarining nohaqona taqsimlanishi — yosh ota-onalardagi nizolarning asosiy manbai. Buni ochiq va muntazam muhokama qiling.

## Tarbiya uslublari (Diana Baumrind)

- **Vakolatli** (iliq + talab qiluvchi) — optimal
- **Avtoritar** (sovuq + talab qiluvchi)
- **Ruxsat beruvchi** (iliq + talab qilmaydigan)
- **Befarq** (sovuq + talab qilmaydigan)

Ikkala sherik ham qaysi uslubga moyil ekanligini tushunishi va yondashuvni muhokama qilishi muhim.''',
            },
            'uz_cyrl': {
                'title': "Жамоавий тарбия: фарзанд туғилгач жуфтликни йўқотмаслик",
                'brief': "Тадқиқотлар биринчи фарзанд туғилганидан кейин никоҳ қониқарлилиги кескин пасайишини кўрсатади. Бунинг олдини қандай олиш.",
                'body': '''## Фарзанд туғилиши жуфтлик учун инқироздир

Готтман тадқиқотлари кўрсатадики: жуфтликларнинг 67% да фарзанд туғилганидан кейинги дастлабки уч йил ичида никоҳ қониқарлилиги сезиларли даражада пасаяди.

Бу **нормал**, лекин муқаррар эмас.

## Нима бўлади

- Юк ва уйқусизлик кескин ортади
- Жуфтлик учун вақт қисқаради
- Тарбия ёндашувларидаги келишмовчиликлар пайдо бўлади
- Шерикдан бири «четга қолган» ҳис қилиши мумкин

## Уч асосий кўникма

**1. Келишмовчиликларда ҳам жамоавий бўлиш.**
Болалар ота-онанинг бир-бирининг обрўсини тушириши ни кўрмаслиги керак. Келишмовчиликларни бола олдида эмас, алоҳида муҳокама қилинг.

**2. Муносабатларни устуворлик сифатида ҳимоя қилиш.**
Жуфтлик сифатида мунтазам вақт — ҳашамат эмас, зарурият. Бахтли оилаларда катта бўлган болалар психологик жиҳатдан соғлом.

**3. Юкни тақсимлаш.**
Тадқиқотлар кўрсатадики: уй вазифаларининг нохакона тақсимланиши — ёш ота-оналардаги низоларнинг асосий манбаи. Буни очиқ ва мунтазам муҳокама қилинг.

## Тарбия услублари (Диана Баумринд)

- **Ваколатли** (илиқ + талаб қилувчи) — оптимал
- **Авторитар** (совуқ + талаб қилувчи)
- **Рухсат берувчи** (илиқ + талаб қилмайдиган)
- **Бефарқ** (совуқ + талаб қилмайдиган)

Иккала шерик ҳам қайси услубга мойил эканлигини тушуниши ва ёндашувни муҳокама қилиши муҳим.''',
            },
        },
        'read_time_minutes': 9,
        'difficulty': 'intermediate',
        'tags': ['дети', 'родительство', 'команда'],
        'sources': ['Джон Готтман', 'APA (American Psychological Association)'],
        'order_index': 1,
    },

    # --- Восстановление после кризиса ---
    {
        'slug': 'crisis-recovery-roadmap',
        'category': 'crisis_recovery',
        'title': 'Дорожная карта восстановления после семейного кризиса',
        'brief': 'Структурированный научный подход к восстановлению, основанный на исследованиях кризисной терапии пар.',
        'body': '''## Кризис — это не конец

Исследования показывают: пары, прошедшие через кризис и получившие поддержку, нередко сообщают о более глубоких и зрелых отношениях, чем до него.

## Фазы кризиса

**Острая фаза (0-2 месяца).** Шок, отрицание, сильные эмоции. Главная задача — не делать необратимых решений в этот период.

**Переходная фаза (2-6 месяцев).** Начало осмысления. Появляется возможность для разговора.

**Интеграция (6+ месяцев).** Создание новых договорённостей и смыслов.

## Три необходимых условия восстановления

**1. Безопасность.** Оба чувствуют, что могут говорить честно без атаки в ответ.

**2. Ответственность.** Каждый признаёт свою роль — не только виновный.

**3. Готовность к изменениям.** Не к «возврату как было», а к построению чего-то нового.

## Что не работает

- Пытаться «поговорить и решить» в острой фазе
- Ставить ультиматумы под давлением эмоций
- Привлекать третьих лиц (родственников) как «судей»
- Игнорировать кризис в надежде, что «само пройдёт»

## Когда нужен профессионал

Если один из партнёров: отказывается говорить, угрожает, находится в депрессии или тревожном расстройстве — обратитесь к семейному психологу.''',
        'i18n': {
            'en': {
                'title': 'A Roadmap for Recovery After a Family Crisis',
                'brief': 'A structured scientific approach to recovery, based on couples crisis therapy research.',
                'body': '''## A crisis is not the end

Research shows: couples who have gone through a crisis and received support often report deeper, more mature relationships than before.

## Phases of crisis

**Acute phase (0–2 months).** Shock, denial, strong emotions. The main task — do not make irreversible decisions during this period.

**Transitional phase (2–6 months).** Sense-making begins. The possibility of dialogue emerges.

**Integration (6+ months).** Creating new agreements and meanings.

## Three necessary conditions for recovery

**1. Safety.** Both feel they can speak honestly without being attacked.

**2. Responsibility.** Each acknowledges their role — not just the person who caused harm.

**3. Willingness to change.** Not a "return to how things were," but building something new.

## What doesn\'t work

- Trying to "talk it out and resolve it" in the acute phase
- Issuing ultimatums under emotional pressure
- Involving third parties (relatives) as "judges"
- Ignoring the crisis hoping it will "sort itself out"

## When professional help is needed

If one partner: refuses to talk, makes threats, is experiencing depression or an anxiety disorder — consult a family therapist.''',
            },
            'uz': {
                'title': "Oilaviy inqirozdan keyin tiklanish yo'l xaritasi",
                'brief': "Tiklanishga tizimli ilmiy yondashuv, juftliklar inqirozi terapiyasi tadqiqotlariga asoslangan.",
                'body': '''## Inqiroz — bu oxir emas

Tadqiqotlar ko\'rsatadiki: inqirozdan o\'tgan va yordam olgan juftliklar ko\'pincha undan oldingi munosabatlardan ko\'ra chuqurroq va balogat yetganroq munosabatlar haqida xabar berishadi.

## Inqiroz bosqichlari

**O\'tkir bosqich (0-2 oy).** Shok, inkor etish, kuchli hissiyotlar. Asosiy vazifa — bu davrda qaytib bo\'lmas qarorlar qabul qilmaslik.

**O\'tish bosqichi (2-6 oy).** Anglash boshlanadi. Suhbat imkoniyati paydo bo\'ladi.

**Integratsiya (6+ oy).** Yangi kelishuvlar va ma\'nolar yaratish.

## Tiklanish uchun uch zarur shart

**1. Xavfsizlik.** Ikkalasi ham hujumga uchrash qo\'rquvisiz halol gapira olishini his qiladi.

**2. Mas\'uliyat.** Har biri — faqat aybdor emas — o\'z rolini tan oladi.

**3. O\'zgarishga tayyorlik.** «Avvalgiday qaytish» emas, yangi narsa qurish.

## Nima ishlamaydi

- O\'tkir bosqichda «gaplashib hal qilish»ga urinish
- Hissiy bosim ostida ultimatum qo\'yish
- Uchinchi shaxslarni (qarindoshlarni) «hakam» sifatida jalb qilish
- «O\'zi o\'tar» deb inqirozni e\'tiborsiz qoldirish

## Mutaxassis yordami qachon kerak

Agar sherikdan biri: gapishdan bosh tortsa, tahdid qilsa, depressiya yoki xavotir buzilishi bilan kurashayotgan bo\'lsa — oila psixologiga murojaat qiling.''',
            },
            'uz_cyrl': {
                'title': "Оилавий инқироздан кейин тикланиш йўл харитаси",
                'brief': "Тикланишга тизимли илмий ёндашув, жуфтликлар инқирози терапияси тадқиқотларига асосланган.",
                'body': '''## Инқироз — бу охир эмас

Тадқиқотлар кўрсатадики: инқироздан ўтган ва ёрдам олган жуфтликлар кўпинча ундан олдинги муносабатлардан кўра чуқурроқ ва балоғат етганроқ муносабатлар ҳақида хабар беришади.

## Инқироз босқичлари

**Ўткир босқич (0-2 ой).** Шок, инкор этиш, кучли ҳиссиётлар. Асосий вазифа — бу даврда қайтиб бўлмас қарорлар қабул қилмаслик.

**Ўтиш босқичи (2-6 ой).** Англаш бошланади. Суҳбат имконияти пайдо бўлади.

**Интеграция (6+ ой).** Янги келишувлар ва маънолар яратиш.

## Тикланиш учун уч зарур шарт

**1. Хавфсизлик.** Иккаласи ҳам ҳужумга учраш қўрқувисиз ҳалол гапира олишини ҳис қилади.

**2. Масъулият.** Ҳар бири — фақат айбдор эмас — ўз ролини тан олади.

**3. Ўзгаришга тайёрлик.** «Аввалгидай қайтиш» эмас, янги нарса қуриш.

## Нима ишламайди

- Ўткир босқичда «гаплашиб ҳал қилиш»га уриниш
- Ҳиссий босим остида ультиматум қўйиш
- Учинчи шахсларни (қариндошларни) «ҳакам» сифатида жалб қилиш
- «Ўзи ўтар» деб инқирозни эьтиборсиз қолдириш

## Мутахассис ёрдами қачон керак

Агар шерикдан бири: гапишдан бош тортса, таҳдид қилса, депрессия ёки хавотир бузилиши билан курашаётган бўлса — оила психологига мурожаат қилинг.''',
            },
        },
        'read_time_minutes': 10,
        'difficulty': 'advanced',
        'tags': ['кризис', 'восстановление', 'терапия'],
        'sources': ['Джон Готтман', 'Джули Готтман', 'APA (American Psychological Association)'],
        'order_index': 1,
    },

    # --- Подготовка к браку ---
    {
        'slug': 'premarital-checklist',
        'category': 'marriage_prep',
        'title': '15 вопросов, которые нужно обсудить до брака',
        'brief': 'Исследования показывают: пары, обсудившие ключевые темы до брака, разводятся в 2 раза реже.',
        'body': '''## Зачем говорить об этом заранее

Большинство разводов происходит не из-за того, что пара не любила друг друга, а из-за того, что у партнёров оказались несовместимые ожидания, которые никто не озвучил.

## Блок 1: Дети

- Хотите ли вы детей? Сколько?
- Когда?
- Кто остаётся с ребёнком, если нужно выбрать карьеру?
- Каков ваш подход к воспитанию?

## Блок 2: Финансы

- Как будем управлять деньгами (раздельно / вместе / гибрид)?
- Кто ведёт семейный бюджет?
- Как относитесь к долгам?
- Какова финансовая цель на 5 лет?

## Блок 3: Карьера и быт

- Возможен ли переезд ради карьеры одного из вас?
- Как распределяется домашний труд?
- Что происходит, если один захочет не работать?

## Блок 4: Семьи и границы

- Как часто и в каком формате общаемся с родителями?
- Как принимать решения, если родители не согласны?
- Что делать в случае конфликта с родственниками?

## Блок 5: Ценности и смыслы

- Какова ваша религиозная / духовная позиция?
- Какими вы видите себя через 10 лет?
- Что для вас «счастливая семья»?

## Как проводить эти разговоры

- По одному блоку за раз
- В спокойной обстановке
- Без давления «правильного ответа»
- Цель — понять, не убедить''',
        'i18n': {
            'en': {
                'title': '15 Questions to Discuss Before Marriage',
                'brief': 'Research shows couples who discuss key topics before marriage divorce at half the rate.',
                'body': '''## Why talk about this in advance

Most divorces happen not because the couple didn\'t love each other, but because partners had incompatible expectations that no one voiced.

## Block 1: Children

- Do you want children? How many?
- When?
- Who stays home with the child if one must choose between career and family?
- What is your approach to parenting?

## Block 2: Finances

- How will we manage money (separately / together / hybrid)?
- Who manages the family budget?
- What is your attitude toward debt?
- What is the financial goal for the next 5 years?

## Block 3: Career and Home Life

- Is relocating for one partner\'s career a possibility?
- How is housework divided?
- What happens if one partner wants to stop working?

## Block 4: Extended Family and Boundaries

- How often and in what format do we interact with parents?
- How do we make decisions when parents disagree?
- What do we do in the event of conflict with relatives?

## Block 5: Values and Meaning

- What is your religious / spiritual position?
- Where do you see yourself in 10 years?
- What does "a happy family" mean to you?

## How to have these conversations

- One block at a time
- In a calm setting
- Without pressure to give "the right answer"
- Goal — to understand, not to persuade''',
            },
            'uz': {
                'title': "Nikohdan oldin muhokama qilish kerak bo'lgan 15 ta savol",
                'brief': "Tadqiqotlar shuni ko'rsatadiki, nikohdan oldin asosiy mavzularni muhokama qilgan juftliklar 2 marta kamroq ajrashadi.",
                'body': '''## Buni oldindan nima uchun muhokama qilish kerak

Ko\'pchilik ajrashishlar juftliklar bir-birini sevmaganligi uchun emas, balki sheriklar hech kim ovoz chiqarmaган mos kelmagan umidlarga ega bo\'lganligi uchun sodir bo\'ladi.

## 1-blok: Bolalar

- Siz farzand ko\'rishni xohlaysizmi? Nechta?
- Qachon?
- Karera va oila o\'rtasida tanlov qilish kerak bo\'lsa, bola bilan kim qoladi?
- Tarbiyaga yondashuvingiz qanday?

## 2-blok: Moliya

- Pulni qanday boshqaramiz (alohida / birgalikda / gibrid)?
- Oila byudjetini kim boshqaradi?
- Qarzga munosabatingiz qanday?
- 5 yillik moliyaviy maqsad nima?

## 3-blok: Karyera va maishiy turmush

- Sherikdan birining karerasi uchun ko\'chish mumkinmi?
- Uy ishlari qanday taqsimlanadi?
- Agar biri ishlamaslikni xohlasa nima bo\'ladi?

## 4-blok: Katta oila va chegaralar

- Ota-onalar bilan qanchalik tez-tez va qanday formatda muloqot qilamiz?
- Ota-onalar kelishmaganda qarorlarni qanday qabul qilamiz?
- Qarindoshlar bilan ziddiyat yuzaga kelsa nima qilamiz?

## 5-blok: Qadriyatlar va mazmun

- Diniy/ma\'naviy pozitsiyangiz qanday?
- 10 yil o\'tib o\'zingizni qanday ko\'rasiz?
- Siz uchun «baxtli oila» nima?

## Bu suhbatlarni qanday o\'tkazish

- Bir vaqtda bitta blok
- Tinch muhitda
- «To\'g\'ri javob» berishga bosim bo\'lmasdan
- Maqsad — tushunish, ishontirish emas''',
            },
            'uz_cyrl': {
                'title': "Никоҳдан олдин муҳокама қилиш керак бўлган 15 та савол",
                'brief': "Тадқиқотлар шуни кўрсатадики, никоҳдан олдин асосий мавзуларни муҳокама қилган жуфтликлар 2 марта камроқ ажрашади.",
                'body': '''## Буни олдиндан нима учун муҳокама қилиш керак

Кўпчилик ажрашишлар жуфтликлар бир-бирини севмаганлиги учун эмас, балки шериклар ҳеч ким овоз чиқармаган мос келмаган умидларга эга бўлганлиги учун содир бўлади.

## 1-блок: Болалар

- Сиз фарзанд кўришни хоҳлайсизми? Нечта?
- Қачон?
- Карера ва оила ўртасида танлов қилиш керак бўлса, бола билан ким қолади?
- Тарбияга ёндашувингиз қандай?

## 2-блок: Молия

- Пулни қандай бошқарамиз (алоҳида / биргаликда / гибрид)?
- Оила бюджетини ким бошқаради?
- Қарзга муносабатингиз қандай?
- 5 йиллик молиявий мақсад нима?

## 3-блок: Карера ва маиший турмуш

- Шерикдан бирининг карерси учун кўчиш мумкинми?
- Уй ишлари қандай тақсимланади?
- Агар бири ишламасликни хоҳласа нима бўлади?

## 4-блок: Катта оила ва чегаралар

- Ота-оналар билан қанчалик тез-тез ва қандай форматда мулоқот қиламиз?
- Ота-оналар келишмаганда қарорларни қандай қабул қиламиз?
- Қариндошлар билан зиддият юзага келса нима қиламиз?

## 5-блок: Қадриятлар ва маzmун

- Диний/маъnaviy позицияngиz қandай?
- 10 йил ўтиб ўзingизни қандай кўрасиз?
- Сиз учун «бахтли оила» нима?

## Бу суҳбатларни қандай ўтказиш

- Бир вақтда битта блок
- Тинч муҳитда
- «Тўғри жавоб» беришга босим бўлмасдан
- Мақсад — тушуниш, ишонтириш эмас''',
            },
        },
        'read_time_minutes': 10,
        'difficulty': 'beginner',
        'tags': ['подготовка к браку', 'ожидания', 'договорённости'],
        'sources': ['APA (American Psychological Association)', 'Journal of Marriage and Family'],
        'order_index': 1,
    },

    # --- Традиции ---
    {
        'slug': 'family-rituals-research',
        'category': 'traditions',
        'title': 'Семейные ритуалы: наука о том, зачем они нужны',
        'brief': 'Исследования показывают: семьи с регулярными ритуалами имеют более крепкую идентичность и лучшие отношения.',
        'body': '''## Что такое семейный ритуал

Ритуал — это повторяющееся действие, наполненное смыслом. Не просто «мы ужинаем вместе», а «наш семейный ужин, где мы рассказываем о лучшем событии дня».

## Почему ритуалы важны

Исследования Journal of Marriage and Family показывают:
- Пары с регулярными ритуалами оценивают удовлетворённость браком выше
- Дети в семьях с ритуалами демонстрируют лучшую эмоциональную регуляцию
- Ритуалы создают ощущение «мы» — семейную идентичность

## Три типа семейных ритуалов

**Ритуалы связи** (ежедневные): утренний кофе вдвоём, вечерний разговор «о дне», совместная прогулка.

**Ритуалы праздника**: как отмечаете дни рождения, годовщины, небольшие победы.

**Ритуалы перехода**: как провожаете в дорогу, встречаете после разлуки, отмечаете окончание трудного периода.

## Как создать ритуал

1. Выберите момент (утро/вечер, еженедельно)
2. Дайте ему название — это делает его реальным
3. Зафиксируйте «правила» (что делаем, чего не делаем — телефоны, например)
4. Повторяйте, даже если кажется бессмысленным в трудные дни''',
        'i18n': {
            'en': {
                'title': 'Family Rituals: The Science of Why They Matter',
                'brief': 'Research shows families with regular rituals have stronger identity and better relationships.',
                'body': '''## What is a family ritual

A ritual is a repeated action filled with meaning. Not just "we have dinner together," but "our family dinner where we each share the best moment of the day."

## Why rituals matter

Journal of Marriage and Family research shows:
- Couples with regular rituals rate marital satisfaction higher
- Children in families with rituals demonstrate better emotional regulation
- Rituals create a sense of "us" — a family identity

## Three Types of Family Rituals

**Connection rituals** (daily): morning coffee together, an evening talk "about the day," a shared walk.

**Celebration rituals**: how you mark birthdays, anniversaries, small victories.

**Transition rituals**: how you say goodbye when someone leaves, how you welcome each other home, how you mark the end of a hard period.

## How to create a ritual

1. Choose a moment (morning/evening, weekly)
2. Give it a name — this makes it real
3. Set the "rules" (what you do, what you don\'t — phones, for example)
4. Repeat it, even if it feels pointless on hard days''',
            },
            'uz': {
                'title': "Oilaviy rituallar: nima uchun ular kerakligi haqida ilm",
                'brief': "Tadqiqotlar shuni ko'rsatadiki, muntazam rituallarga ega oilalar kuchliroq identifikatsiya va yaxshiroq munosabatlarga ega.",
                'body': '''## Oilaviy ritual nima

Ritual — mazmunli takroriy harakat. Shunchaki «biz birgalikda kechki ovqat yeymiz» emas, balki «kunning eng yaxshi lahzasini aytadigan bizning oilaviy kechki ovqatimiz».

## Nima uchun rituallar muhim

Journal of Marriage and Family tadqiqotlari ko\'rsatadiki:
- Muntazam rituallarga ega juftliklar nikoh qoniqarligini yuqoriroq baholaydi
- Rituallari bor oilalardagi bolalar hissiy tartibga solishning yaxshiroq ko\'nikmalarini namoyish etadi
- Rituallar «biz» hissini yaratadi — oilaviy identifikatsiya

## Oilaviy rituallarning uch turi

**Bog\'lanish rituallari** (kundalik): ikkalangiz birgalikda ertalabki qahva, «kun haqida» kechki suhbat, birgalikdagi sayr.

**Nishon rituallari**: tug\'ilgan kunlar, yillik to\'ylar, kichik g\'alabalarni qanday nishonlaysiz.

**O\'tish rituallari**: safarga jo\'natish, qaytganda kutib olish, qiyin davrning tugashini nishonlash.

## Ritual qanday yaratish

1. Bir lahza tanlang (ertalab/kechqurun, haftalik)
2. Unga nom bering — bu uni haqiqiy qiladi
3. «Qoidalar»ni belgilang (nima qilamiz, nima qilmaymiz — masalan, telefonlar)
4. Qiyin kunlarda ham takrorlang''',
            },
            'uz_cyrl': {
                'title': "Оилавий ритуаллар: нима учун улар кераклиги ҳақида илм",
                'brief': "Тадқиқотлар шуни кўрсатадики, мунтазам ритуалларга эга оилалар кучлироқ идентификация ва яхшироқ муносабатларга эга.",
                'body': '''## Оилавий ритуал нима

Ритуал — маzmунли такрорий ҳаракат. Шунчаки «биз биргаликда кечки овқат еймиз» эмас, балки «куннинг энг яхши лаҳзасини айтадиган бизнинг оилавий кечки овқатимиз».

## Нима учун ритуаллар муҳим

Journal of Marriage and Family тадқиқотлари кўрсатадики:
- Мунтазам ритуалларга эга жуфтликлар никоҳ қониқарлигини юқорироқ баҳолайди
- Ритуаллари бор оилалардаги болалар ҳиссий тартибга солишнинг яхшироқ кўниkmаларini намойиш этади
- Ритуаллар «биз» ҳиссини яратади — оилавий идентификация

## Оилавий ритуалларнинг уч тури

**Боғланиш ритуаллари** (кундалик): иккалангиз биргаликда эрталабки қаҳва, «кун ҳақида» кечки суҳбат, биргаликдаги сайр.

**Нишон ритуаллари**: туғилган кунлар, йиллик тўйлар, кичик ғалабаларни қандай нишонлайсиз.

**Ўтиш ритуаллари**: сафарга жўнатиш, қайтганда кутиб олиш, қийин даврнинг тугашини нишонлаш.

## Ритуал қандай яратиш

1. Бир лаҳза танланг (эрталаб/кечқурун, ҳафталик)
2. Унга ном беринг — бу уни ҳақиқий қилади
3. «Қоидалар»ни белгиланг (нима қиламиз, нима қилмаймиз — масалан, телефонлар)
4. Қийин кунларда ҳам такрорланг''',
            },
        },
        'read_time_minutes': 7,
        'difficulty': 'beginner',
        'tags': ['традиции', 'ритуалы', 'идентичность'],
        'sources': ['Journal of Marriage and Family', 'Джон Готтман'],
        'order_index': 1,
    },
]

TRAININGS = [
    {
        'slug': 'active-listening-training',
        'skill_type': 'active_listening',
        'title': 'Тренировка активного слушания',
        'description': 'Освоить технику полного присутствия в разговоре с партнёром, научиться отражать чувства и содержание.',
        'theory': '''## Что такое активное слушание

Активное слушание — это не просто молчание. Это навык полного присутствия, при котором вы не только слышите слова, но и воспринимаете эмоциональное состояние партнёра.

**Четыре шага:**
1. **Телесное присутствие** — отложить телефон, повернуться лицом, поддерживать контакт глаз
2. **Отражение содержания** — перефразировать услышанное своими словами
3. **Отражение эмоций** — назвать то, что, кажется, чувствует партнёр
4. **Проверка** — спросить, правильно ли вы поняли

Исследования показывают: один из главных источников конфликтов в паре — ощущение «меня не слышат». Этот навык снижает количество конфликтов на 40-60%.''',
        'exercise_instruction': '''## Упражнение «Зеркало»

**Продолжительность:** 15-20 минут
**Участники:** оба партнёра

### Шаги:

**1. Выберите тему** (не конфликтную). Например: «Расскажи, как прошёл твой день» или «Что тебя сейчас больше всего беспокоит?»

**2. Говорящий** рассказывает 2-3 минуты без перебиваний.

**3. Слушающий** делает следующее:
- Не перебивает и не готовит ответ
- После окончания говорит: «Я услышал, что ты... [содержание]. Похоже, ты при этом чувствуешь... [эмоция]. Я правильно понял?»

**4. Говорящий** подтверждает или поправляет.

**5. Поменяйтесь ролями.**

### Правила:
- Слушающий не оценивает, не советует, не объясняет
- Если не знаете, какую эмоцию назвать, спросите: «Что ты при этом чувствовал?»''',
        'completion_check': 'Вы выполнили упражнение, если оба партнёра почувствовали, что их услышали и поняли. Спросите друг друга: "Ты чувствовал себя услышанным?" Если да — упражнение выполнено.',
        'i18n': {
            'en': {
                'title': 'Active Listening Training',
                'description': 'Master the technique of full presence in conversation with your partner, learn to reflect feelings and content.',
                'theory': '''## What is active listening

Active listening is not just staying quiet. It is the skill of full presence, in which you not only hear the words but also perceive your partner\'s emotional state.

**Four steps:**
1. **Physical presence** — put down the phone, turn to face each other, maintain eye contact
2. **Reflecting content** — paraphrase what you heard in your own words
3. **Reflecting emotions** — name what your partner seems to be feeling
4. **Checking** — ask if you understood correctly

Research shows: one of the main sources of conflict in a couple is the feeling of "I\'m not being heard." This skill reduces conflicts by 40–60%.''',
                'exercise_instruction': '''## "Mirror" Exercise

**Duration:** 15–20 minutes
**Participants:** both partners

### Steps:

**1. Choose a topic** (non-conflictual). For example: "Tell me how your day went" or "What\'s worrying you most right now?"

**2. The speaker** talks for 2–3 minutes without interruption.

**3. The listener** does the following:
- Does not interrupt or prepare a response
- After the speaker finishes, says: "I heard that you... [content]. It seems like you feel... [emotion]. Did I understand correctly?"

**4. The speaker** confirms or corrects.

**5. Switch roles.**

### Rules:
- The listener does not evaluate, advise, or explain
- If you don\'t know what emotion to name, ask: "What were you feeling about that?"''',
                'completion_check': 'You have completed the exercise if both partners felt heard and understood. Ask each other: "Did you feel heard?" If yes — the exercise is complete.',
            },
            'uz': {
                'title': "Faol tinglash trenirovkasi",
                'description': "Sherik bilan suhbatda to'liq hozirlik texnikasini o'zlashtiring, hissiyotlar va mazmunni aks ettirishni o'rganing.",
                'theory': '''## Faol tinglash nima

Faol tinglash — shunchaki jim turish emas. Bu to\'liq hozirlik ko\'nikmasi bo\'lib, unda siz nafaqat so\'zlarni eshitasiz, balki sherikingizning hissiy holatini ham idrok etasiz.

**To\'rtta qadam:**
1. **Jismoniy hozirlik** — telefonni qo\'ying, yuzma-yuz o\'tiring, ko\'z aloqasini saqlang
2. **Mazmunni aks ettirish** — eshitganingizni o\'z so\'zlaringiz bilan qayta aytib bering
3. **Hissiyotlarni aks ettirish** — sherikingiz qanday his qilayotganga o\'xshashini ayting
4. **Tekshirish** — to\'g\'ri tushunganingizni so\'rang

Tadqiqotlar ko\'rsatadiki: juftlikdagi nizolarning asosiy manbalaridan biri «meni eshitmayapti» hissidir. Bu ko\'nikma nizolarni 40-60% ga kamaytiradi.''',
                'exercise_instruction': '''## «Ko\'zgu» mashqi

**Davomiyligi:** 15-20 daqiqa
**Ishtirokchilar:** ikkala sherik

### Qadamlar:

**1. Mavzu tanlang** (nizosiz). Masalan: «Kuning qanday o\'tdi?» yoki «Hozir sizni eng ko\'p nima bezovta qilmoqda?»

**2. Gapiruvchi** 2-3 daqiqa to\'xtatilmasdan gapiradi.

**3. Tinglovchi** quyidagilarni qiladi:
- To\'xtatmaydi va javob tayyorlamaydi
- Gapiruvchi tugatgandan so\'ng aytadi: «Eshitdim, siz... [mazmun]. O\'ylaymanki, siz... [hissiyot] his qilyapsiz. To\'g\'ri tushundimmi?»

**4. Gapiruvchi** tasdiqlaydi yoki tuzatadi.

**5. Rollarni almashing.**

### Qoidalar:
- Tinglovchi baholamaydi, maslahat bermaydi, tushuntirmaydi
- Qaysi hissiyotni aytishni bilmasangiz, so\'rang: «Bu haqda nima his qildingiz?»''',
                'completion_check': "Agar ikkala sherik ham eshitilgan va tushunilgan his qilsa, mashq bajarilgan. Bir-biridan so'rang: «O'zingizni eshitilgan his qildingizmi?» Agar ha — mashq bajarildi.",
            },
            'uz_cyrl': {
                'title': "Фаол тинглаш тренировкаси",
                'description': "Шерик билан суҳбатда тўлиқ ҳозирлик техникасини ўзлаштиринг, ҳиссиётлар ва мазмунни акс эттиришни ўрганинг.",
                'theory': '''## Фаол тинглаш нима

Фаол тинглаш — шунчаки жим туриш эмас. Бу тўлиқ ҳозирлик кўниkmаси бўлиб, унда сиз нафақат сўзларни эшитасиз, балки шерикингизнинг ҳиссий ҳолатини ҳам идрок этасиз.

**Тўртта қадам:**
1. **Жисмоний ҳозирлик** — телефонни қўйинг, юзма-юз ўтиринг, кўз алоқасини сақланг
2. **Мазмунни акс эттириш** — эшитганингизни ўз сўзларingиз билан қайта айтиб беринг
3. **Ҳиссиётларни акс эттириш** — шерикингиз қандай ҳис қилаётганга ўхшашини айтинг
4. **Текшириш** — тўғри тушунганингизни сўранг

Тадқиқотлар кўрсатадики: жуфтликдаги низоларнинг асосий манбаларидан бири «мени эшитмаяпти» ҳиссидир. Бу кўникма низоларни 40-60% га камайтиради.''',
                'exercise_instruction': '''## «Кўзгу» машқи

**Давомийлиги:** 15-20 дақиқа
**Иштирокчилар:** иккала шерик

### Қадамлар:

**1. Мавзу танланг** (низосиз). Масалан: «Кунинг қандай ўтди?» ёки «Ҳозир сизни энг кўп нима безовта қилмоқда?»

**2. Гапирувчи** 2-3 дақиқа тўхтатилмасдан гапиради.

**3. Тингловчи** қуйидагиларни қилади:
- Тўхтатмайди ва жавоб тайёрламайди
- Гапирувчи тугатгандан сўнг айтади: «Эшитдим, сиз... [мазмун]. Ўйлайманки, сиз... [ҳиссиёт] ҳис қиляпсиз. Тўғри тушундимми?»

**4. Гапирувчи** тасдиқлайди ёки тузатади.

**5. Ролларни алмашинг.**

### Қоидалар:
- Тингловчи баҳоламайди, маслаҳат бермайди, тушунтирмайди
- Қайси ҳиссиётни айтишни билмасangиз, сўранг: «Бу ҳақда нима ҳис қилдингиз?»''',
                'completion_check': "Агар иккала шерик ҳам эшитилган ва тушунилган ҳис қилса, машқ бажарилган. Бир-биридан сўранг: «Ўзингизни эшитилган ҳис қилдингизми?» Агар ҳа — машқ бажарилди.",
            },
        },
        'duration_minutes': 20,
        'difficulty': 'beginner',
        'order_index': 1,
    },
    {
        'slug': 'emotion-management-training',
        'skill_type': 'emotion_management',
        'title': 'Управление эмоциями в конфликте',
        'description': 'Научиться распознавать эмоциональное перевозбуждение и использовать техники саморегуляции до и во время разговора.',
        'theory': '''## Почему эмоции «захватывают» нас

Когда пульс превышает 100 ударов в минуту, префронтальная кора (отвечающая за рациональное мышление) отключается. Миндалина берёт управление — это называется «амигдала-хайджекинг».

В этом состоянии мы:
- Перестаём слышать партнёра
- Говорим то, о чём потом сожалеем
- Видим угрозу там, где её нет

**Ключевой принцип:** нельзя вести продуктивный разговор, когда вы в состоянии перевозбуждения.

## Окно толерантности

Это зона, в которой человек может думать, чувствовать и общаться одновременно. За её пределами — либо гиперактивация (паника, агрессия), либо гипоактивация (оцепенение, диссоциация).

Задача — научиться оставаться в этом окне или возвращаться в него.

## Три метода саморегуляции

**1. Физиологический вздох** (Stanford): медленный двойной вдох через нос + долгий выдох через рот. Активирует парасимпатическую нервную систему.

**2. STOP:** Stop (остановись) → Take a breath (дыши) → Observe (замечай) → Proceed (продолжай).

**3. Пауза:** договоритесь с партнёром о кодовом слове для паузы. Пауза — минимум 20 минут, без «прокручивания» ситуации.''',
        'exercise_instruction': '''## Упражнение «Термометр эмоций»

**Продолжительность:** 15 минут (можно делать индивидуально)

### Часть 1: Составьте свою карту (10 мин)

Возьмите лист и запишите ответы:

1. Какие ситуации с партнёром обычно запускают моё перевозбуждение? (назовите 3-5)
2. Как я понимаю, что начинаю перегреваться? (телесные сигналы: учащённое дыхание, напряжение в теле, жар)
3. Что мне помогает остыть? (пауза, вода, прогулка, дыхание)

### Часть 2: Практика физиологического вздоха (5 мин)

1. Сделайте обычный вдох
2. Сразу за ним — ещё один короткий «дополнительный» вдох через нос
3. Медленный, долгий выдох через рот (в 2 раза длиннее вдохов)
4. Повторите 5 раз

Замерьте пульс до и после. Большинство людей отмечают снижение на 5-10 ударов.

### Договорённость с партнёром

Поговорите о кодовом слове для паузы и о том, как вы вернётесь к разговору после паузы.''',
        'completion_check': 'Упражнение выполнено, если вы составили карту своих триггеров и попрактиковали физиологический вздох минимум 5 раз. Бонус: поделитесь своей картой с партнёром.',
        'i18n': {
            'en': {
                'title': 'Emotion Management in Conflict',
                'description': 'Learn to recognize emotional flooding and use self-regulation techniques before and during difficult conversations.',
                'theory': '''## Why emotions "take over"

When your heart rate exceeds 100 beats per minute, the prefrontal cortex (responsible for rational thinking) shuts down. The amygdala takes over — this is called "amygdala hijacking."

In this state we:
- Stop hearing our partner
- Say things we regret later
- Perceive threat where there is none

**Key principle:** you cannot have a productive conversation when you are flooded.

## The Window of Tolerance

This is the zone in which a person can think, feel, and communicate simultaneously. Outside it — either hyper-activation (panic, aggression) or hypo-activation (numbness, dissociation).

The goal is to learn to stay within this window or return to it.

## Three Self-Regulation Methods

**1. Physiological sigh** (Stanford): a slow double inhale through the nose + a long exhale through the mouth. Activates the parasympathetic nervous system.

**2. STOP:** Stop → Take a breath → Observe → Proceed.

**3. Pause:** agree with your partner on a code word for a pause. The pause — at minimum 20 minutes, without "replaying" the situation.''',
                'exercise_instruction': '''## "Emotion Thermometer" Exercise

**Duration:** 15 minutes (can be done individually)

### Part 1: Create your own map (10 min)

Take a sheet of paper and write your answers:

1. Which situations with my partner usually trigger my flooding? (name 3–5)
2. How do I know I\'m starting to overheat? (physical signals: rapid breathing, body tension, feeling hot)
3. What helps me cool down? (pause, water, a walk, breathing)

### Part 2: Practice the physiological sigh (5 min)

1. Take a normal breath in
2. Immediately take one more short "top-up" breath through the nose
3. A slow, long exhale through the mouth (twice as long as the inhales)
4. Repeat 5 times

Measure your pulse before and after. Most people notice a drop of 5–10 beats.

### Agreement with your partner

Talk about a code word for a pause and how you will return to the conversation after the pause.''',
                'completion_check': 'The exercise is complete if you created a map of your triggers and practiced the physiological sigh at least 5 times. Bonus: share your map with your partner.',
            },
            'uz': {
                'title': "Nizoda hissiyotlarni boshqarish",
                'description': "Hissiy to'lib toshishni tanishni va og'ir suhbatlardan oldin va paytida o'z-o'zini tartibga solish texnikalaridan foydalanishni o'rganing.",
                'theory': '''## Nima uchun hissiyotlar bizni «egallab oladi»

Puls minutiga 100 zarbadan oshganda, prefrontal po\'stloq (ratsional fikrlash uchun mas\'ul) o\'chadi. Amigdala boshqaruvni qo\'lga oladi — bu «amigdala o\'g\'rilik qilishi» deyiladi.

Bu holatda biz:
- Sherikni eshitishni to\'xtatamiz
- Keyinchalik afsus qiladigan narsalar aytamiz
- Xavf yo\'q joyda xavf ko\'ramiz

**Asosiy tamoyil:** to\'lib toshgan holatda samarali suhbat olib borish mumkin emas.

## Tolerantlik oynasi

Bu inson bir vaqtda fikrlashi, his qilishi va muloqot qilishi mumkin bo\'lgan zona. Undan tashqarida — yoki giperaktivatsiya (vahima, agressiya) yoki gipoaktivatsiya (uyushib qolish, dissotsiatsiya).

Maqsad — bu oynanav ichida qolishni yoki unga qaytishni o\'rganish.

## O\'z-o\'zini tartibga solishning uch usuli

**1. Fiziologik xo\'rsinish** (Stanford): burun orqali sekin ikki marta nafas olish + og\'iz orqali uzun nafas chiqarish. Parasimpatik asab tizimini faollashtiradi.

**2. STOP:** To\'xta → Nafas ol → Kuzat → Davom et.

**3. Tanaffus:** sherik bilan tanaffus uchun shifr so\'z haqida kelishing. Tanaffus — kamida 20 daqiqa, vaziyatni «qayta o\'ynamay».''',
                'exercise_instruction': '''## «Hissiyot termometri» mashqi

**Davomiyligi:** 15 daqiqa (alohida bajarilishi mumkin)

### 1-qism: O\'z xaritangizni tuzing (10 daqiqa)

Bir varaq oling va javoblarni yozing:

1. Sherik bilan qanday vaziyatlar odatda mening to\'lib toshishimni keltirib chiqaradi? (3-5 ta ayting)
2. Men qizib ketayotganimni qanday tushunaman? (jismoniy signallar: tezlashgan nafas, tana tarangligi, issiqlik)
3. Menga sovish uchun nima yordam beradi? (tanaffus, suv, sayr, nafas olish)

### 2-qism: Fiziologik xo\'rsinishni mashq qiling (5 daqiqa)

1. Oddiy nafas oling
2. Darhol burun orqali yana bir qisqa «qo\'shimcha» nafas oling
3. Og\'iz orqali sekin, uzun nafas chiqaring (nafas olishlardan 2 marta uzunroq)
4. 5 marta takrorlang

Oldin va keyin pulsni o\'lchang. Ko\'pchilik 5-10 zarba kamayishini his qiladi.

### Sherik bilan kelishuv

Tanaffus uchun shifr so\'z va tanaffusdan keyin suhbatga qanday qaytishingiz haqida gaplashing.''',
                'completion_check': "Mashq bajarildi, agar siz o'z triggerlaringiz xaritasini tuzgan bo'lsangiz va fiziologik xo'rsinishni kamida 5 marta mashq qilgan bo'lsangiz. Bonus: xaritangizni sherik bilan ulashing.",
            },
            'uz_cyrl': {
                'title': "Низода ҳиссиётларни бошқариш",
                'description': "Ҳиссий тўлиб тошишни танишни ва оғир суҳбатлардан олдин ва пайтида ўз-ўзини тартибга солиш техникаларидан фойдаланишни ўрганинг.",
                'theory': '''## Нима учун ҳиссиётлар бизни «эгаллаб олади»

Пулс дақиқасига 100 зарбадан ошганда, префронтал пўстлоқ (рационал фикрлаш учун масъул) ўчади. Амигдала бошқарувни қўлга олади — бу «амигдала ўғриlик қилиши» дейилади.

Бу ҳолатда биз:
- Шерикни эшитишни тўхтатамиз
- Кейинчалик афсус қиладиган нарсалар айтамиз
- Хавф йўқ жойда хавф кўрамиз

**Асосий тамойил:** тўлиб тошган ҳолатда самарали суҳбат олиб бориш мумкин эмас.

## Толерантлик ойнаси

Бу инсон бир вақтда фикрлаши, ҳис қилиши ва мулоқот қилиши мумкин бўлган zona. Ундан ташқарида — ёки гиперактивация (ваҳима, агрессия) ёки гипоактивация (уюшиб қолиш, диссоциация).

Мақсад — бу oynaнинг ичида қолишни ёки унга қайтишни ўрганиш.

## Ўз-ўзини тартибга солишнинг уч усули

**1. Физиологик хўрсиниш** (Stanford): бурун орқали секин икки марта нафас олиш + оғиз орқали узун нафас чиқариш. Парасимпатик асаб тизимини фаоллаштиради.

**2. STOP:** Тўхта → Нафас ол → Кузат → Давом эт.

**3. Танаффус:** шерик билан танаффус учун шифр сўз ҳақида келишинг. Танаффус — камида 20 дақиқа, вазиятни «қайта ўйнамай».''',
                'exercise_instruction': '''## «Ҳиссиёт термометри» машқи

**Давомийлиги:** 15 дақиқа (алоҳида бажарилиши мумкин)

### 1-қисм: Ўз харитангизни тузинг (10 дақиқа)

Бир варақ олинг ва жавобларни ёзинг:

1. Шерик билан қандай вазиятлар одатда менинг тўлиб тошишимни келтириб чиқаради? (3-5 та айтинг)
2. Мен қизиб кетаётганимни қандай тушунаман? (жисмоний сигналлар: тезлашган нафас, тана таранглиги, иссиқлик)
3. Менга совиш учун нима ёрдам беради? (танаффус, сув, сайр, нафас олиш)

### 2-қисм: Физиологик хўрсинишни машқ қилинг (5 дақиқа)

1. Оддий нафас олинг
2. Дарҳол бурун орқали яна бир қисқа «қўшимча» нафас олинг
3. Оғиз орқали секин, узун нафас чиқаринг (нафас олишлардан 2 марта узунроқ)
4. 5 марта такрорланг

Олдин ва кейин пулсни ўлчанг. Кўпчилик 5-10 зарба камайишини ҳис қилади.

### Шерик билан келишув

Танаффус учун шифр сўз ва танаффусдан кейин суҳбатга қандай қайтишингиз ҳақида гаплашинг.''',
                'completion_check': "Машқ бажарилди, агар сиз ўз тригgerларингиз харитасини тузган бўлсангиз ва физиологик хўрсинишни камида 5 марта машқ қилган бўлсангиз. Бонус: харитангизни шерик билан улашинг.",
            },
        },
        'duration_minutes': 15,
        'difficulty': 'beginner',
        'order_index': 2,
    },
    {
        'slug': 'gratitude-training',
        'skill_type': 'gratitude',
        'title': 'Навык благодарности в паре',
        'description': 'Практика регулярной, конкретной благодарности — одна из самых простых и мощных техник укрепления отношений.',
        'theory': '''## Почему благодарность работает

Исследования Мартина Селигмана (позитивная психология) и Джона Готтмана показывают: соотношение позитивных и негативных взаимодействий 5:1 предсказывает счастливые отношения.

Это называется «Магическое соотношение Готтмана».

## Нейронаука благодарности

Когда мы выражаем или получаем благодарность:
- Выделяется дофамин (вознаграждение)
- Снижается уровень кортизола
- Активируется префронтальная кора

**Важный нюанс:** привычка замечать хорошее требует сознательного усилия, потому что мозг эволюционно настроен на негативное (negativity bias).

## Три правила эффективной благодарности

1. **Конкретность.** «Спасибо, что вчера вечером помыл посуду, мне не нужно было об этом думать» лучше, чем «Ты такой заботливый».

2. **Личный смысл.** «Для меня это важно, потому что...»

3. **Регулярность.** Лучше маленькое ежедневно, чем большое раз в месяц.''',
        'exercise_instruction': '''## Упражнение «Три конкретных спасибо»

**Продолжительность:** 5-7 минут (ежедневно в течение недели)

### Шаги:

Каждый вечер или утро, по очереди:

**1.** Назовите одно конкретное действие партнёра, за которое вы благодарны.
Формула: «Я хочу поблагодарить тебя за [конкретное действие]. Для меня это [что это значит лично для тебя].»

Пример: «Я хочу поблагодарить тебя за то, что ты вчера забрал детей, хотя был уставший. Для меня это значило, что я смогла закончить работу без стресса.»

**2. Запрет:** не добавлять «но» после благодарности.

**3. Принимающий** отвечает только: «Спасибо, что заметил. Это приятно слышать.»

### Вариант: «Письмо благодарности»

Раз в неделю напишите партнёру короткое письмо (5-10 предложений) о том, что вы в нём цените.''',
        'completion_check': 'Выполняйте упражнение 7 дней подряд. В конце недели обсудите: изменилось ли что-то в атмосфере между вами?',
        'i18n': {
            'en': {
                'title': 'Gratitude Skill in a Couple',
                'description': 'The practice of regular, specific gratitude is one of the simplest and most powerful techniques for strengthening a relationship.',
                'theory': '''## Why gratitude works

Research by Martin Seligman (positive psychology) and John Gottman shows: a ratio of positive to negative interactions of 5:1 predicts happy relationships.

This is called "Gottman\'s Magic Ratio."

## The Neuroscience of Gratitude

When we express or receive gratitude:
- Dopamine is released (reward)
- Cortisol levels drop
- The prefrontal cortex is activated

**Important nuance:** the habit of noticing the good requires conscious effort, because the brain is evolutionarily wired toward the negative (negativity bias).

## Three Rules for Effective Gratitude

1. **Specificity.** "Thank you for washing the dishes last night — I didn\'t have to think about it" is better than "You\'re so caring."

2. **Personal meaning.** "This matters to me because..."

3. **Regularity.** Small daily is better than large monthly.''',
                'exercise_instruction': '''## "Three Specific Thank-Yous" Exercise

**Duration:** 5–7 minutes (daily for a week)

### Steps:

Each evening or morning, taking turns:

**1.** Name one specific action of your partner that you are grateful for.
Formula: "I want to thank you for [specific action]. For me, this means [what it means to you personally]."

Example: "I want to thank you for picking up the kids yesterday even though you were tired. It meant I could finish work without stress."

**2. Prohibition:** do not add "but" after the gratitude.

**3. The receiver** responds only: "Thank you for noticing. That means a lot to hear."

### Variation: "Gratitude Letter"

Once a week, write your partner a short letter (5–10 sentences) about what you value in them.''',
                'completion_check': 'Do the exercise for 7 days in a row. At the end of the week, discuss: has anything changed in the atmosphere between you?',
            },
            'uz': {
                'title': "Juftlikda minnatdorlik ko'nikmasi",
                'description': "Muntazam, aniq minnatdorlik amaliyoti munosabatlarni mustahkamlashning eng oddiy va kuchli texnikalaridan biridir.",
                'theory': '''## Nima uchun minnatdorlik ishlaydi

Martin Seligman (ijobiy psixologiya) va Jon Gottmanning tadqiqotlari ko\'rsatadiki: ijobiy va salbiy o\'zaro ta\'sirlarning 5:1 nisbati baxtli munosabatlarni bashorat qiladi.

Bu «Gottmanning Sehrli nisbati» deb ataladi.

## Minnatdorlikning nevrologiyasi

Biz minnatdorlikni ifodalaganmizda yoki qabul qilganimizda:
- Dopamin ajralib chiqadi (mukofot)
- Kortizol darajasi pasayadi
- Prefrontal po\'stloq faollashadi

**Muhim nuance:** yaxshilikni sezish odati ongli harakat talab qiladi, chunki miya evolyutsion jihatdan salbiylikka yo\'naltirilgan (negativity bias).

## Samarali minnatdorlikning uch qoidasi

1. **Aniqlik.** «Kecha kechki ovqatdan keyin idishlarni yuving — buni o\'ylamasligim kerak emas edi» «Siz juda g\'amxo\'rsiz»dan yaxshiroq.

2. **Shaxsiy ma\'no.** «Bu men uchun muhim, chunki...»

3. **Muntazamlik.** Kichik kundalik oylik kattadan yaxshiroq.''',
                'exercise_instruction': '''## «Uchta aniq rahmat» mashqi

**Davomiyligi:** 5-7 daqiqa (bir hafta davomida kundalik)

### Qadamlar:

Har kuni kechqurun yoki ertalab, navbat bilan:

**1.** Sherikingizning bitta aniq harakatini ayting, unga minnatdorsiz.
Formula: «[Aniq harakat] uchun sizga minnatdorlik bildirgim keladi. Bu men uchun [bu siz uchun shaxsan nima degani] anglatadi.»

Misol: «Charchagan bo\'lsangiz ham kecha bolalarni olib kelganingiz uchun minnatdorman. Bu men uchun stresssiz ishni tugatishim mumkin bo\'lgani degani edi.»

**2. Taqiq:** minnatdorlikdan keyin «lekin» qo\'shmang.

**3. Qabul qiluvchi** faqat javob beradi: «Payqaganingiz uchun rahmat. Eshitish yoqimli.»

### Variant: «Minnatdorlik xati»

Haftada bir marta sherikingizga ulardagi qadrlaydigan narsalar haqida qisqa xat (5-10 gap) yozing.''',
                'completion_check': "Mashqni 7 kun ketma-ket bajaring. Hafta oxirida muhokama qiling: o'rtangizda atmosfera o'zgardimi?",
            },
            'uz_cyrl': {
                'title': "Жуфтликда миннатдорлик кўниkmаси",
                'description': "Мунтазам, аниқ миннатдорлик амалиёти муносабатларни мустаҳкамлашнинг энг оддий ва кучли техникаларидан биридир.",
                'theory': '''## Нима учун миннатдорлик ишлайди

Мартин Селигман (ижобий психология) ва Жон Готтманнинг тадқиқотлари кўрсатадики: ижобий ва салбий ўзаро таъсирларнинг 5:1 нисбати бахтли муносабатларни башорат қилади.

Бу «Готтманнинг Сеҳрли нисбати» деб аталади.

## Миннатдорликнинг неврологияси

Биз миннатдорликни ифодалаганимизда ёки қабул қилганимизда:
- Дофамин ажралиб чиқади (мукофот)
- Кортизол даражаси пасаяди
- Префронтал пўстлоқ фаоллашади

**Муҳим нюанс:** яхшиликни сезиш одати онгли ҳаракат талаб қилади, чунки мия эволюцион жиҳатдан салбийликка йўналтирилган (negativity bias).

## Самарали миннатдорликнинг уч қоидаси

1. **Аниқлик.** «Кеча кечки овқатдан кейин идишларни ювдингиз — буни ўйламаслигим керак эди» «Сиз жуда ғамхўрсиз»дан яхшироқ.

2. **Шахсий маъно.** «Бу мен учун муҳим, чунки...»

3. **Мунтазамлик.** Кичик кундалик ойлик каттадан яхшироқ.''',
                'exercise_instruction': '''## «Учта аниқ раҳмат» машқи

**Давомийлиги:** 5-7 дақиқа (бир ҳафта давомида кундалик)

### Қадамлар:

Ҳар куни кечқурун ёки эрталаб, навбат билан:

**1.** Шерикингизнинг битта аниқ ҳаракатини айтинг, унга миннатдорсиз.
Формула: «[Аниқ ҳаракат] учун сизга миннатдорлик билдиргим келади. Бу мен учун [бу сиз учун шахсан нима дегани] англатади.»

Мисол: «Чарчаган бўлсангиз ҳам кеча болаларни олиб келганингиз учун миннатдорман. Бу мен учун стрессиз ишни тугатишим мумкин бўлгани дегани эди.»

**2. Тақиқ:** миннатдорликдан кейин «лекин» қўшманг.

**3. Қабул қилувчи** фақат жавоб беради: «Пайқаганингиз учун раҳмат. Эшитиш ёқимли.»

### Вариант: «Миннатдорлик хати»

Ҳафтада бир марта шерикингизга уларда қадрлайдиган нарсалар ҳақида қисқа хат (5-10 гап) ёзинг.''',
                'completion_check': "Машқни 7 кун кетма-кет бажаринг. Ҳафта охирида муҳокама қилинг: ўртангизда атмосфера ўзгардими?",
            },
        },
        'duration_minutes': 7,
        'difficulty': 'beginner',
        'order_index': 3,
    },
    {
        'slug': 'partner-support-training',
        'skill_type': 'partner_support',
        'title': 'Навык поддержки партнёра',
        'description': 'Научиться давать именно тот вид поддержки, который нужен партнёру в конкретный момент.',
        'theory': '''## Главная ошибка в поддержке

Мы часто даём ту поддержку, которую хотели бы получить сами. Но партнёр может нуждаться в другом.

Исследования показывают: неправильный вид поддержки может быть воспринят как обесценивание или вмешательство.

## Четыре вида поддержки

**1. Эмоциональная** — «быть рядом», выслушать, принять чувства
**2. Информационная** — дать совет, объяснить, найти решение
**3. Практическая** — конкретная помощь (отвезти, приготовить, сделать)
**4. Оценочная** — признать усилия, подтвердить правильность действий

## Правило «Спроси перед тем, как помочь»

Прежде чем поддержать, спросите: «Тебе нужно, чтобы я тебя выслушал, или ты хочешь совет?»

Этот простой вопрос снижает количество конфликтов из-за «ненужных советов» на 70%.

## Формула EAR

- **E** — Empathy (Эмпатия): «Я понимаю, как тебе сейчас тяжело»
- **A** — Acknowledgment (Признание): «Твои чувства совершенно понятны»
- **R** — Respect (Уважение): «Ты справляешься с этим»''',
        'exercise_instruction': '''## Упражнение «Что тебе нужно?»

**Продолжительность:** 20 минут

### Часть 1: Разговор о поддержке (10 мин)

Поговорите о том, как каждый из вас предпочитает получать поддержку:

- Когда у меня что-то идёт не так, мне обычно нужно: [выслушать / совет / объятие / тишина / конкретная помощь]
- Самое бесполезное, что можно сделать в этот момент: ...
- Фраза, которая всегда помогает: ...

### Часть 2: Практика (10 мин)

Один из партнёров рассказывает о чём-то, что его сейчас беспокоит (не обязательно связанном с отношениями).

Слушающий:
1. Задаёт вопрос: «Как ты хочешь, чтобы я сейчас тебя поддержал — просто выслушал или дал совет?»
2. Даёт именно тот вид поддержки, который попросили.
3. В конце спрашивает: «Ты получил то, что было нужно?»

Поменяйтесь ролями.''',
        'completion_check': 'Упражнение выполнено, если вы провели оба разговора и каждый партнёр мог сказать «да» на вопрос «Ты получил то, что было нужно?»',
        'i18n': {
            'en': {
                'title': "Partner Support Skill",
                'description': 'Learn to provide exactly the kind of support your partner needs in a specific moment.',
                'theory': '''## The main mistake in support

We often give the support we would want to receive ourselves. But our partner may need something different.

Research shows: the wrong kind of support can be perceived as dismissal or intrusion.

## Four Types of Support

**1. Emotional** — "being there," listening, accepting feelings
**2. Informational** — giving advice, explaining, finding a solution
**3. Practical** — concrete help (giving a ride, cooking, doing something)
**4. Appraisal** — acknowledging efforts, confirming the person is on the right track

## The "Ask Before You Help" Rule

Before offering support, ask: "Do you need me to listen, or do you want advice?"

This simple question reduces conflicts over "unwanted advice" by 70%.

## The EAR Formula

- **E** — Empathy: "I understand how hard this is for you right now"
- **A** — Acknowledgment: "Your feelings make complete sense"
- **R** — Respect: "You\'re handling this"''',
                'exercise_instruction': '''## "What Do You Need?" Exercise

**Duration:** 20 minutes

### Part 1: Conversation about support (10 min)

Talk about how each of you prefers to receive support:

- When something is going wrong for me, I usually need: [to be listened to / advice / a hug / silence / concrete help]
- The most unhelpful thing to do in that moment: ...
- A phrase that always helps: ...

### Part 2: Practice (10 min)

One partner shares something that is worrying them right now (not necessarily about the relationship).

The listener:
1. Asks: "How would you like me to support you right now — just listen, or give advice?"
2. Gives exactly the kind of support that was requested.
3. At the end asks: "Did you get what you needed?"

Switch roles.''',
                'completion_check': 'The exercise is complete if you had both conversations and each partner could say "yes" to the question "Did you get what you needed?"',
            },
            'uz': {
                'title': "Sherikni qo'llab-quvvatlash ko'nikmasi",
                'description': "Muayyan lahzada sherikingizga aynan kerakli turdagi ko'mak berishni o'rganing.",
                'theory': '''## Ko\'makning asosiy xatosi

Biz ko\'pincha o\'zimiz olishni xohlagan ko\'makni beramiz. Ammo sherikingizga boshqa narsa kerak bo\'lishi mumkin.

Tadqiqotlar ko\'rsatadiki: noto\'g\'ri turdagi ko\'mak kamsitish yoki aralashuv sifatida qabul qilinishi mumkin.

## Ko\'makning to\'rt turi

**1. Hissiy** — «yonida bo\'lish», tinglash, his-tuyg\'ularni qabul qilish
**2. Axborot** — maslahat berish, tushuntirish, yechim topish
**3. Amaliy** — aniq yordam (olib borish, pishirish, qilish)
**4. Baholash** — sa\'y-harakatlarni tan olish, harakatlarning to\'g\'riligini tasdiqlash

## «Yordam berishdan oldin so\'rang» qoidasi

Ko\'mak ko\'rsatishdan oldin so\'rang: «Sizga eshitishimni istaysizmi yoki maslahat kerakmi?»

Bu oddiy savol «keraksiz maslahatlar» tufayli yuzaga keladigan nizolarni 70% ga kamaytiradi.

## EAR formulasi

- **E** — Empatiya: «Hozir sizga qanchalik qiyin ekanini tushunaman»
- **A** — Tan olish: «Sizning his-tuyg\'ularingiz mutlaqo tushuniladi»
- **R** — Hurmat: «Siz bu bilan muvaffaqiyatli kurashyapsiz»''',
                'exercise_instruction': '''## «Sizga nima kerak?» mashqi

**Davomiyligi:** 20 daqiqa

### 1-qism: Ko\'mak haqida suhbat (10 daqiqa)

Har biringliz ko\'makni qanday qabul qilishni afzal ko\'rishingiz haqida gaplashing:

- Menda biror narsa yomonlashsa, odatda menga kerak: [tinglash / maslahat / quchoq / jimlik / aniq yordam]
- O\'sha lahzada qilish mumkin bo\'lgan eng foydasisz narsa: ...
- Har doim yordam beradigan ibora: ...

### 2-qism: Amaliyot (10 daqiqa)

Sherikdan biri hozir bezovta qilayotgan narsa haqida gapiradi (munosabatlar bilan bog\'liq bo\'lishi shart emas).

Tinglovchi:
1. So\'raydi: «Meni qanday qo\'llab-quvvatlashimni xohlaysiz — shunchaki tinglasammi yoki maslahat bersam?»
2. So\'ralgan turdagi ko\'makni beradi.
3. Oxirida so\'raydi: «Kerakli narsani oldingizmi?»

Rollarni almashing.''',
                'completion_check': "Mashq bajarildi, agar siz ikkala suhbatni ham o'tkazgan bo'lsangiz va har bir sherik «Kerakli narsani oldingizmi?» savoliga «Ha» deb javob bera olsa.",
            },
            'uz_cyrl': {
                'title': "Шерикни қўллаб-қувватлаш кўниkmаси",
                'description': "Муайян лаҳзада шерикингизга айнан керакли тurdagi кўмак беришни ўрганинг.",
                'theory': '''## Кўмакнинг асосий хатоси

Биз кўпинча ўзимиз олишни хоҳлаган кўмакни берамиз. Аммо шерикингизга бошқа нарса керак бўлиши мумкин.

Тадқиқотлар кўрсатадики: нотўғри тurdagi кўмак камситиш ёки аралашув сифатида қабул қилиниши мумкин.

## Кўмакнинг тўрт тури

**1. Ҳиссий** — «ёнида бўлиш», тинглаш, ҳис-туйғуларни қабул қилиш
**2. Ахборот** — маслаҳат бериш, тушунтириш, ечим топиш
**3. Амалий** — аниқ ёрдам (олиб бориш, пишириш, қилиш)
**4. Баҳолаш** — саъй-ҳаракатларни тан олиш, ҳаракатларнинг тўғрилигини тасдиқлаш

## «Ёрдам беришдан олдин сўранг» қоидаси

Кўмак кўрсатишдан олдин сўранг: «Сизга эшитишимни истайсизми ёки маслаҳат керакми?»

Бу оддий савол «керaксиз маслаҳатлар» туфайли юзага келадиган низоларни 70% га камайтиради.

## EAR формуласи

- **E** — Эмпатия: «Ҳозир сизга қанчалик қийин эканини тушунаман»
- **A** — Тан олиш: «Сизнинг ҳис-туйғуларingиз мутлақо тушунилади»
- **R** — Ҳурмат: «Сиз бу билан муваффақиятли курашяпсиз»''',
                'exercise_instruction': '''## «Сизга нима керак?» машқи

**Давомийлиги:** 20 дақиқа

### 1-қисм: Кўмак ҳақида суҳбат (10 дақиқа)

Ҳар биринглиз кўмакни қандай қабул қилишни афзал кўришингиз ҳақида гаплашинг:

- Менда бирор нарса ёмонлашса, одатда менга керак: [тинглаш / маслаҳат / қучоқ / жимлик / аниқ ёрдам]
- Ўша лаҳзада қилиш мумкин бўлган энг фойдасиз нарса: ...
- Ҳар доим ёрдам берадиган ибора: ...

### 2-қисм: Амалиёт (10 дақиқа)

Шерикдан бири ҳозир безовта қилаётган нарса ҳақида гапиради (муносабатлар билан боғлиқ бўлиши шарт эмас).

Тингловчи:
1. Сўрайди: «Мени қандай қўллаб-қувватлашимни xоҳлайсиз — шунчаки тинглаямми ёки маслаҳат берсам?»
2. Сўралган тurdagi кўмакни беради.
3. Охирида сўрайди: «Керакли нарсани олдингизми?»

Ролларни алмашинг.''',
                'completion_check': "Машқ бажарилди, агар сиз иккала суҳбатни ҳам ўтказган бўлсангиз ва ҳар бир шерик «Керакли нарсани олдингизми?» саволига «Ҳа» деб жавоб бера олса.",
            },
        },
        'duration_minutes': 20,
        'difficulty': 'beginner',
        'order_index': 4,
    },
    {
        'slug': 'constructive-dialogue-training',
        'skill_type': 'constructive_dialogue',
        'title': 'Конструктивный диалог о сложных темах',
        'description': 'Освоить структуру «мягкого старта» — как начать трудный разговор без обвинений и защитных реакций.',
        'theory': '''## Почему важен старт разговора

Готтман установил: в 96% случаев конец разговора можно предсказать по первым трём минутам. Жёсткий старт (обвинение, критика, сарказм) практически гарантирует неудачу.

## Мягкий старт (Soft Startup)

Ключевые элементы мягкого старта:

**1. Начните с «Я», а не с «Ты».**
- Жёсткий: «Ты никогда меня не слушаешь»
- Мягкий: «Я чувствую себя невидимым в наших разговорах»

**2. Описывайте факт, а не личность.**
- Жёсткий: «Ты безответственный»
- Мягкий: «Когда счета приходят неоплаченными...»

**3. Назовите свои чувства без оценки партнёра.**
Используйте слова: одиноко, тревожно, грустно, обидно, устало.

**4. Сформулируйте позитивную просьбу.**
Не «прекрати делать X», а «мне нужно Y».

## Правило «Одна проблема — один разговор»

Не добавляйте к текущей теме воспоминания о прошлых обидах. «Ты всегда так делаешь» убивает диалог.''',
        'exercise_instruction': '''## Упражнение «Переформулируй»

**Продолжительность:** 15-20 минут

### Часть 1: Индивидуально (7 мин)

Каждый пишет 3 претензии к партнёру в формате обвинения, а затем переформулирует их в «мягкий старт».

Шаблон: «Когда [факт без оценки], я чувствую [эмоция], потому что [объяснение]. Мне хотелось бы [конкретная просьба].»

Пример:
- Обвинение: «Ты постоянно сидишь в телефоне вместо того, чтобы поговорить со мной»
- Мягкий старт: «Когда вечером мы в одной комнате, но не разговариваем, я чувствую одиночество. Мне хотелось бы 20 минут без телефонов.»

### Часть 2: Вместе (10 мин)

Поочерёдно прочитайте вслух одно из своих «мягких стартов» (не самое острое).
Слушающий только слушает и подтверждает: «Я услышал тебя.»
Затем обсудите: изменилось ли что-то при таком формулировании?''',
        'completion_check': 'Упражнение выполнено, если каждый переформулировал хотя бы 2 из 3 претензий и партнёр смог выслушать их без защитной реакции.',
        'i18n': {
            'en': {
                'title': 'Constructive Dialogue on Difficult Topics',
                'description': 'Master the "soft startup" structure — how to begin a difficult conversation without accusations and defensive reactions.',
                'theory': '''## Why the start of a conversation matters

Gottman established: in 96% of cases, the outcome of a conversation can be predicted from the first three minutes. A harsh start (blame, criticism, sarcasm) virtually guarantees failure.

## Soft Startup

Key elements of a soft startup:

**1. Start with "I," not "You."**
- Harsh: "You never listen to me"
- Soft: "I feel invisible in our conversations"

**2. Describe the fact, not the person.**
- Harsh: "You\'re irresponsible"
- Soft: "When bills arrive unpaid..."

**3. Name your feelings without judging your partner.**
Use words: lonely, anxious, sad, hurt, exhausted.

**4. Formulate a positive request.**
Not "stop doing X," but "I need Y."

## The "One Issue, One Conversation" Rule

Don\'t add memories of past grievances to the current topic. "You always do this" kills dialogue.''',
                'exercise_instruction': '''## "Rephrase It" Exercise

**Duration:** 15–20 minutes

### Part 1: Individually (7 min)

Each person writes 3 complaints about their partner in accusatory form, then rephrases them as a "soft startup."

Template: "When [fact without evaluation], I feel [emotion], because [explanation]. I would like [specific request]."

Example:
- Accusation: "You\'re always on your phone instead of talking to me"
- Soft startup: "When we\'re in the same room in the evening but not talking, I feel lonely. I would like 20 minutes without phones."

### Part 2: Together (10 min)

Take turns reading one of your "soft startups" aloud (not the sharpest one).
The listener only listens and confirms: "I heard you."
Then discuss: did anything change when you phrased it this way?''',
                'completion_check': 'The exercise is complete if each person rephrased at least 2 out of 3 complaints and the partner was able to listen without a defensive reaction.',
            },
            'uz': {
                'title': "Qiyin mavzularda konstruktiv muloqot",
                'description': "«Yumshoq boshlash» tuzilmasini o'zlashtiring — ayblovlar va himoyalanish reaksiyalarisiz qiyin suhbatni qanday boshlash.",
                'theory': '''## Suhbat boshlanishi nima uchun muhim

Gottman aniqladi: 96% hollarda suhbatning oxiri dastlabki uch daqiqadan bashorat qilinishi mumkin. Qattiq boshlash (ayblash, tanqid, kinoya) muvaffaqiyatsizlikni deyarli kafolatlaydi.

## Yumshoq boshlash (Soft Startup)

Yumshoq boshlashning asosiy elementlari:

**1. «Men» bilan boshlang, «Siz» bilan emas.**
- Qattiq: «Siz meni hech qachon eshitmaysiz»
- Yumshoq: «Suhbatlarimizda o\'zimni ko\'rinmas his qilaman»

**2. Faktni tasvirlang, shaxsni emas.**
- Qattiq: «Siz mas\'uliyatsiz»
- Yumshoq: «Hisoblar to\'lanmasdan kelganda...»

**3. Sherikni baholamasdan his-tuyg\'ularingizni nomlang.**
So\'zlardan foydalaning: yolg\'iz, xavotirli, g\'amgin, ranjigan, charchagan.

**4. Ijobiy so\'rovni shakllantiring.**
«X qilishni to\'xtating» emas, balki «Menga Y kerak».

## «Bitta muammo — bitta suhbat» qoidasi

Joriy mavzuga o\'tgan shikoyatlar xotiralarini qo\'shmang. «Siz har doim shunday qilasiz» muloqotni o\'ldiradi.''',
                'exercise_instruction': '''## «Qayta shakllantiring» mashqi

**Davomiyligi:** 15-20 daqiqa

### 1-qism: Alohida (7 daqiqa)

Har biri sherikka nisbatan 3 ta shikoyatni ayblov shaklida yozadi, so\'ngra ularni «yumshoq boshlash» shaklida qayta shakllantiradi.

Shablon: «[Baholashsiz fakt] bo\'lganda, men [hissiyot] his qilaman, chunki [tushuntirish]. [Aniq so\'rov] ni xohlardim.»

Misol:
- Ayblov: «Siz men bilan gaplashish o\'rniga doim telefonda o\'tirasiz»
- Yumshoq boshlash: «Kechqurun bir xonada bo\'lganimizda lekin gaplashmaganimizda, o\'zimni yolg\'iz his qilaman. Telefonlarsiz 20 daqiqa xohlayman.»

### 2-qism: Birgalikda (10 daqiqa)

Navbat bilan «yumshoq boshlash»lardan birini ovoz chiqarib o\'qing (eng o\'tkirini emas).
Tinglovchi faqat tinglaydi va tasdiqlaydi: «Sizni eshitdim.»
So\'ngra muhokama qiling: bunday shakllantirganda biror narsa o\'zgardimi?''',
                'completion_check': "Mashq bajarildi, agar har biri 3 ta shikoyatdan kamida 2 tasini qayta shakllantirgan bo'lsa va sherik himoyalanish reaksiyasisiz ularni eshita olgan bo'lsa.",
            },
            'uz_cyrl': {
                'title': "Қийин мавзуларда конструктив мулоқот",
                'description': "«Юмшоқ бошлаш» тузилmasini ўзлаштиринг — айбловлар ва ҳимояланиш реакцияларисиз қийин суҳбатни қандай бошлаш.",
                'theory': '''## Суҳбат бошланиши нима учун муҳим

Готтман аниқлади: 96% ҳолларда суҳбатнинг охири дастлабки уч дақиқадан башорат қилиниши мумкин. Қаттиқ бошлаш (айблаш, танқид, кинoya) муваффақиятсизликни деярли кафолатлайди.

## Юмшоқ бошлаш (Soft Startup)

Юмшоқ бошлашнинг асосий элементлари:

**1. «Мен» билан бошланг, «Сиз» билан эмас.**
- Қаттиқ: «Сиз мени ҳеч қачон эшитмайсиз»
- Юмшоқ: «Суҳбатларимизда ўзимни кўринмас ҳис қиламан»

**2. Фактни тасвирланг, шахсни эмас.**
- Қаттиқ: «Сиз масъулиятсизсиз»
- Юмшоқ: «Ҳисоблар тўланмасдан келганда...»

**3. Шерикни баҳоламасдан ҳис-туйғуларingизni номланг.**
Сўзлардан фойдаланинг: ёлғиз, хавотирли, ғамгин, ранжиган, чарчаган.

**4. Ижобий сўровни шакллантиринг.**
«X қилишни тўхтатинг» эмас, балки «Менга Y керак».

## «Битта муаммо — битта суҳбат» қоидаси

Жорий мавзуга ўтган шикоятлар хотираларини қўшманг. «Сиз ҳар доим шундай қиласиз» мулоқотни ўлдиради.''',
                'exercise_instruction': '''## «Қайта шакллантиринг» машқи

**Давомийлиги:** 15-20 дақиқа

### 1-қисм: Алоҳида (7 дақиқа)

Ҳар бири шерикка нисбатан 3 та шикоятни айблов шаклида ёзади, сўнгра уларни «юмшоқ бошлаш» шаклида қайта шакллантиради.

Шаблон: «[Баҳолашсиз факт] бўлганда, мен [ҳиссиёт] ҳис қиламан, чунки [тушунтириш]. [Аниқ сўров] ни хоҳлардим.»

Мисол:
- Айблов: «Сиз мен билан гаплашиш ўрнига доим телефонда ўтирасиз»
- Юмшоқ бошлаш: «Кечқурун бир хонада бўлганимизда лекин гаплашмаганимизда, ўзимни ёлғиз ҳис қиламан. Телефонларсиз 20 дақиқа хоҳлайман.»

### 2-қисм: Биргаликда (10 дақиқа)

Навбат билан «юмшоқ бошлаш»лардан бирини овоз чиқариб ўқинг (энг ўтkirини эмас).
Тингловчи фақат тинглайди ва тасдиқлайди: «Сизни эшитдим.»
Сўнгра муҳокама қилинг: бундай шаклlantirganda бирор нарса ўзгардими?''',
                'completion_check': "Машқ бажарилди, агар ҳар бири 3 та шикоятдан камида 2 тасини қайта шакллантирган бўлса ва шерик ҳимояланиш реакцияsиз уларни эшита олган бўлса.",
            },
        },
        'duration_minutes': 20,
        'difficulty': 'intermediate',
        'order_index': 5,
    },
    {
        'slug': 'conflict-resolution-training',
        'skill_type': 'conflict_resolution',
        'title': 'Навык решения конфликтов без жертв',
        'description': 'Освоить технику «Победа-победа»: находить решения, которые учитывают интересы обоих партнёров.',
        'theory': '''## Почему «победить» в конфликте — это проигрыш

В отношениях не существует победителей. Если один партнёр «выиграл» спор, другой чувствует обиду и желание «отыграться» позже.

Цель — не победить, а найти решение, которое оба могут принять с уважением.

## Модель «Победа-Победа»

Основана на гарвардском методе переговоров (Фишер, Ури, Патон).

**Шаг 1: Разделите позиции и интересы.**
- Позиция: «Хочу ехать в отпуск в горы»
- Интерес (что за ней стоит): «Хочу активный отдых, хочу восстановиться от работы»

Когда вы понимаете интересы партнёра, нередко находится решение, удовлетворяющее обоих.

**Шаг 2: Генерация вариантов без оценки.**
Записывайте все идеи, даже абсурдные. Оценивать будете потом.

**Шаг 3: Выбор по критериям, которые оба признали справедливыми.**

## Что делать с вечными конфликтами

Если тема повторяется — это «вечный конфликт». Цель здесь не решение, а диалог о ценностях и мечтах, стоящих за позициями.

Задайте вопрос: «Что для тебя самое важное в этом?»''',
        'exercise_instruction': '''## Упражнение «Интересы за позицией»

**Продолжительность:** 25 минут

### Выберите реальный конфликт

Возьмите тему, которая повторяется у вас. Не самую острую — средней интенсивности.

### Шаг 1: Карточки позиций (5 мин)

Каждый пишет на карточке: «Моя позиция по этой теме: [что именно хочу]»

### Шаг 2: Копание вглубь (10 мин)

По очереди задавайте друг другу вопросы (задающий только слушает, не спорит):
- «Почему для тебя это важно?»
- «Что произойдёт, если этого не будет?»
- «Какая твоя мечта или страх связаны с этим?»

Записывайте интересы.

### Шаг 3: Поиск общего (10 мин)

Найдите хотя бы один интерес, который у вас общий.
На основе него придумайте 3 возможных решения, которые учитывают интересы обоих.
Обсудите: какое из них вы оба можете попробовать на 1 месяц?''',
        'completion_check': 'Упражнение выполнено, если вы нашли хотя бы один общий интерес и договорились попробовать одно из решений.',
        'i18n': {
            'en': {
                'title': 'Conflict Resolution Without Losers',
                'description': 'Master the "win-win" technique: finding solutions that take both partners\' interests into account.',
                'theory': '''## Why "winning" a conflict is a loss

In relationships, there are no winners. If one partner "won" the argument, the other feels resentment and a desire to "get back" later.

The goal is not to win, but to find a solution that both can accept with respect.

## The "Win-Win" Model

Based on the Harvard negotiation method (Fisher, Ury, Patton).

**Step 1: Separate positions from interests.**
- Position: "I want to go on vacation to the mountains"
- Interest (what\'s behind it): "I want an active rest, I want to recover from work"

When you understand your partner\'s interests, a solution that satisfies both is often found.

**Step 2: Generate options without evaluating.**
Write down all ideas, even absurd ones. You\'ll evaluate later.

**Step 3: Choose based on criteria that both consider fair.**

## What to do with perpetual conflicts

If the topic recurs — it\'s a "perpetual conflict." The goal here is not a solution, but dialogue about the values and dreams behind each position.

Ask: "What matters most to you about this?"''',
                'exercise_instruction': '''## "Interests Behind the Position" Exercise

**Duration:** 25 minutes

### Choose a real conflict

Take a topic that recurs for you. Not the sharpest one — medium intensity.

### Step 1: Position cards (5 min)

Each person writes on a card: "My position on this topic: [what I want specifically]"

### Step 2: Digging deeper (10 min)

Take turns asking each other questions (the questioner only listens, does not argue):
- "Why is this important to you?"
- "What will happen if this doesn\'t happen?"
- "What dream or fear of yours is connected to this?"

Write down the interests.

### Step 3: Finding common ground (10 min)

Find at least one interest you share in common.
Based on it, come up with 3 possible solutions that take both interests into account.
Discuss: which one can you both try for 1 month?''',
                'completion_check': 'The exercise is complete if you found at least one shared interest and agreed to try one of the solutions.',
            },
            'uz': {
                'title': "Qurbonlarsiz nizolarni hal qilish ko'nikmasi",
                'description': "«G'alaba-g'alaba» texnikasini o'zlashtiring: ikkala sherikningam manfaatlarini hisobga oladigan yechimlar topish.",
                'theory': '''## Nizoda «g\'alaba qozonish» nima uchun mag\'lubiyatdir

Munosabatlarda g\'oliblar yo\'q. Agar sherikdan biri bahsda «g\'alaba qozonsa», ikkinchisi adovat va keyinroq «qasos olish» istagini his qiladi.

Maqsad — g\'alaba qozonish emas, ikkalasi ham hurmat bilan qabul qila oladigan yechim topish.

## «G\'alaba-G\'alaba» modeli

Garvard muzokaralar usuliga asoslangan (Fisher, Uri, Paton).

**1-qadam: Pozitsiyalar va manfaatlarni ajrating.**
- Pozitsiya: «Tog\'larga ta\'tilga bormoqchiman»
- Manfaat (ortidagi narsa): «Faol dam olishni xohlayman, ishdan tiklanmoqchiman»

Sherikingizning manfaatlarini tushunganingizda, ko\'pincha ikkalasini ham qoniqtiradigan yechim topiladi.

**2-qadam: Baholamasdan variantlar generatsiyasi.**
Barcha g\'oyalarni, hatto absurd bo\'lganlarini ham yozing. Baholash keyinroq.

**3-qadam: Ikkalasi ham adolatli deb tan olgan mezonlar bo\'yicha tanlash.**

## Abadiy nizolar bilan nima qilish kerak

Agar mavzu takrorlanayotgan bo\'lsa — bu «abadiy nizo». Bu yerda maqsad yechim emas, har bir pozitsiya ortidagi qadriyatlar va orzular haqida muloqotdir.

So\'rang: «Bunda siz uchun eng muhimi nima?»''',
                'exercise_instruction': '''## «Pozitsiya ortidagi manfaatlar» mashqi

**Davomiyligi:** 25 daqiqa

### Haqiqiy nizoni tanlang

Sizda takrorlanadigan mavzuni oling. Eng o\'tkirini emas — o\'rtacha intensivlikdagini.

### 1-qadam: Pozitsiya kartalari (5 daqiqa)

Har biri kartaga yozadi: «Bu mavzu bo\'yicha mening pozitsiyam: [aynan nima xohlayman]»

### 2-qadam: Chuqurroq qazish (10 daqiqa)

Navbat bilan bir-biringizga savollar bering (so\'rovchi faqat tinglaydi, bahslaşmaydi):
- «Bu siz uchun nima uchun muhim?»
- «Bu bo\'lmasa nima bo\'ladi?»
- «Qanday orzu yoki qo\'rquvingiz bilan bog\'liq?»

Manfaatlarni yozing.

### 3-qadam: Umumiy topish (10 daqiqa)

Kamida bitta umumiy manfaatingizni toping.
Unga asoslanib ikkisiningam manfaatlarini hisobga oladigan 3 ta mumkin bo\'lgan yechim o\'ylab toping.
Muhokama qiling: qaysi birini ikkalangiz ham 1 oy sinab ko\'rishingiz mumkin?''',
                'completion_check': "Mashq bajarildi, agar siz kamida bitta umumiy manfaat topgan bo'lsangiz va yechimlardan birini sinab ko'rishga kelishgan bo'lsangiz.",
            },
            'uz_cyrl': {
                'title': "Қурбонларсиз низоларни ҳал қилиш кўниkmаси",
                'description': "«Ғалаба-ғалаба» техникасini ўзлаштиринг: иккала шерикningam манфаатларини ҳисобга оладиган ечимлар топиш.",
                'theory': '''## Низода «ғалаба қозониш» нима учун мағлубиятдир

Муносабатларда ғолиблар йўқ. Агар шерикдан бири баҳсда «ғалаба қозонса», иккинчиси адоват ва кейинроқ «қасос олиш» исtagini ҳис қилади.

Мақсад — ғалаба қозониш эмас, иккаласи ҳам ҳурмат билан қабул қила оладиган ечим топиш.

## «Ғалаба-Ғалаба» модели

Гарвард музокаралар усулига асосланган (Фишер, Ури, Патон).

**1-қадам: Позициялар ва манфаатларни ажратинг.**
- Позиция: «Тоғларга та\'тилга бормоқчиман»
- Манфаат (ортидаги нарса): «Фаол дам олишни хоҳлайман, ишдан тикланмоқчиман»

Шерикingizнинг манфаатларини тушунганингизда, кўпинча иккаласини ҳам қониқтирадиган ечим топилади.

**2-қадам: Баҳоламасдан вариантлар генерацияси.**
Барча ғояларни, ҳатто абсурд бўлганларини ҳам ёзинг. Баҳолаш кейинроқ.

**3-қадам: Иккаласи ҳам адолатли деб тан олган мезонлар бўйича танлаш.**

## Абадий низолар билан нима қилиш керак

Агар мавзу такрорланаётган бўлса — бу «абадий низо». Бу ерда мақсад ечим эмас, ҳар бир позиция ортидаги қадриятлар ва орзулар ҳақида мулоқотдир.

Сўранг: «Бунда сиз учун энг муҳими нима?»''',
                'exercise_instruction': '''## «Позиция ортидаги манфаатлар» машқи

**Давомийлиги:** 25 дақиқа

### Ҳақиқий низони танланг

Сизда такрорланадиган мавзуни олинг. Энг ўтkirини эмас — ўртача интенсивликдагини.

### 1-қадам: Позиция карталари (5 дақиқа)

Ҳар бири картага ёзади: «Бу мавзу бўйича менинг позициям: [айнан нима хоҳлайман]»

### 2-қадам: Чуқурроқ қазиш (10 дақиқа)

Навбат билан бир-бирингизга саволлар беринг (сўровчи фақат тинглайди, баҳслашмайди):
- «Бу сиз учун нима учун муҳим?»
- «Бу бўлмаса нима бўлади?»
- «Қандай орзу ёки қўрқувingиз билан боғлиқ?»

Манфаатларни ёзинг.

### 3-қадам: Умумий топиш (10 дақиқа)

Камида биттa умумий манфаатингизni топинг.
Унга асосланиб иккисiningam манфаатларини ҳисобга оладиган 3 та мумкин бўлган ечим ўйлаб топинг.
Муҳокама қилинг: қайси бирини иккалангиз ҳам 1 ой синаб кўришингиз мумкин?''',
                'completion_check': "Машқ бажарилди, агар сиз камида биттa умумий манфаат топган бўлсангиз ва ечимлардан бирини синаб кўришга келишган бўлсангиз.",
            },
        },
        'duration_minutes': 25,
        'difficulty': 'intermediate',
        'order_index': 6,
    },
    {
        'slug': 'joint-planning-training',
        'skill_type': 'joint_planning',
        'title': 'Навык совместного планирования',
        'description': 'Научиться строить общее видение будущего и принимать совместные решения, сохраняя уважение к разным стилям планирования.',
        'theory': '''## Почему совместное планирование важно

Пары с общими целями и регулярным обсуждением будущего имеют более высокий уровень удовлетворённости отношениями. Это подтверждается исследованиями Journal of Marriage and Family.

## Разные стили планирования

Некоторые люди — «планировщики», другие — «импровизаторы». Конфликт стилей часто воспринимается как конфликт ценностей, хотя это просто разные стратегии.

**Планировщик** чувствует тревогу при отсутствии определённости.
**Импровизатор** чувствует ограничение при жёстких планах.

Задача — найти систему, которая даёт достаточно структуры для одного и достаточно гибкости для другого.

## Три уровня планирования

**Ежедневный** — кто что делает, кто забирает детей, кто готовит.
**Еженедельный** — «Как пройдёт наша неделя? Что важного предстоит?»
**Стратегический** — «Где мы через 5 лет? Что для нас важно?»

## Инструмент: «Семейный совет»

Раз в неделю — 20 минут на обсуждение текущих дел и ближайших планов. С чёткой структурой: позитивное начало → практические вопросы → планы → что мы хотим сделать вместе.''',
        'exercise_instruction': '''## Упражнение «Первый семейный совет»

**Продолжительность:** 30 минут

### Повестка (следуйте строго по пунктам):

**1. Открытие (3 мин):** каждый называет одну вещь, за которую благодарен партнёру на этой неделе.

**2. Обзор недели (5 мин):** что важного произошло? Что получилось хорошо?

**3. Практические вопросы (10 мин):** что нужно организовать на следующей неделе? (встречи, дела, поручения). Разделите задачи.

**4. Планы (7 мин):** что хотите сделать вместе на следующей неделе? Назначьте конкретное время.

**5. Закрытие (5 мин):** каждый говорит одно слово или фразу о том, как чувствует себя сейчас.

### Правила:
- Без телефонов
- Не обсуждайте конфликты на совете (для этого есть другие разговоры)
- Проводите в одно и то же время каждую неделю''',
        'completion_check': 'Упражнение выполнено, если вы провели первый семейный совет по всем пяти пунктам и оба почувствовали, что это было полезно.',
        'i18n': {
            'en': {
                'title': 'Joint Planning Skill',
                'description': 'Learn to build a shared vision of the future and make decisions together while respecting different planning styles.',
                'theory': '''## Why joint planning matters

Couples with shared goals and regular discussions about the future have higher relationship satisfaction. This is confirmed by Journal of Marriage and Family research.

## Different planning styles

Some people are "planners," others are "improvisers." Conflict between styles is often perceived as a conflict of values, when it is really just different strategies.

**The planner** feels anxious in the absence of certainty.
**The improviser** feels constrained by rigid plans.

The task is to find a system that gives enough structure for one partner and enough flexibility for the other.

## Three Levels of Planning

**Daily** — who does what, who picks up the kids, who cooks.
**Weekly** — "How will our week go? What\'s coming up?"
**Strategic** — "Where will we be in 5 years? What\'s important to us?"

## Tool: "Family Council"

Once a week — 20 minutes to discuss current affairs and upcoming plans. With a clear structure: positive opening → practical matters → plans → what we want to do together.''',
                'exercise_instruction': '''## "First Family Council" Exercise

**Duration:** 30 minutes

### Agenda (follow strictly in order):

**1. Opening (3 min):** each person names one thing they are grateful to their partner for this week.

**2. Week in review (5 min):** what important things happened? What went well?

**3. Practical matters (10 min):** what needs to be organized for next week? (appointments, tasks, errands). Divide up the tasks.

**4. Plans (7 min):** what would you like to do together next week? Set a specific time.

**5. Closing (5 min):** each person says one word or phrase about how they feel right now.

### Rules:
- No phones
- Don\'t discuss conflicts at the council (there are other conversations for that)
- Hold it at the same time every week''',
                'completion_check': 'The exercise is complete if you held the first family council covering all five points and both felt it was useful.',
            },
            'uz': {
                'title': "Birgalikda rejalashtirish ko'nikmasi",
                'description': "Kelajak haqida umumiy tasavvur qurishni va turli rejalashtirish uslublarini hurmat qilgan holda birgalikda qarorlar qabul qilishni o'rganing.",
                'theory': '''## Nima uchun birgalikda rejalashtirish muhim

Umumiy maqsadlarga ega va kelajak haqida muntazam muhokama qiladigan juftliklar munosabatlar qoniqarligining yuqori darajasiga ega. Buni Journal of Marriage and Family tadqiqotlari tasdiqlaydi.

## Turli rejalashtirish uslublari

Ba\'zi odamlar «rejalashtiruvchi», boshqalari «improvisatorlar». Uslublar o\'rtasidagi ziddiyat ko\'pincha qadriyatlar ziddiyati sifatida qabul qilinadi, holbuki bu shunchaki turli strategiyalar.

**Rejalashtiruvchi** aniqlik yo\'qligida xavotir his qiladi.
**Improvisator** qat\'iy rejalarda cheklanganlik his qiladi.

Vazifa — bir sherik uchun yetarli tuzilma va boshqasi uchun yetarli moslashuvchanlik beruvchi tizim topish.

## Rejalashtirishning uch darajasi

**Kundalik** — kim nima qiladi, bolalarni kim oladi, kim pishiradi.
**Haftalik** — «Haftamiz qanday o\'tadi? Nima kutilmoqda?»
**Strategik** — «5 yildan keyin biz qayerdamiz? Biz uchun nima muhim?»

## Vosita: «Oila kengashi»

Haftada bir marta — joriy ishlar va yaqinlashib kelayotgan rejalarni muhokama qilish uchun 20 daqiqa. Aniq tuzilma bilan: ijobiy ochilish → amaliy masalalar → rejalar → birgalikda nima qilishni xohlaymiz.''',
                'exercise_instruction': '''## «Birinchi oila kengashi» mashqi

**Davomiyligi:** 30 daqiqa

### Kun tartibi (qat\'iy tartibda kuzating):

**1. Ochilish (3 daqiqa):** har biri bu haftada sherikiga minnatdor bo\'lgan bitta narsani nomlaydi.

**2. Haftani ko\'rib chiqish (5 daqiqa):** nima muhim narsa bo\'ldi? Nima yaxshi bo\'ldi?

**3. Amaliy masalalar (10 daqiqa):** keyingi haftaga nima tashkil qilish kerak? (uchrashuvlar, vazifalar, topshiriqlar). Vazifalarni taqsimlang.

**4. Rejalar (7 daqiqa):** keyingi haftada birgalikda nima qilishni xohlaysizlar? Aniq vaqtni belgilang.

**5. Yopilish (5 daqiqa):** har biri hozir qanday his qilayotganini bitta so\'z yoki ibora bilan aytadi.

### Qoidalar:
- Telefonsiz
- Kengashda nizolarni muhokama qilmang (buning uchun boshqa suhbatlar bor)
- Har haftada bir xil vaqtda o\'tkazing''',
                'completion_check': "Mashq bajarildi, agar siz birinchi oila kengashini barcha besh band bo'yicha o'tkazgan bo'lsangiz va ikkalangiz ham bu foydali ekanini his qilgan bo'lsangiz.",
            },
            'uz_cyrl': {
                'title': "Биргаликда режалаштириш кўниkmаси",
                'description': "Келажак ҳақида умумий тасаввур қуришни ва турли режалаштириш услубларини ҳурмат қилган ҳолда биргаликда қарорлар қабул қилишни ўрганинг.",
                'theory': '''## Нима учун биргаликда режалаштириш муҳим

Умумий мақсадларга эга ва келажак ҳақида мунтазам муҳокама қиладиган жуфтликлар муносабатлар қониqarlигining юқори даражасига эга. Буни Journal of Marriage and Family тадқиқотлари тасдиқлайди.

## Турли режалаштириш услублари

Баъзи одамлар «режалаштирувчи», бошқалари «импровизаторлар». Услублар ўртасидаги зиддият кўпинча қадриятлар зиддияти сифатида қабул қилинади, ҳолбуки бу шунчаки турли стратегиялар.

**Режалаштирувчи** аниқлик йўқлигида хавотир ҳис қилади.
**Импровизатор** қатъий режаларда чекланганлик ҳис қилади.

Вазифа — бир шерик учун етарли тузилма ва бошқаси учун етарли мослашувчанлик берувчи тизим топиш.

## Режалашtirishнинг уч даражаси

**Кундалик** — ким нима қилади, болаларни ким олади, ким пиширади.
**Ҳафталик** — «Ҳафтамиз қандай ўтади? Нима кутилмоқда?»
**Стратегик** — «5 йилдан кейин биз қаердамиз? Биз учун нима муҳим?»

## Восита: «Оила кенгаши»

Ҳафтада бир марта — жорий ишлар ва яқинлашиб келаётган режаларни муҳокама қилиш учун 20 дақиқа. Аниқ тузилма билан: ижобий очилиш → амалий масалалар → режалар → биргаликда нима қилишni хоҳлаймиз.''',
                'exercise_instruction': '''## «Биринчи оила кенгаши» машқи

**Давомийлиги:** 30 дақиқа

### Кун тартиби (қатъий тартибда кузатинг):

**1. Очилиш (3 дақиқа):** ҳар бири бу ҳафтада шерикига миннатдор бўлган битта нарсани номлайди.

**2. Ҳафтани кўриб чиқиш (5 дақиқа):** нима муҳим нарса бўлди? Нима яхши бўлди?

**3. Амалий масалалар (10 дақиқа):** кейинги ҳафтага нима ташкил қилиш керак? (учрашувлар, вазифалар, топшириқлар). Вазифаларни тақсимланг.

**4. Режалар (7 дақиқа):** кейинги ҳафтада биргаликда нима қилишни xоҳлайсизлар? Аниқ вақтни белгиланг.

**5. Ёпилиш (5 дақиқа):** ҳар бири ҳозир қандай ҳис қилаётганини битта сўз ёки ибора билан айтади.

### Қоидалар:
- Телефонсиз
- Кенгашда низоларни муҳокама қилманг (бунинг учун бошқа суҳбатлар бор)
- Ҳар ҳафтада бир хил вақтда ўтказинг''',
                'completion_check': "Машқ бажарилди, агар сиз биринчи оила кенгашини барча беш банд бўйича ўтказган бўлсангиз ва иккалангиз ҳам бу фойдали эканини ҳис қилган бўлсангиз.",
            },
        },
        'duration_minutes': 30,
        'difficulty': 'beginner',
        'order_index': 7,
    },
]

PROGRAMS = [
    {
        'slug': '7-days-communication',
        'title': '7 дней улучшения общения',
        'description': 'Базовая программа для любой пары. Каждый день — маленькая практика, которая постепенно меняет качество ежедневного общения.',
        'duration_days': 7,
        'category_focus': 'communication',
        'cover_gradient': 'linear-gradient(135deg, #6558A8 0%, #4A88B8 100%)',
        'order_index': 1,
        'i18n': {
            'en': {
                'title': '7 Days of Better Communication',
                'description': 'A foundational program for any couple. Each day, a small practice that gradually transforms the quality of your daily communication.',
            },
            'uz': {
                'title': "Muloqotni yaxshilashning 7 kuni",
                'description': "Har qanday juftlik uchun asosiy dastur. Har kuni — kundalik muloqot sifatini asta-sekin o'zgartiradigan kichik mashq.",
            },
            'uz_cyrl': {
                'title': "Мулоқотни яхшилашнинг 7 куни",
                'description': "Ҳар қандай жуфтлик учун асосий дастур. Ҳар куни — кунлик мулоқот сифатини аста-секин ўзгартирадиган кичик машқ.",
            },
        },
        'days': [
            {
                'day_number': 1, 'title': 'Присутствие',
                'material': 'Большинство проблем в общении начинаются не с того, что мы говорим, а с того, насколько мы присутствуем. Сегодня изучите базовые принципы активного слушания: телесное присутствие, отражение содержания и эмоций.',
                'exercise': 'Проведите 10 минут разговора с партнёром без телефона и других отвлекающих факторов. Один говорит о своём дне, другой только слушает и задаёт уточняющие вопросы.',
                'reflection_prompt': 'Что было сложнее всего — не отвлекаться или не давать советов? Что заметил партнёр в вашем поведении?',
                'i18n': {
                    'en': {
                        'title': 'Presence',
                        'material': 'Most communication problems start not from what we say, but from how present we are. Today, learn the core principles of active listening: physical presence, reflecting content and emotions.',
                        'exercise': 'Spend 10 minutes talking with your partner without phones or other distractions. One person talks about their day, the other only listens and asks clarifying questions.',
                        'reflection_prompt': 'What was harder — not getting distracted or not giving advice? What did your partner notice about your behavior?',
                    },
                    'uz': {
                        'title': 'Hozirlik',
                        'material': "Ko'pchilik muloqot muammolari nima deymizdan emas, balki qanchalik hozir ekanligimizdan boshlanadi. Bugun faol tinglashning asosiy tamoyillarini o'rganing: jismoniy hozirlik, mazmun va his-tuyg'ularni aks ettirish.",
                        'exercise': "Telefon va boshqa chalg'ituvchilarsiz turmush o'rtoqingiz bilan 10 daqiqa gaplashing. Biri kuni haqida gapiradi, ikkinchisi faqat tinglaydi va aniqlashtiruvchi savollar beradi.",
                        'reflection_prompt': "Nima qiyinroq bo'ldi — chalg'imaslik yoki maslahat bermaslik? Turmush o'rtoqingiz xatti-harakatingizda nima sezdi?",
                    },
                    'uz_cyrl': {
                        'title': 'Ҳозирлик',
                        'material': 'Кўпчилик мулоқот муаммолари нима деймизданмас, балки қанчалик ҳозир эканлигимиздан бошланади. Бугун фаол тинглашнинг асосий тамойилларини ўрганинг: жисмоний ҳозирлик, мазмун ва ҳис-туйғуларни акс эттириш.',
                        'exercise': 'Телефон ва бошқа чалғитувчиларсиз турмуш ўртоғингиз билан 10 дақиқа гаплашинг. Бири куни ҳақида гапиради, иккинчиси фақат тинглайди ва аниқлаштирувчи саволлар беради.',
                        'reflection_prompt': 'Нима қийинроқ бўлди — чалғимаслик ёки маслаҳат бермаслик? Турмуш ўртоғингиз хатти-ҳаракатингизда нима сезди?',
                    },
                },
            },
            {
                'day_number': 2, 'title': 'Язык чувств',
                'material': 'Когда мы говорим «ты меня игнорируешь» — это обвинение. Когда мы говорим «мне одиноко, когда ты в телефоне» — это чувство. Второй вариант вызывает сочувствие, а не защиту.',
                'exercise': 'В течение дня замечайте момент, когда хочется сказать «ты [что-то делаешь не так]». Остановитесь и переформулируйте через «я чувствую [эмоция], когда [факт]». Вечером поделитесь примерами с партнёром.',
                'reflection_prompt': 'Какие эмоциональные слова вам удалось использовать? Как отреагировал партнёр на «я-высказывание»?',
                'i18n': {
                    'en': {
                        'title': 'Language of feelings',
                        'material': "When we say 'you're ignoring me' — that's an accusation. When we say 'I feel lonely when you're on your phone' — that's a feeling. The second approach creates empathy, not defensiveness.",
                        'exercise': "Throughout the day, notice moments when you want to say 'you [do something wrong]'. Stop and rephrase it as 'I feel [emotion] when [fact]'. In the evening, share your examples with your partner.",
                        'reflection_prompt': "What emotional words were you able to use? How did your partner respond to your 'I-statement'?",
                    },
                    'uz': {
                        'title': 'His tili',
                        'material': "«Sen meni e'tiborsiz qoldirasan» desak — bu ayblov. «Sen telefonda bo'lganda o'zimni yolg'iz his qilaman» desak — bu his. Ikkinchi variant ximoyalanishni emas, hamdardlikni uyg'otadi.",
                        'exercise': "Kun davomida «sen [noto'g'ri ish qilasan]» demoqchi bo'lgan onlarni sezib qoling. To'xtang va «men [his] his qilaman, [holat]da» tarzida qayta ifodalang. Kechqurun misollaringizni turmush o'rtoqingiz bilan bo'lishing.",
                        'reflection_prompt': "Qanday his so'zlarini ishlatishga muvaffaq bo'ldingiz? Turmush o'rtoqingiz «men-gapiga» qanday munosabat bildirdi?",
                    },
                    'uz_cyrl': {
                        'title': 'Ҳис тили',
                        'material': '«Сен мени эътиборсиз қолдирасан» десак — бу айблов. «Сен телефонда бўлганда ўзимни ёлғиз ҳис қиламан» десак — бу ҳис. Иккинчи вариант ҳимояланишни эмас, ҳамдардликни уйғотади.',
                        'exercise': '«Сен [нотўғри иш қиласан]» демоқчи бўлган онларни сезиб қолинг. Тўхтанг ва «мен [ҳис] ҳис қиламан, [ҳолат]да» тарзида қайта ифодаланг. Кечқурун мисолларингизни турмуш ўртоғингиз билан бўлишинг.',
                        'reflection_prompt': 'Қандай ҳис сўзларини ишлатишга муваффақ бўлдингиз? Турмуш ўртоғингиз «мен-гапига» қандай муносабат билдирди?',
                    },
                },
            },
            {
                'day_number': 3, 'title': 'Вопросы вместо ответов',
                'material': 'Открытые вопросы начинаются с «как», «что», «расскажи мне» и открывают пространство для разговора. Закрытые («ты устал?») получают ответ «да/нет». Сегодня практикуем открытые вопросы.',
                'exercise': 'Задайте партнёру сегодня минимум 5 открытых вопросов о его дне, мыслях, чувствах. Запишите вопросы, которые вам понравились.',
                'reflection_prompt': 'Какой вопрос вызвал самый неожиданный ответ? Что нового вы узнали о партнёре?',
                'i18n': {
                    'en': {
                        'title': 'Questions instead of answers',
                        'material': "Open-ended questions start with 'how', 'what', 'tell me' and create space for conversation. Closed questions ('are you tired?') get a yes/no answer. Today we practice open-ended questions.",
                        'exercise': 'Ask your partner at least 5 open-ended questions today about their day, thoughts and feelings. Write down the questions you liked best.',
                        'reflection_prompt': 'Which question prompted the most unexpected answer? What new things did you learn about your partner?',
                    },
                    'uz': {
                        'title': "Javoblar o'rniga savollar",
                        'material': "Ochiq savollar «qanday», «nima», «gapirib bering» bilan boshlanadi va suhbat uchun maydon ochadi. Yopiq savollar («charchadingizmi?») «ha/yo'q» javob oladi. Bugun ochiq savollarni mashq qilamiz.",
                        'exercise': "Bugun turmush o'rtoqingizga kuni, fikrlari, his-tuyg'ulari haqida kamida 5 ta ochiq savol bering. Yoqtirgan savollaringizni yozing.",
                        'reflection_prompt': "Qaysi savol eng kutilmagan javobni chiqardi? Turmush o'rtoqingiz haqida nima yangi narsalarni bildingiz?",
                    },
                    'uz_cyrl': {
                        'title': 'Жавоблар ўрнига саволлар',
                        'material': 'Очиқ саволлар «қандай», «нима», «гапириб беринг» билан бошланади ва суҳбат учун майдон очади. Ёпиқ саволлар («чарчадингизми?») «ҳа/йўқ» жавоб олади. Бугун очиқ саволларни машқ қиламиз.',
                        'exercise': 'Бугун турмуш ўртоғингизга куни, фикрлари, ҳис-туйғулари ҳақида камида 5 та очиқ савол беринг. Ёқтирган саволларингизни ёзинг.',
                        'reflection_prompt': 'Қайси савол энг кутилмаган жавобни чиқарди? Турмуш ўртоғингиз ҳақида нима янги нарсаларни билдингиз?',
                    },
                },
            },
            {
                'day_number': 4, 'title': 'Признание без «но»',
                'material': 'Признание — это когда вы показываете партнёру, что видите его усилия или чувства. «Я вижу, как ты устал» — это признание. «Я вижу, как ты устал, но...» — это отмена признания.',
                'exercise': 'Найдите сегодня три момента, когда можно выразить признание партнёру. Используйте формулу: «Я вижу/замечаю, что ты [наблюдение]. Это [важно / я ценю].» Никаких «но».',
                'reflection_prompt': 'Как партнёр реагировал на признание? Что было сложно в том, чтобы остановиться и не добавить «но»?',
                'i18n': {
                    'en': {
                        'title': 'Acknowledgment without "but"',
                        'material': "Acknowledgment is when you show your partner that you see their efforts or feelings. 'I see how tired you are' — that's acknowledgment. 'I see how tired you are, but...' — that cancels it.",
                        'exercise': "Find three moments today when you can express acknowledgment to your partner. Use the formula: 'I see/notice that you [observation]. That [matters / I appreciate it].' No 'but'.",
                        'reflection_prompt': "How did your partner respond to the acknowledgment? What was hard about stopping and not adding 'but'?",
                    },
                    'uz': {
                        'title': '«Lekin» siz tan olish',
                        'material': "Tan olish — bu turmush o'rtoqingizga uning sa'y-harakatlari yoki his-tuyg'ularini ko'rishingizni ko'rsatishdir. «Ko'ryapman, qanchalik charchaganingizni» — tan olish. «Ko'ryapman, qanchalik charchaganingizni, lekin...» — bu tan olishni bekor qilish.",
                        'exercise': "Bugun turmush o'rtoqingizga tan olishni ifodalash mumkin bo'lgan uch lahzani toping. Formuladan foydalaning: «Ko'ryapman/sezayapman, siz [kuzatuv]. Bu [muhim / qadrlayapman].» Hech qanday «lekin» yo'q.",
                        'reflection_prompt': "Turmush o'rtoqingiz tan olishga qanday munosabat bildirdi? To'xtab, «lekin» qo'shmaslik nima uchun qiyin edi?",
                    },
                    'uz_cyrl': {
                        'title': '«Лекин» сиз тан олиш',
                        'material': 'Тан олиш — бу турмуш ўртоғингизга унинг саъй-ҳаракатлари ёки ҳис-туйғуларини кўришингизни кўрсатишдир. «Кўряпман, қанчалик чарчаганингизни» — тан олиш. «Кўряпман, қанчалик чарчаганингизни, лекин...» — бу тан олишни бекор қилиш.',
                        'exercise': 'Бугун турмуш ўртоғингизга тан олишни ифодалаш мумкин бўлган уч лаҳзани топинг. Формуладан фойдаланинг: «Кўряпман/сезяпман, сиз [кузатув]. Бу [муҳим / қадрлаяпман].» Ҳеч қандай «лекин» йўқ.',
                        'reflection_prompt': 'Турмуш ўртоғингиз тан олишга қандай муносабат билдирди? Тўхтаб, «лекин» қўшмаслик нима учун қийин эди?',
                    },
                },
            },
            {
                'day_number': 5, 'title': 'Пауза и возврат',
                'material': 'Иногда лучшее, что можно сделать в разговоре — это взять паузу. Но пауза работает только если вы договорились о том, что вернётесь к разговору.',
                'exercise': 'Обсудите с партнёром: как вы сигнализируете друг другу, что вам нужна пауза? Придумайте кодовую фразу или жест. Договоритесь о том, как возвращаетесь к разговору после паузы.',
                'reflection_prompt': 'Что мешало вам брать паузы раньше? Как вы себя чувствуете, договорившись об этом заранее?',
                'i18n': {
                    'en': {
                        'title': 'Pause and return',
                        'material': 'Sometimes the best thing you can do in a conversation is to take a pause. But a pause only works if you have agreed that you will return to the conversation.',
                        'exercise': 'Discuss with your partner: how do you signal to each other that you need a pause? Come up with a code phrase or gesture. Agree on how you return to the conversation after a pause.',
                        'reflection_prompt': 'What prevented you from taking pauses before? How do you feel now that you have agreed on this in advance?',
                    },
                    'uz': {
                        'title': 'Tanaffus va qaytish',
                        'material': "Ba'zida suhbatda qilishingiz mumkin bo'lgan eng yaxshi narsa — tanaffus olish. Ammo tanaffus faqat suhbatga qaytishga kelishib olgan bo'lsangiz ishlaydi.",
                        'exercise': "Turmush o'rtoqingiz bilan muhokama qiling: bir-biringizga tanaffus kerakligini qanday signal berasiz? Kod so'z yoki imo-ishora o'ylab toping. Tanaffusdan keyin suhbatga qanday qaytishingizni kelishib oling.",
                        'reflection_prompt': "Avval tanaffus olishingizga nima to'sqinlik qildi? Buni oldindan kelishib olganingizdan so'ng o'zingizni qanday his qilyapsiz?",
                    },
                    'uz_cyrl': {
                        'title': 'Танаффус ва қайтиш',
                        'material': "Баъзида суҳбатда қилишингиз мумкин бўлган энг яхши нарса — танаффус олиш. Аммо танаффус фақат суҳбатга қайтишга келишиб олган бўлсангиз ишлайди.",
                        'exercise': 'Турмуш ўртоғингиз билан муҳокама қилинг: бир-биringiзга танаффус кераклигини қандай сигнал берасиз? Код сўз ёки имо-ишора ўйлаб топинг. Танаффусдан кейин суҳбатга қандай қайтишингизни келишиб олинг.',
                        'reflection_prompt': 'Аввал танаффус олишингизга нима тўсқинлик қилди? Буни олдиндан келишиб олганингиздан сўнг ўзингизни қандай ҳис қиляпсиз?',
                    },
                },
            },
            {
                'day_number': 6, 'title': 'Один разговор — одна тема',
                'material': 'Один из самых разрушительных паттернов — когда в середине обсуждения одной темы вдруг появляется «а вот ты три месяца назад...». Это называется «кухонный пожар» — всё горит одновременно.',
                'exercise': 'Выберите одну небольшую тему, по которой у вас есть разногласие. Обсудите её от начала до конца, не переходя на другие темы, не вспоминая прошлое. Если другая тема «вылезла» — запишите её и договоритесь обсудить отдельно.',
                'reflection_prompt': 'Удалось ли удержаться в рамках одной темы? Что помогало? Что тянуло на другие темы?',
                'i18n': {
                    'en': {
                        'title': 'One conversation — one topic',
                        'material': "One of the most destructive patterns is when, in the middle of discussing one topic, 'but three months ago you...' suddenly appears. This is called 'kitchen fire' — everything burns at once.",
                        'exercise': 'Choose one small topic where you have a disagreement. Discuss it from start to finish without switching to other topics or bringing up the past. If another topic comes up — write it down and agree to discuss it separately.',
                        'reflection_prompt': 'Were you able to stay on one topic? What helped? What pulled you toward other topics?',
                    },
                    'uz': {
                        'title': 'Bir suhbat — bir mavzu',
                        'material': "Eng halokatli naqshlardan biri — bir mavzuni muhokama qilish o'rtasida «uch oy oldin esa sen...» paydo bo'lganda. Bu «oshxona yong'ini» deb ataladi — hamma narsa bir vaqtda yonadi.",
                        'exercise': "Kelishmovchilik mavjud bitta kichik mavzuni tanlang. Uni boshidan oxirigacha, boshqa mavzularga o'tmasdan, o'tmishni eslamasdan muhokama qiling. Boshqa mavzu chiqib kelsa — uni yozing va alohida muhokama qilishga kelishing.",
                        'reflection_prompt': "Bitta mavzu doirasida qolishga muvaffaq bo'ldingizmi? Nima yordam berdi? Nima boshqa mavzularga tortdi?",
                    },
                    'uz_cyrl': {
                        'title': 'Бир суҳбат — бир мавзу',
                        'material': 'Энг ҳалокатли нақшлардан бири — бир мавзуни муҳокама қилиш ўртасида «уч ой олдин эса сен...» пайдо бўлганда. Бу «ошхона ёнғини» деб аталади — ҳамма нарса бир вақтда ёнади.',
                        'exercise': 'Келишмовчилик мавжуд биттакичик мавзуни танланг. Уни бошидан охиригача, бошқа мавзуларга ўтмасдан, ўтмишни эсламасдан муҳокама қилинг. Бошқа мавзу чиқиб келса — уни ёзинг ва алоҳида муҳокама қилишга келишинг.',
                        'reflection_prompt': 'Битта мавзу доирасида қолишга муваффақ бўлдингизми? Нима ёрдам берди? Нима бошқа мавзуларга тортди?',
                    },
                },
            },
            {
                'day_number': 7, 'title': 'Разговор об общении',
                'material': 'Метакоммуникация — разговор о том, как вы общаетесь. Это один из самых мощных инструментов. Счастливые пары умеют говорить о своих способах общения без обвинений.',
                'exercise': 'Проведите 20-минутный разговор на тему: «Как нам лучше общаться?» Каждый называет одно, что ему нравится в общении с партнёром, и одно, что хотелось бы улучшить (в формате «мне хотелось бы...», а не «ты должен...»).',
                'reflection_prompt': 'Что изменилось за эту неделю? Какая практика была самой полезной? Что хотите продолжать делать?',
                'i18n': {
                    'en': {
                        'title': 'Talking about communication',
                        'material': 'Metacommunication — talking about how you communicate — is one of the most powerful tools. Happy couples know how to discuss their communication styles without blame.',
                        'exercise': "Have a 20-minute conversation on the topic: 'How can we communicate better?' Each person names one thing they like about communicating with their partner and one thing they'd like to improve (in the format 'I would like...' not 'you should...').",
                        'reflection_prompt': 'What changed this week? Which practice was most useful? What do you want to continue doing?',
                    },
                    'uz': {
                        'title': 'Muloqot haqida suhbat',
                        'material': "Metakommunikatsiya — muloqot qilish uslubingiz haqida gaplashish — eng kuchli vositalardan biri. Baxtli juftliklar ayblov qilmasdan muloqot uslublari haqida gaplasha olishadi.",
                        'exercise': "«Muloqotimizni qanday yaxshilash mumkin?» mavzusida 20 daqiqalik suhbat o'tkazing. Har biri turmush o'rtoqi bilan muloqotda yoqtirgan bitta narsasini va yaxshilamoqchi bo'lgan bitta narsasini aytadi («xohlardim...» formatida, «siz kerak...» emas).",
                        'reflection_prompt': "Bu hafta nima o'zgardi? Qaysi mashq eng foydali bo'ldi? Nima qilishni davom ettirishni xohlaysiz?",
                    },
                    'uz_cyrl': {
                        'title': 'Мулоқот ҳақида суҳбат',
                        'material': 'Метакоммуникация — мулоқот қилиш услубингиз ҳақида гаплашиш — энг кучли воситалардан бири. Бахтли жуфтликлар айблов қилмасдан мулоқот услублари ҳақида гаплаша олишади.',
                        'exercise': '«Мулоқотимизни қандай яхшилаш мумкин?» мавзусида 20 дақиқалик суҳбат ўтказинг. Ҳар бири турмуш ўртоғи билан мулоқотда ёқтирган битта нарсасини ва яхшиламоқчи бўлган битта нарсасини айтади («хоҳлардим...» форматида, «сиз керак...» эмас).',
                        'reflection_prompt': 'Бу ҳафта нима ўзгарди? Қайси машқ энг фойдали бўлди? Нима қилишни давом эттиришни хоҳлайсиз?',
                    },
                },
            },
        ],
    },
    {
        'slug': '14-days-trust',
        'title': '14 дней восстановления доверия',
        'description': 'Глубокая программа для пар, которые хотят восстановить или укрепить доверие. Основана на исследованиях Готтмана и теории привязанности.',
        'duration_days': 14,
        'category_focus': 'trust',
        'i18n': {
            'en': {
                'title': '14 Days of Rebuilding Trust',
                'description': 'A deep program for couples who want to restore or strengthen trust. Based on research by Gottman and attachment theory.',
            },
            'uz': {
                'title': "Ishonchni qayta tiklashning 14 kuni",
                'description': "Ishonchni tiklash yoki mustahkamlashni istagan juftliklar uchun chuqur dastur. Gottman tadqiqotlari va ilova nazariyasiga asoslangan.",
            },
            'uz_cyrl': {
                'title': "Ишончни қайта тиклашнинг 14 куни",
                'description': "Ишончни тиклаш ёки мустаҳкамлашни истаган жуфтликлар учун чуқур дастур. Готтман тадқиқотлари ва илова назариясига асосланган.",
            },
        },
        'cover_gradient': 'linear-gradient(135deg, #5A9E80 0%, #4A88B8 100%)',
        'order_index': 2,
        'days': [
            {
                'day_number': 1, 'title': 'Что такое доверие для нас',
                'material': 'Доверие — не одно понятие. Для одного это предсказуемость, для другого — честность, для третьего — поддержка. Важно понять, как каждый из вас определяет доверие.',
                'exercise': 'Каждый напишет 3 ответа на вопрос: «Я чувствую себя в безопасности с тобой, когда...» Поделитесь ответами.',
                'reflection_prompt': 'Совпали ли ваши представления о доверии? Что вас удивило?',
            },
            {
                'day_number': 2, 'title': 'Надёжность в малом',
                'material': 'Доверие строится не в грандиозных жестах, а в последовательности маленьких действий. «Я сказал — я сделал». Сегодня сфокусируемся на надёжности в обычных ситуациях.',
                'exercise': 'Каждый называет 3 маленьких обещания, которые выполнит сегодня. Вечером отмечаете результат.',
                'reflection_prompt': 'Как вы себя чувствуете, когда партнёр держит слово, даже в мелочах?',
            },
            {
                'day_number': 3, 'title': 'Признание ошибок',
                'material': 'Способность признавать ошибки без защитных реакций — ключевой компонент доверия. Это не слабость, а проявление зрелости и уважения к партнёру.',
                'exercise': 'Каждый вспоминает одну ситуацию за последний месяц, где он был неправ или мог поступить лучше. Признаёт это партнёру без объяснений и без «но».',
                'reflection_prompt': 'Что было сложным в признании? Как почувствовал себя партнёр, услышав это?',
            },
            {
                'day_number': 4, 'title': 'Хранить тайны',
                'material': 'Конфиденциальность — основа доверия. Что остаётся между нами? Что можно рассказывать другим? Многие пары никогда не обговаривали эти границы.',
                'exercise': 'Обсудите: что из нашей личной жизни остаётся только между нами? Где границы того, что можно рассказывать друзьям / родителям?',
                'reflection_prompt': 'Были ли у вас ситуации, когда граница конфиденциальности нарушалась? Как вы к этому относитесь теперь?',
            },
            {
                'day_number': 5, 'title': 'Честность без жестокости',
                'material': 'Честность — не значит говорить всё, что думаешь, в любой момент. Это говорить правду с заботой о партнёре. «Добрая правда» — искусство, которому можно научиться.',
                'exercise': 'Поговорите о чём-то, что вы обычно замалчиваете из страха расстроить партнёра. Используйте формулу: «Я хочу быть честным, потому что уважаю тебя. Хочу сказать...»',
                'reflection_prompt': 'Что помогало и что мешало быть честным? Как партнёр принял вашу честность?',
            },
            {
                'day_number': 6, 'title': 'Непоследовательность',
                'material': 'Один из самых разрушительных для доверия паттернов — когда слова расходятся с делами. «Я всегда буду рядом», но в трудный момент — исчезает. Сегодня честно смотрим на это.',
                'exercise': 'Каждый честно отвечает: «Есть ли область, где мои слова расходятся с делами? Что я хочу изменить?» Поделитесь.',
                'reflection_prompt': 'Было ли страшно признать это вслух? Что вы почувствовали, услышав партнёра?',
            },
            {
                'day_number': 7, 'title': 'Неделя доверия: итог',
                'material': 'Конец первой недели. Доверие восстанавливается медленно — через накопленные доказательства надёжности. Важно отметить прогресс.',
                'exercise': 'Каждый называет одно действие партнёра за эту неделю, которое укрепило доверие. Затем называет одно маленькое обязательство на следующую неделю.',
                'reflection_prompt': 'Что изменилось за эту неделю? Что чувствуете сейчас по отношению к теме доверия?',
            },
            {
                'day_number': 8, 'title': 'История наших отношений',
                'material': 'Один из методов Готтмана — «переписать» историю отношений в позитивном ключе. Пары, которые помнят хорошее начало, легче переживают трудные периоды.',
                'exercise': 'Расскажите друг другу историю вашего знакомства и начала отношений. Что привлекло вас тогда? Что было особенным?',
                'reflection_prompt': 'Что вы почувствовали, вспоминая начало? Что из того времени хотели бы вернуть?',
            },
            {
                'day_number': 9, 'title': 'Страхи в отношениях',
                'material': 'У каждого из нас есть страхи в отношениях: быть брошенным, контролируемым, недостаточным. Когда мы говорим об этом, страхи теряют власть.',
                'exercise': 'Поделитесь одним своим страхом в отношениях. Используйте формулу: «Иногда я боюсь, что...» Партнёр только слушает и говорит: «Спасибо, что доверил мне это».',
                'reflection_prompt': 'Что значило для вас поделиться этим? Как вы себя чувствуете, зная о страхе партнёра?',
            },
            {
                'day_number': 10, 'title': 'Ремонт отношений',
                'material': 'Попытки примирения — это жесты, которые останавливают эскалацию. Это может быть юмор, прикосновение, слово «стоп». Важно, чтобы партнёр их принимал.',
                'exercise': 'Обсудите: что для каждого из вас лучший способ «перезагрузить» разговор, когда он идёт плохо? Придумайте общий сигнал.',
                'reflection_prompt': 'Были ли ситуации, когда попытка примирения была отвергнута? Почему, как вы думаете?',
            },
            {
                'day_number': 11, 'title': 'Великодушие интерпретации',
                'material': 'Трактуйте действия партнёра в лучшую сторону. «Он опоздал, потому что не уважает моё время» vs «Он опоздал, возможно, что-то случилось». Недоверие строит негативные нарративы.',
                'exercise': 'Вспомните 3 ситуации, когда вы интерпретировали действие партнёра в худшую сторону. Переформулируйте каждую ситуацию в «благожелательную интерпретацию».',
                'reflection_prompt': 'Как изменилось ваше чувство к ситуации при новой интерпретации?',
            },
            {
                'day_number': 12, 'title': 'Обещание как ритуал',
                'material': 'Маленькие, выполняемые обещания создают доверие быстрее, чем большие. Ритуал «я обещаю» может стать якорем для надёжности.',
                'exercise': 'Каждый называет одно конкретное обещание на следующие 30 дней — что-то небольшое, но значимое для партнёра. Запишите и поставьте напоминание.',
                'reflection_prompt': 'Почему именно это обещание важно для партнёра? Что вам нужно, чтобы его выполнить?',
            },
            {
                'day_number': 13, 'title': 'Доверие к себе',
                'material': 'Трудно доверять партнёру, если не доверяем себе. Сегодня — честный взгляд на то, насколько мы доверяем своим чувствам и решениям.',
                'exercise': 'Ответьте письменно: «В чём я доверяю себе больше всего? В чём мне сложно доверять себе? Как это влияет на наши отношения?»',
                'reflection_prompt': 'Поделитесь с партнёром одним из ответов. Что он мог не знать о вас до сегодня?',
            },
            {
                'day_number': 14, 'title': '14 дней: итог и новый договор',
                'material': 'Две недели работы над доверием — это серьёзно. Доверие — не пункт назначения, а постоянная практика. Сегодня создаём «договор о доверии».',
                'exercise': 'Напишите вместе короткий «договор»: 3-5 конкретных вещей, которые каждый обязуется делать для поддержания доверия. Подпишите.',
                'reflection_prompt': 'Что изменилось за эти две недели? Как вы себя чувствуете сейчас по отношению к партнёру?',
            },
        ],
    },
    {
        'slug': '21-days-intimacy',
        'title': '21 день эмоциональной близости',
        'description': 'Программа для пар, которые хотят углубить эмоциональную связь и лучше понять внутренний мир друг друга.',
        'duration_days': 21,
        'category_focus': 'intimacy',
        'cover_gradient': 'linear-gradient(135deg, #A8755E 0%, #6558A8 100%)',
        'order_index': 3,
        'i18n': {
            'en': {
                'title': '21 Days of Emotional Intimacy',
                'description': 'A program for couples who want to deepen their emotional connection and better understand each other\'s inner world.',
            },
            'uz': {
                'title': "Hissiy yaqinlikning 21 kuni",
                'description': "Hissiy bog'liqlikni chuqurlashtirish va bir-birining ichki dunyosini yaxshiroq tushunishni istagan juftliklar uchun dastur.",
            },
            'uz_cyrl': {
                'title': "Ҳиссий яқинликнинг 21 куни",
                'description': "Ҳиссий боғлиқликни чуқурлаштириш ва бир-бирининг ички дунёсини яхшироқ тушунишни истаган жуфтликлар учун дастур.",
            },
        },
        'days': [
            {
                'day_number': 1, 'title': 'Карта внутреннего мира',
                'material': 'Готтман называет глубокое знание внутреннего мира партнёра «картой любви». Это знание его страхов, надежд, ценностей, воспоминаний. Сегодня начинаем её обновлять.',
                'exercise': 'Задайте друг другу по 3 вопроса из списка: «Что тебя сейчас больше всего радует? Какой твой самый большой страх прямо сейчас? Что ты мечтаешь сделать, но ещё не сделал?»',
                'reflection_prompt': 'Что вас удивило в ответах партнёра? Что вы узнали нового?',
            },
            {
                'day_number': 2, 'title': 'История привязанности',
                'material': 'То, как нас любили в детстве, влияет на то, как мы любим и принимаем любовь сегодня. Понимание стиля привязанности партнёра — ключ к эмпатии.',
                'exercise': 'Расскажите друг другу об одном важном воспоминании из детства, связанном с любовью или заботой. Как оно влияет на вас сейчас?',
                'reflection_prompt': 'Что вы почувствовали, услышав историю партнёра? Как это меняет ваше понимание его реакций?',
            },
            {
                'day_number': 3, 'title': 'Момент полного присутствия',
                'material': 'Близость требует присутствия — не физического, а эмоционального. Сегодня практикуем полное присутствие без отвлечений.',
                'exercise': '30 минут вместе без телефонов, задач, экранов. Делайте что-то простое: готовьте вместе, гуляйте, сидите. Просто будьте рядом.',
                'reflection_prompt': 'Что было странным или приятным в этих 30 минутах? Насколько часто вы бываете вот так вместе?',
            },
            {
                'day_number': 4, 'title': 'Язык тела и близость',
                'material': 'Исследования показывают: до 70% эмоционального сообщения передаётся невербально. Прикосновение, взгляд, поза, расстояние — всё это создаёт или разрушает близость. Многие пары со временем перестают касаться друг друга без сексуального контекста.',
                'exercise': 'В течение дня инициируйте три несексуальных прикосновения: рука на плече, объятие, сжатие ладони. Обратите внимание, как партнёр реагирует и как вы себя чувствуете.',
                'reflection_prompt': 'Насколько комфортно вам давать и получать прикосновения вне сексуального контекста? Что изменилось за день?',
            },
            {
                'day_number': 5, 'title': 'Уязвимость как дверь',
                'material': 'Брене Браун провела 20 лет, изучая стыд и уязвимость. Её главное открытие: уязвимость — это не слабость. Это единственный путь к настоящей близости. Мы не можем выборочно отключать неудобные чувства — когда мы их блокируем, мы блокируем и радость, и любовь.',
                'exercise': 'Поделитесь с партнёром чем-то, о чём обычно молчите. Это может быть страх, сомнение в себе, что-то, за что вам стыдно или что кажется «слишком маленьким». Партнёр только слушает и говорит: «Я рад, что ты мне это сказал».',
                'reflection_prompt': 'Что вы почувствовали, делясь этим? Как ощущается, когда вас принимают уязвимым?',
            },
            {
                'day_number': 6, 'title': 'Мечты вслух',
                'material': 'У каждого из нас есть мечты, которые мы давно не произносили вслух. Иногда — потому что боимся быть непонятыми, иногда — потому что сами не решаемся в них верить. Когда партнёр знает наши мечты, он может стать союзником, а не источником сомнений.',
                'exercise': 'Каждый называет две мечты: одну маленькую (что-то, что хочется сделать в этом году) и одну большую (что-то на 5-10 лет вперёд). Другой только слушает и задаёт вопросы «расскажи больше», не оценивая реалистичность.',
                'reflection_prompt': 'Как ощущалось называть свои мечты вслух? Что вы узнали о мечтах партнёра, чего не знали раньше?',
            },
            {
                'day_number': 7, 'title': 'Неделя близости: итог',
                'material': 'Первая неделя позади. Вы говорили о внутреннем мире, прикасались, были уязвимыми, делились мечтами. Близость — это не одно большое событие, а сумма маленьких моментов. Сегодня замечаем накопленное.',
                'exercise': 'Каждый называет один момент за эту неделю, когда почувствовал себя по-настоящему близким к партнёру. Опишите, что происходило, что было сказано, что вы при этом ощущали.',
                'reflection_prompt': 'Что из практик этой недели вы хотите сохранить? Что было самым неожиданным?',
            },
            {
                'day_number': 8, 'title': 'Прошлые раны',
                'material': 'Каждый из нас приходит в отношения с историей — опытом боли, разочарований, потерь. Эти раны часто «активируются» в отношениях, особенно в моменты стресса. Понимание прошлого партнёра — ключ к состраданию в настоящем.',
                'exercise': 'Поделитесь одним болезненным опытом из прошлого (не из ваших отношений), который, как вам кажется, влияет на то, как вы ведёте себя сейчас. Партнёр слушает, не даёт советов, не сравнивает.',
                'reflection_prompt': 'Как этот опыт влияет на ваши нынешние реакции? Что партнёр может сделать, зная это?',
            },
            {
                'day_number': 9, 'title': 'Мои потребности в близости',
                'material': 'У людей разные потребности в близости. Один нуждается в ежедневных долгих разговорах, другому достаточно тихого присутствия рядом. Это не значит, что один любит больше. Это разные «языки близости».',
                'exercise': 'Каждый честно отвечает: «Как я чувствую себя любимым больше всего? Что для меня означает "нам хорошо вместе"?» Запишите 3-5 конкретных ответа и поделитесь с партнёром.',
                'reflection_prompt': 'Совпадают ли ваши потребности? Где разница? Как вы можете учитывать её?',
            },
            {
                'day_number': 10, 'title': 'Ритуалы связи',
                'material': 'Готтман называет «ритуалами связи» маленькие, регулярные моменты, которые создают ощущение «мы». Это не крупные события, а ежедневные ниточки: как вы здороваетесь, как прощаетесь, как заканчиваете вечер.',
                'exercise': 'Составьте список из 3-5 ритуалов, которые уже есть у вас. Затем вместе выберите один новый ритуал связи, который хотите добавить. Опишите его: когда, как, что именно.',
                'reflection_prompt': 'Какой из ваших существующих ритуалов вам особенно дорог? Почему?',
            },
            {
                'day_number': 11, 'title': 'Конфликт и близость',
                'material': 'Многие избегают конфликтов, чтобы «сохранить близость». Но исследования показывают: умение проходить через конфликт и возвращаться к близости — один из главных маркеров крепких отношений. Конфликт — не разрушение близости, а возможность её углубить.',
                'exercise': 'Вспомните конфликт, после которого вы почувствовали себя ближе к партнёру. Что помогло? Поговорите о том, как вы хотели бы восстанавливать близость после разногласий.',
                'reflection_prompt': 'Как выглядит «возврат к близости» после конфликта у вас? Что могло бы помочь делать это быстрее?',
            },
            {
                'day_number': 12, 'title': 'Сила прощения',
                'material': 'Прощение — не значит «делать вид, что ничего не было». Это значит отпустить обиду ради себя и отношений. Исследования Роберта Энрайта показывают: люди, практикующие прощение, имеют лучшее психическое и физическое здоровье.',
                'exercise': 'Есть ли что-то небольшое (не острое), что вы до сих пор несёте в себе из прошлого в ваших отношениях? Назовите это и скажите партнёру: «Я хочу отпустить это.» Партнёр говорит: «Я слышу тебя. Спасибо.»',
                'reflection_prompt': 'Как вам ощущение после этого? Что мешает прощать быстрее?',
            },
            {
                'day_number': 13, 'title': 'Восхищение',
                'material': 'Со временем пары перестают замечать друг в друге то, что когда-то восхищало. Привыкание — нейрологический процесс. Но восхищение можно возродить намеренно — через внимание к конкретным качествам партнёра.',
                'exercise': 'Напишите партнёру список из 5 качеств, которые вас восхищают в нём — конкретных, с примерами. Прочитайте вслух. Партнёр только принимает, не преуменьшает.',
                'reflection_prompt': 'Что из списка партнёра вас удивило? Что было приятно слышать больше всего?',
            },
            {
                'day_number': 14, 'title': 'Две недели: пауза',
                'material': 'Половина пути. За эти две недели вы говорили о прошлом, уязвимости, потребностях, прощении. Близость — это не состояние, а процесс. Сегодня — момент осознанной остановки.',
                'exercise': 'Сядьте напротив друг друга на 5 минут в тишине. Смотрите друг другу в глаза. Потом каждый произносит одно предложение: «Рядом с тобой я чувствую...»',
                'reflection_prompt': 'Как ощущалось молчание вдвоём? Что всплыло в эти минуты?',
            },
            {
                'day_number': 15, 'title': 'Общие ценности',
                'material': 'Близость строится не только на чувствах, но и на общем фундаменте ценностей. Исследования показывают: пары с более совпадающими ценностями имеют более высокое удовлетворение отношениями. Но важно именно обсуждать их, а не предполагать совпадение.',
                'exercise': 'Каждый называет 5 самых важных ценностей (честность, семья, свобода, рост, безопасность и т.д.). Сравните. Обсудите 1-2 ценности, где есть различие — без оценки, с любопытством.',
                'reflection_prompt': 'Что вас удивило? Где ваши ценности удачно дополняют друг друга?',
            },
            {
                'day_number': 16, 'title': 'Личное пространство и близость',
                'material': 'Близость не означает слияние. Каждому из нас нужно личное пространство — время наедине с собой, своё занятие, своя зона. Парадокс близости: чем безопаснее каждый чувствует себя в своей отдельности, тем глубже возможна близость.',
                'exercise': 'Поговорите: сколько времени в одиночестве нужно каждому из вас в неделю? Как вы относитесь к тому, что партнёр хочет побыть один? Как сообщать об этой потребности без обиды?',
                'reflection_prompt': 'Удаётся ли вам уважать потребность партнёра в пространстве? Что мешает?',
            },
            {
                'day_number': 17, 'title': 'Доверие своим чувствам',
                'material': 'Иногда мы обесцениваем собственные чувства — «это глупо расстраиваться из-за этого». Но в отношениях умение называть и доверять своим чувствам — основа настоящего контакта. Когда мы не говорим о чувствах, партнёр не может нас понять.',
                'exercise': 'В течение дня три раза остановитесь и спросите себя: «Что я сейчас чувствую?» Вечером поделитесь с партнёром одним чувством, которое вы заметили в себе, — не мнением, а именно чувством.',
                'reflection_prompt': 'Легко ли вам называть свои чувства? Что мешает говорить о них с партнёром?',
            },
            {
                'day_number': 18, 'title': 'История, которую мы рассказываем',
                'material': 'У каждой пары есть «нарратив отношений» — история о том, кто вы есть вместе, как вы встретились, через что прошли. Готтман обнаружил: пары с позитивным нарративом легче переживают трудные периоды.',
                'exercise': 'Расскажите друг другу историю ваших отношений — с самого начала. Каждый рассказывает свою версию. Обратите внимание: что вы выделяете? Что считаете важным?',
                'reflection_prompt': 'Что общего в ваших версиях? Что разное? Какие моменты каждый считает поворотными?',
            },
            {
                'day_number': 19, 'title': 'Письмо партнёру',
                'material': 'Написанное слово создаёт особый вид близости. Оно требует замедлиться, выбирать слова, быть точным. Многие пары, регулярно пишущие друг другу — пусть даже короткие записки — сообщают о более высоком уровне удовлетворённости.',
                'exercise': 'Напишите партнёру письмо — от руки или в мессенджере — объёмом хотя бы 5-7 предложений. О чём угодно: что вы цените в нём, что вас тронуло недавно, что вы хотите, чтобы он знал.',
                'reflection_prompt': 'Что было в письме партнёра, что особенно задело? Что вы почувствовали, когда писали?',
            },
            {
                'day_number': 20, 'title': 'Видение будущего вместе',
                'material': 'Пары с общим видением будущего чувствуют большую связь. Это не просто планы — это разговор о том, какую жизнь вы хотите создать вместе, что для вас важно через 10 лет.',
                'exercise': 'Каждый описывает: «Какой будет наша жизнь через 10 лет в лучшем варианте?» Включите: где живёте, как проводите время, как выглядят ваши отношения, что вас радует в жизни. Поделитесь и найдите общее.',
                'reflection_prompt': 'Где ваши видения совпадают? Что вы хотите начать строить уже сейчас?',
            },
            {
                'day_number': 21, 'title': '21 день: итог и договор близости',
                'material': 'Три недели работы над близостью. Вы прошли через уязвимость, прощение, мечты, ценности, восхищение. Близость — не пункт назначения. Это выбор, который делается каждый день.',
                'exercise': 'Создайте вместе «договор близости» — 3-5 конкретных обязательств, которые каждый берёт на себя для поддержания эмоциональной близости. Запишите. Договоритесь вернуться к нему через месяц.',
                'reflection_prompt': 'Что изменилось за эти 21 день? Что вы хотите продолжать? Какое открытие о партнёре было самым важным?',
            },
        ],
    },
    {
        'slug': '30-days-family',
        'title': '30 дней укрепления семьи',
        'description': 'Комплексная программа, охватывающая все ключевые аспекты семейной жизни. Один шаг в день к более осознанным и счастливым отношениям.',
        'duration_days': 30,
        'category_focus': 'communication',
        'cover_gradient': 'linear-gradient(135deg, #B8904A 0%, #5A9E80 100%)',
        'order_index': 4,
        'i18n': {
            'en': {
                'title': '30 Days of Family Strengthening',
                'description': 'A comprehensive program covering all key aspects of family life. One step a day toward more conscious and happy relationships.',
            },
            'uz': {
                'title': "Oilani mustahkamlashning 30 kuni",
                'description': "Oilaviy hayotning barcha asosiy jihatlarini qamrab oluvchi keng qamrovli dastur. Ongliroq va baxtliroq munosabatlarga kunlik bir qadam.",
            },
            'uz_cyrl': {
                'title': "Оилани мустаҳкамлашнинг 30 куни",
                'description': "Оилавий ҳаётнинг барча асосий жиҳатларини қамраб олувчи кенг қамровли дастур. Онглироқ ва бахтлироқ муносабатларга кунлик бир қадам.",
            },
        },
        'days': [
            {
                'day_number': 1, 'title': 'Зачем мы вместе',
                'material': 'Исследования показывают: пары, которые могут ответить на вопрос «зачем мы вместе», имеют более устойчивые отношения. Смысл отношений — это не данность, а то, что нужно создавать.',
                'exercise': 'Каждый письменно отвечает: «Что делает наши отношения ценными для меня? Что я хочу, чтобы мы создали вместе?» Поделитесь ответами.',
                'reflection_prompt': 'Совпадает ли ваше видение смысла отношений? Что вас объединяет больше всего?',
            },
            {
                'day_number': 2, 'title': 'Первое «спасибо» дня',
                'material': 'Позитивный старт дня задаёт тон всему остальному. Маленький ритуал утренней благодарности — один из самых простых способов поднять общее качество отношений.',
                'exercise': 'С сегодняшнего дня: каждое утро говорите партнёру одну конкретную вещь, за которую вы благодарны. Начните прямо сейчас.',
                'reflection_prompt': 'Как это ощущалось? Легко или непривычно? Что сказал партнёр?',
            },
            # --- Неделя 1: Общение ---
            {
                'day_number': 3, 'title': 'Слушаю, не перебивая',
                'material': 'По данным исследований, средний человек перебивает собеседника уже через 17 секунд. В паре это превращается в привычку, которая постепенно разрушает ощущение «меня слышат». Сегодня практикуем настоящее слушание.',
                'exercise': 'Поговорите 15 минут: один говорит о своём дне или о чём-то важном — другой только слушает и задаёт уточняющие вопросы. Без советов, без перебиваний. Затем поменяйтесь.',
                'reflection_prompt': 'Что было труднее — говорить или слушать? Что заметил партнёр в вашем поведении?',
            },
            {
                'day_number': 4, 'title': 'Язык «я»',
                'material': '«Ты никогда не слушаешь» — обвинение, которое вызывает защиту. «Мне одиноко, когда я рассказываю и не получаю ответа» — чувство, которое вызывает сочувствие. Разница в одном слове: «ты» или «я».',
                'exercise': 'Вечером поговорите о чём-то, что вас беспокоит в паре — обязательно в формате «я чувствую..., когда..., потому что...». Избегайте «ты делаешь» и «ты всегда».',
                'reflection_prompt': 'Как изменился разговор, когда вы говорили о себе, а не о партнёре? Что почувствовал партнёр?',
            },
            {
                'day_number': 5, 'title': 'Вопросы вглубь',
                'material': 'Большинство ежедневных разговоров в паре остаются на поверхности: «как дела», «что на ужин», «видел новости». Более глубокие вопросы создают настоящий контакт. Их нужно задавать специально.',
                'exercise': 'Сегодня задайте партнёру три вопроса, которые вы обычно не задаёте: о его мыслях, переживаниях, мечтах. Например: «Что тебя сейчас больше всего занимает?», «Есть ли что-то, о чём ты хочешь поговорить, но не знаешь, как начать?»',
                'reflection_prompt': 'Что нового вы узнали о партнёре? Какой вопрос открыл самый неожиданный разговор?',
            },
            {
                'day_number': 6, 'title': 'Признание без «но»',
                'material': 'Признание — это показать партнёру, что вы видите его усилия, его состояние, его вклад. Признание обнуляется, если после него идёт «но». «Я вижу, как ты старался, но...» — это критика с маскировкой.',
                'exercise': 'Найдите сегодня три момента, чтобы выразить признание: «Я вижу, что ты [наблюдение]. Это [важно для меня / я ценю / это помогает мне].» Никаких «но» и продолжений.',
                'reflection_prompt': 'Как партнёр реагировал? Что было сложно в том, чтобы остановиться и не добавить «но»?',
            },
            {
                'day_number': 7, 'title': 'Итог первой недели общения',
                'material': 'Первая неделя была о качестве ежедневного общения. Эти навыки — слушание, «я-высказывания», признание — не инструменты для кризиса. Они работают именно в обычные дни.',
                'exercise': 'Проведите «семейный совет» на 20 минут: что прошло хорошо на этой неделе? Что было сложным? Что хотите делать иначе? Каждый говорит по очереди, другой только слушает.',
                'reflection_prompt': 'Что из практик этой недели хотите сохранить? Что вас удивило в партнёре?',
            },
            # --- Неделя 2: Доверие ---
            {
                'day_number': 8, 'title': 'Что разрушает доверие',
                'material': 'Брене Браун исследовала доверие и обнаружила: оно разрушается не столько через большие предательства, сколько через накопление маленьких моментов невнимания, непоследовательности, пренебрежения. Осознать паттерн — первый шаг.',
                'exercise': 'Каждый честно отвечает письменно: «Есть ли что-то, что я делаю (или не делаю), что может подрывать доверие партнёра ко мне?» Поделитесь ответами. Партнёр не спорит, не критикует — только слушает.',
                'reflection_prompt': 'Что вам далось тяжелее — писать или слушать? Что вы хотите изменить?',
            },
            {
                'day_number': 9, 'title': 'Слово, которое держат',
                'material': 'Надёжность строится через последовательность: сказал — сделал. Даже маленькие несдержанные обещания («я перезвоню», «сделаю завтра») постепенно подтачивают доверие. И наоборот — выполненные мелочи создают фундамент.',
                'exercise': 'Каждый называет три конкретных обещания, которые выполнит сегодня. Это должны быть реальные, выполнимые вещи. Вечером отчитайтесь друг другу.',
                'reflection_prompt': 'Все ли три пункта выполнены? Что помешало, если нет? Как партнёр реагировал на выполнение?',
            },
            {
                'day_number': 10, 'title': 'Честность, которая не ранит',
                'material': '«Честность» — не лицензия говорить всё, что думаешь, без фильтра. Это умение говорить правду с заботой. Ключевой вопрос перед честным разговором: «Мой партнёр нуждается в этой информации? Мой мотив — его благо или моё облегчение?»',
                'exercise': 'Поговорите о чём-то, о чём обычно молчите из страха реакции партнёра. Используйте структуру: «Я хочу быть честным, потому что мне важны наши отношения. Хочу сказать... Мне было бы важно, чтобы ты [услышал / не воспринял в штыки / просто знал об этом].»',
                'reflection_prompt': 'Как партнёр воспринял вашу честность? Что изменилось от того, что это было произнесено?',
            },
            {
                'day_number': 11, 'title': 'Принять ответственность',
                'material': 'Защитная реакция — один из «четырёх всадников» Готтмана. Когда нам предъявляют претензию, мы инстинктивно защищаемся или перекладываем вину. Но именно способность принять ответственность («да, в этом есть и моя роль») восстанавливает доверие быстрее всего.',
                'exercise': 'Вспомните ситуацию из последних недель, где вы были неправы или могли поступить лучше. Скажите партнёру: «В той ситуации я [что сделал]. Я понимаю, что это [как это повлияло]. Мне жаль.» Без объяснений и «но».',
                'reflection_prompt': 'Что было сложно в этом? Как почувствовал себя партнёр, услышав это?',
            },
            {
                'day_number': 12, 'title': 'Конфиденциальность',
                'material': 'Пары редко явно договариваются о том, что остаётся между ними. В результате один рассказывает маме о конфликте, другой — другу о проблемах. Это нарушение конфиденциальности подрывает доверие даже без умысла.',
                'exercise': 'Обсудите: что из вашей личной жизни остаётся только между вами? Что можно рассказывать друзьям / родителям, а что — нет? Договоритесь конкретно.',
                'reflection_prompt': 'Были ли случаи, когда граница нарушалась? Как вы к этому относитесь теперь, после разговора?',
            },
            {
                'day_number': 13, 'title': 'Великодушие интерпретации',
                'material': 'Когда доверие подорвано или мы в стрессе, мы трактуем действия партнёра в худшую сторону. «Он опоздал — ему всё равно». Великодушная интерпретация — это сознательный выбор: «Возможно, что-то случилось». Это не наивность, а мудрость.',
                'exercise': 'Вспомните 3 ситуации, где вы подумали о партнёре плохое. Перепишите каждую в «благожелательную интерпретацию». Поделитесь одной из них с партнёром.',
                'reflection_prompt': 'Как изменилось ваше ощущение ситуации при новой интерпретации?',
            },
            {
                'day_number': 14, 'title': 'Итог недели доверия',
                'material': 'Доверие — это не состояние, которое достигается однажды. Это практика последовательности, честности, принятия ответственности. Сегодня фиксируем прогресс.',
                'exercise': 'Каждый называет одно действие партнёра за эту неделю, которое укрепило доверие. Затем каждый называет одно маленькое обязательство на следующую неделю — что-то конкретное и выполнимое.',
                'reflection_prompt': 'Что изменилось в атмосфере за эту неделю? Что вы чувствуете по отношению к теме доверия?',
            },
            # --- Неделя 3: Близость и любовь ---
            {
                'day_number': 15, 'title': 'Язык любви партнёра',
                'material': 'Гэри Чепмен описал пять «языков любви»: слова поддержки, время вместе, подарки, помощь и служение, прикосновения. Мы часто любим так, как хотим получать любовь сами — но партнёр может нуждаться в другом.',
                'exercise': 'Каждый называет свой основной «язык любви» — как он хочет получать любовь. Приведите конкретные примеры: «Для меня это выглядит так...» Обменяйтесь.',
                'reflection_prompt': 'Совпадают ли ваши языки любви? Как вы можете говорить на языке партнёра чаще?',
            },
            {
                'day_number': 16, 'title': 'Ритуалы встречи и расставания',
                'material': 'Готтман называет прощание и встречу «воротами» дня. Пары, которые прощаются внимательно (не второпях) и встречаются с интересом («как прошёл день?»), имеют более высокий уровень удовлетворённости.',
                'exercise': 'Договоритесь о новом ритуале: как вы будете прощаться утром и встречаться вечером. Минимум 6-секундное объятие или поцелуй — по данным Готтмана, именно столько нужно, чтобы ритуал «сработал».',
                'reflection_prompt': 'Как ощущался новый ритуал? Что изменилось в настрое после него?',
            },
            {
                'day_number': 17, 'title': 'Общие интересы',
                'material': 'Пары, разделяющие хотя бы одно увлечение, сообщают о более высоком уровне близости. Важно не только «быть вместе», но и делать что-то вместе, что обоим интересно — не только уступая партнёру.',
                'exercise': 'Каждый называет 3-5 вещей, которые ему нравятся делать. Найдите хотя бы одну, которая интересна обоим или может стать интересной. Договоритесь попробовать это вместе на следующей неделе.',
                'reflection_prompt': 'Есть ли занятие, которое вы когда-то делали вместе и перестали? Что мешает вернуть его?',
            },
            {
                'day_number': 18, 'title': 'Комплимент глубже «ты красивый»',
                'material': 'Поверхностные комплименты («ты красивый», «ты умный») быстро обесцениваются. Комплименты о характере, поступках и усилиях — «я восхищаюсь тем, как ты справился с этой ситуацией» — воспринимаются как более искренние.',
                'exercise': 'Напишите партнёру 3 комплимента о его характере или поступках — конкретных, с примером. Не о внешности и не о навыках, а о том, каким он человеком является.',
                'reflection_prompt': 'Что из написанного партнёром вас больше всего тронуло? Почему именно это?',
            },
            {
                'day_number': 19, 'title': 'Дата — не роскошь',
                'material': 'Исследования показывают: регулярные «свидания» пар (время вдвоём без детей, гостей и работы) связаны с более высоким уровнем удовлетворённости и сексуальной активностью. Это не ретроградность — это гигиена отношений.',
                'exercise': 'Прямо сейчас договоритесь и запишите в календарь дату на ближайшие 1-2 недели. Место не имеет значения — прогулка, кафе, кино, готовка вместе дома. Главное — оба хотят, телефоны убраны.',
                'reflection_prompt': 'Когда последний раз вы были только вдвоём без отвлечений? Что мешает делать это чаще?',
            },
            {
                'day_number': 20, 'title': 'Сексуальность и близость',
                'material': 'Сексуальная близость и эмоциональная связаны, но не тождественны. Многие пары теряют физическую близость не из-за отсутствия влечения, а из-за накопленной дистанции в эмоциональном общении. И наоборот — регулярный физический контакт поддерживает эмоциональную близость.',
                'exercise': 'Поговорите (не во время близости) о том, чего каждому из вас не хватает в физическом взаимодействии — не только о сексе, но о прикосновениях, объятиях, нежности. Говорите о желаниях, а не о претензиях.',
                'reflection_prompt': 'Было ли сложно говорить об этом? Что вы услышали нового о партнёре?',
            },
            {
                'day_number': 21, 'title': 'Итог третьей недели',
                'material': 'За эту неделю вы говорили о любви, близости, языках любви, совместных занятиях и физическом контакте. Близость — это инвестиция, которая возвращается каждый день.',
                'exercise': 'Совместный ужин без гаджетов. Договоритесь об этом заранее. Во время ужина поговорите: что для вас «близость» сейчас — в этот период жизни?',
                'reflection_prompt': 'Как ощущается «близость» сейчас по сравнению с тем, как было три недели назад? Что изменилось?',
            },
            # --- Неделя 4: Семья как система ---
            {
                'day_number': 22, 'title': 'Финансовый разговор',
                'material': 'Деньги — одна из трёх главных причин разводов. Но конфликты из-за денег редко о деньгах. Они о ценностях (безопасность vs. свобода), власти (кто принимает решения) и страхах. Осознанный разговор о финансах — это разговор о ценностях.',
                'exercise': 'Каждый честно отвечает: «Что для меня означают деньги? Какое чувство я хочу иметь в отношении нашего бюджета? Что меня беспокоит?» Поделитесь. Без критики.',
                'reflection_prompt': 'Где ваши отношения с деньгами совпадают? Где различаются? Что хотите изменить в этом разговоре?',
            },
            {
                'day_number': 23, 'title': 'Распределение нагрузки',
                'material': 'Ощущение несправедливого распределения домашних обязанностей — один из главных источников обиды в паре. Исследования показывают: субъективное ощущение справедливости важнее, чем объективное равенство в часах.',
                'exercise': 'Составьте список всех задач, которые вы делаете дома. Обменяйтесь списками. Обсудите: что кажется справедливым? Что кто-то делает и не замечается? Что можно перераспределить?',
                'reflection_prompt': 'Что вас удивило в списке партнёра? Где вы чувствовали несправедливость, но не говорили об этом?',
            },
            {
                'day_number': 24, 'title': 'Управление стрессом вместе',
                'material': 'Стресс «перетекает» в отношения: если один партнёр изможден, страдает качество взаимодействия всей пары. Пара может быть «буфером стресса» — но только если оба умеют сигнализировать о своём состоянии и запрашивать нужную поддержку.',
                'exercise': 'Договоритесь о системе: как вы будете сигнализировать другому, что вы «на нулях» и что вам нужно (тишина, объятие, выслушать, помочь с делом). Придумайте простой код — слово или жест.',
                'reflection_prompt': 'Часто ли вы угадываете, что нужно партнёру, когда он в стрессе? Что мешает просить о нужном?',
            },
            {
                'day_number': 25, 'title': 'Семейные традиции',
                'material': 'Традиции создают ощущение «мы» — семейную идентичность. Исследования показывают: семьи с регулярными ритуалами оценивают качество отношений выше и лучше справляются с кризисами.',
                'exercise': 'Перечислите традиции, которые уже есть у вас. Затем каждый предлагает одну новую традицию, которую хотел бы создать. Выберите одну и договоритесь начать уже на этой неделе.',
                'reflection_prompt': 'Какая из существующих традиций вам особенно дорога? Почему?',
            },
            {
                'day_number': 26, 'title': 'Конфликт без жертв',
                'material': 'В отношениях нет победителей. Если один «выиграл» спор, а другой чувствует себя побеждённым — оба проиграли. Цель конфликта — не победить, а понять друг друга и найти решение, которое оба могут принять.',
                'exercise': 'Выберите небольшое разногласие. Используйте структуру: каждый называет свою позицию → каждый называет интерес (что за ней стоит) → ищите решение, учитывающее оба интереса.',
                'reflection_prompt': 'Как ощущалось фокусироваться на интересах, а не на позициях? Нашлось ли решение?',
            },
            {
                'day_number': 27, 'title': 'Семейные цели',
                'material': 'Пары с совместными целями имеют более высокую удовлетворённость отношениями. Важны не только индивидуальные цели, но и то, что вы хотите создать вместе — как пара, как семья.',
                'exercise': 'Каждый записывает 3 цели на следующий год: одну личную, одну для пары и одну семейную. Поделитесь и найдите совпадения. Выберите одну общую цель, над которой начнёте работать.',
                'reflection_prompt': 'Совпадает ли ваше видение «семейной цели»? Что вас вдохновляет в целях партнёра?',
            },
            {
                'day_number': 28, 'title': 'Прощение и освобождение',
                'material': 'К концу месяца у многих пар всплывают старые обиды, которые тихо хранились. Прощение — не жест слабости и не оправдание поступка. Это освобождение от груза, который тянет назад.',
                'exercise': 'Каждый думает: есть ли что-то в наших отношениях, что я несу в себе как обиду или разочарование? Назовите это партнёру — мягко, в формате «я»: «Я всё ещё несу в себе [что]». Партнёр только слушает и говорит: «Спасибо, что сказал. Мне жаль».',
                'reflection_prompt': 'Стало ли легче, когда это было произнесено? Что вы хотите сделать с этим дальше?',
            },
            {
                'day_number': 29, 'title': 'Письмо о будущем',
                'material': 'Исследования показывают: визуализация желаемого будущего повышает вероятность его достижения. Написанное слово делает намерение более конкретным и реальным.',
                'exercise': 'Каждый пишет короткое письмо партнёру из «будущего» — через 5 лет. Каким стали ваши отношения? Что изменилось? Что вы построили вместе? Прочитайте вслух.',
                'reflection_prompt': 'Что в письме партнёра вас тронуло? Где ваши «будущие» совпадают?',
            },
            {
                'day_number': 30, 'title': '30 дней: семья, которую мы создаём',
                'material': 'Тридцать дней маленьких практик. Отношения — это не то, что происходит с вами. Это то, что вы создаёте каждый день: через внимание, честность, благодарность, усилие и выбор быть рядом.',
                'exercise': 'Создайте вместе «Семейный договор»: 5-7 конкретных принципов, по которым хотите жить как пара. Не абстрактных («любить друг друга»), а конкретных: «раз в неделю — ужин без телефонов», «говорю о своих чувствах, а не обвиняю», «каждый день — одно «спасибо»». Подпишите оба.',
                'reflection_prompt': 'Что изменилось за этот месяц? Какая практика была самой важной? Что вы хотите сказать друг другу в конце этого пути?',
            },
        ],
    },
]

MICRO_PRACTICES = [
    {
        'title': 'Момент полного внимания',
        'instruction': 'Выберите 5 минут сегодня, когда вы даёте партнёру полное внимание: никаких телефонов, задач, мыслей о работе. Просто смотрите на него, слушайте, присутствуйте.',
        'category': 'communication',
        'duration_minutes': 5,
        'order_index': 1,
        'i18n': {
            'en': {'title': 'Moment of full attention', 'instruction': 'Choose 5 minutes today to give your partner your full attention: no phones, no tasks, no thoughts about work. Just look at them, listen, be present.'},
            'uz': {'title': "To'liq diqqat lahzasi", 'instruction': "Bugun turmush o'rtoqingizga to'liq e'tibor beradigan 5 daqiqani tanlang: telefonlar yo'q, vazifalar yo'q, ish haqida o'ylar yo'q. Shunchaki unga qarang, eshiting, hozir bo'ling."},
            'uz_cyrl': {'title': 'Тўлиқ диққат лаҳзаси', 'instruction': 'Бугун турмуш ўртоғингизга тўлиқ эътибор берадиган 5 дақиқани танланг: телефонлар йўқ, вазифалар йўқ, иш ҳақида ўйлар йўқ. Шунчаки унга қаранг, эшитинг, ҳозир бўлинг.'},
        },
    },
    {
        'title': 'Конкретное «спасибо»',
        'instruction': 'Скажите партнёру спасибо за одно конкретное действие. Не «ты такой заботливый», а «спасибо, что вчера приготовил ужин — я была так устала».',
        'category': 'communication',
        'duration_minutes': 3,
        'order_index': 2,
        'i18n': {
            'en': {'title': 'Specific "thank you"', 'instruction': 'Thank your partner for one specific action. Not "you\'re so caring," but "thank you for cooking dinner yesterday — I was so tired."'},
            'uz': {'title': 'Aniq "rahmat"', 'instruction': "Turmush o'rtoqingizga bitta aniq harakat uchun rahmat ayting. «Siz juda g'amxo'rsiz» emas, balki «kecha kechki ovqat pishirganingiz uchun rahmat — men juda charchaganman»"},
            'uz_cyrl': {'title': 'Аниқ "раҳмат"', 'instruction': 'Турмуш ўртоғингизга битта аниқ ҳаракат учун раҳмат айтинг. «Сиз жуда ғамхўрсиз» эмас, балки «кеча кечки овқат пиширганингиз учун раҳмат — мен жуда чарчаганман»'},
        },
    },
    {
        'title': 'Открытый вопрос',
        'instruction': 'Задайте партнёру один открытый вопрос о его внутреннем мире: «Что тебя сейчас больше всего занимает?», «Как ты себя чувствуешь?», «О чём ты думал сегодня?»',
        'category': 'intimacy',
        'duration_minutes': 5,
        'order_index': 3,
        'i18n': {
            'en': {'title': 'Open-ended question', 'instruction': 'Ask your partner one open-ended question about their inner world: "What\'s on your mind most right now?", "How are you feeling?", "What were you thinking about today?"'},
            'uz': {'title': 'Ochiq savol', 'instruction': "Turmush o'rtoqingizga ichki dunyosi haqida bitta ochiq savol bering: «Hozir sizni eng ko'p nima band qilmoqda?», «O'zingizni qanday his qilyapsiz?», «Bugun nima haqida o'yladingiz?»"},
            'uz_cyrl': {'title': 'Очиқ савол', 'instruction': 'Турмуш ўртоғингизга ички дунёси ҳақида битта очиқ савол беринг: «Ҳозир сизни энг кўп нима банд қилмоқда?», «Ўзингизни қандай ҳис қиляпсиз?», «Бугун нима ҳақида ўйладингиз?»'},
        },
    },
    {
        'title': 'Приятное воспоминание',
        'instruction': 'Вспомните вместе с партнёром одно хорошее совместное воспоминание. Расскажите, что вам в нём особенно дорого.',
        'category': 'love',
        'duration_minutes': 5,
        'order_index': 4,
        'i18n': {
            'en': {'title': 'A fond memory', 'instruction': 'Recall a good shared memory together with your partner. Share what is especially dear to you about it.'},
            'uz': {'title': 'Yoqimli xotira', 'instruction': "Turmush o'rtoqingiz bilan birgalikda bitta yaxshi umumiy xotirani eslang. Unda sizga ayniqsa qadrli narsani aytib bering."},
            'uz_cyrl': {'title': 'Ёқимли хотира', 'instruction': 'Турмуш ўртоғингиз билан биргаликда битта яхши умумий хотирани эсланг. Унда сизга айниқса қадрли нарсани айтиб беринг.'},
        },
    },
    {
        'title': 'Один позитивный факт',
        'instruction': 'Назовите одну вещь, которая вам нравится в партнёре прямо сейчас — в этот момент, сегодня. Это может быть что-то маленькое.',
        'category': 'love',
        'duration_minutes': 3,
        'order_index': 5,
        'i18n': {
            'en': {'title': 'One positive thing', 'instruction': 'Name one thing you like about your partner right now — in this moment, today. It can be something small.'},
            'uz': {'title': 'Bitta ijobiy fakt', 'instruction': "Hozir — shu lahzada, bugun — turmush o'rtoqingizda yoqtirgan bitta narsani ayting. Bu kichik narsa bo'lishi mumkin."},
            'uz_cyrl': {'title': 'Битта ижобий факт', 'instruction': 'Ҳозир — шу лаҳзада, бугун — турмуш ўртоғингизда ёқтирган битта нарсани айтинг. Бу кичик нарса бўлиши мумкин.'},
        },
    },
    {
        'title': 'Разгрузка дня',
        'instruction': 'Дайте партнёру 5 минут рассказать о своём дне без советов и оценок. Только слушайте. Потом поменяйтесь.',
        'category': 'communication',
        'duration_minutes': 10,
        'order_index': 6,
        'i18n': {
            'en': {'title': 'Day unload', 'instruction': 'Give your partner 5 minutes to talk about their day without advice or judgment. Just listen. Then switch.'},
            'uz': {'title': 'Kunni bo\'shashtirish', 'instruction': "Turmush o'rtoqingizga maslahat va baholarsiz kuni haqida 5 daqiqa gapirish imkonini bering. Shunchaki eshiting. Keyin almashing."},
            'uz_cyrl': {'title': 'Кунни бўшаштириш', 'instruction': 'Турмуш ўртоғингизга маслаҳат ва баҳоларсиз куни ҳақида 5 дақиқа гапириш имконини беринг. Шунчаки эшитинг. Кейин алмашинг.'},
        },
    },
    {
        'title': 'Объятие 20 секунд',
        'instruction': 'Обнимитесь с партнёром и держите объятие не менее 20 секунд. По данным NIH, это время необходимо для выделения окситоцина.',
        'category': 'intimacy',
        'duration_minutes': 1,
        'order_index': 7,
        'i18n': {
            'en': {'title': '20-second hug', 'instruction': 'Hug your partner and hold the hug for at least 20 seconds. According to NIH research, this is the time needed for oxytocin to be released.'},
            'uz': {'title': '20 soniyalik quchoq', 'instruction': "Turmush o'rtoqingizni quchoqlang va kamida 20 soniya ushlab turing. NIH ma'lumotlariga ko'ra, bu oksitotsin ishlab chiqarish uchun zarur vaqt."},
            'uz_cyrl': {'title': '20 сониялик қучоқ', 'instruction': 'Турмуш ўртоғингизни қучоқланг ва камида 20 сония ушлаб туринг. NIH маълумотларига кўра, бу окситотсин ишлаб чиқариш учун зарур вақт.'},
        },
    },
    {
        'title': 'Один план на выходные',
        'instruction': 'Договоритесь об одном совместном занятии на ближайшие выходные — не обязательно большом. Главное: оба хотят этого делать.',
        'category': 'traditions',
        'duration_minutes': 5,
        'order_index': 8,
        'i18n': {
            'en': {'title': 'One weekend plan', 'instruction': 'Agree on one activity to do together this coming weekend — it does not have to be big. The key: both of you want to do it.'},
            'uz': {'title': 'Dam olish kunlari uchun bir reja', 'instruction': "Yaqin dam olish kunlaridagi bitta umumiy mashg'ulotni kelishib oling — katta bo'lishi shart emas. Muhimi: ikkalangiz ham buni qilishni xohlaysiz."},
            'uz_cyrl': {'title': 'Дам олиш кунлари учун бир режа', 'instruction': 'Яқин дам олиш кунларидаги битта умумий машғулотни келишиб олинг — катта бўлиши шарт эмас. Муҳими: иккалангиз ҳам буни қилишни хоҳлайсиз.'},
        },
    },
    {
        'title': 'Признание чувства',
        'instruction': 'Найдите момент и скажите партнёру о чувстве, которое вы сейчас испытываете. Не мнение, не жалобу — именно чувство. «Я сейчас устал и мне нужна тишина» или «Мне сегодня тревожно».',
        'category': 'intimacy',
        'duration_minutes': 3,
        'order_index': 9,
        'i18n': {
            'en': {'title': 'Naming a feeling', 'instruction': 'Find a moment and tell your partner about the feeling you are experiencing right now. Not an opinion, not a complaint — a feeling. "I am tired right now and need some quiet" or "I feel anxious today."'},
            'uz': {'title': 'Hissiyotni tan olish', 'instruction': "Bir lahza toping va turmush o'rtoqingizga hozir his qilayotgan tuyg'uingiz haqida ayting. Fikr emas, shikoyat emas — aynan his. «Hozir charchadim va jimlik kerak» yoki «Bugun xavotirdaman»."},
            'uz_cyrl': {'title': 'Ҳиссиётни тан олиш', 'instruction': 'Бир лаҳза топинг ва турмуш ўртоғингизга ҳозир ҳис қилаётган туйғуингиз ҳақида айтинг. Фикр эмас, шикоят эмас — айнан ҳис. «Ҳозир чарчадим ва жимлик керак» ёки «Бугун хавотирдаман».'},
        },
    },
    {
        'title': 'Вопрос о мечте',
        'instruction': 'Спросите партнёра: «Есть ли что-то, что ты очень хочешь сделать или попробовать, но пока не решился?» Выслушайте без оценки.',
        'category': 'intimacy',
        'duration_minutes': 5,
        'order_index': 10,
        'i18n': {
            'en': {'title': 'Dream question', 'instruction': 'Ask your partner: "Is there something you really want to do or try, but haven\'t dared yet?" Listen without judgment.'},
            'uz': {'title': 'Orzu haqida savol', 'instruction': "Turmush o'rtoqingizdan so'rang: «Siz juda qilishni yoki sinab ko'rishni xohlagan, lekin hali jur'at eta olmagan biror narsa bormi?» Baholarsiz tinglang."},
            'uz_cyrl': {'title': 'Орзу ҳақида савол', 'instruction': 'Турмуш ўртоғингиздан сўранг: «Сиз жуда қилишни ёки синаб кўришни хоҳлаган, лекин ҳали жур\'ат эта олмаган бирор нарса борми?» Баҳоларсиз тинглинг.'},
        },
    },
]

ACHIEVEMENTS = [
    {'key': 'first_article', 'title': 'Первый шаг', 'description': 'Прочитали первую статью', 'icon': '📖', 'condition_type': 'articles_count', 'condition_value': 1},
    {'key': 'five_articles', 'title': 'Читатель', 'description': 'Прочитали 5 статей', 'icon': '📚', 'condition_type': 'articles_count', 'condition_value': 5},
    {'key': 'ten_articles', 'title': 'Знаток', 'description': 'Прочитали 10 статей', 'icon': '🎓', 'condition_type': 'articles_count', 'condition_value': 10},
    {'key': 'first_training', 'title': 'Практик', 'description': 'Завершили первую тренировку', 'icon': '💪', 'condition_type': 'trainings_count', 'condition_value': 1},
    {'key': 'all_trainings', 'title': 'Мастер навыков', 'description': 'Завершили все тренировки', 'icon': '🏆', 'condition_type': 'trainings_count', 'condition_value': 7},
    {'key': 'first_program', 'title': 'Студент', 'description': 'Завершили первую программу', 'icon': '🎯', 'condition_type': 'programs_count', 'condition_value': 1},
    {'key': 'three_programs', 'title': 'Выпускник', 'description': 'Завершили 3 программы', 'icon': '🌟', 'condition_type': 'programs_count', 'condition_value': 3},
    {'key': 'streak_3', 'title': 'На разгоне', 'description': '3 дня подряд выполняете практики', 'icon': '🔥', 'condition_type': 'streak_days', 'condition_value': 3},
    {'key': 'streak_7', 'title': 'Неделя роста', 'description': '7 дней подряд', 'icon': '✨', 'condition_type': 'streak_days', 'condition_value': 7},
    {'key': 'streak_30', 'title': 'Месяц практики', 'description': '30 дней подряд', 'icon': '🌈', 'condition_type': 'streak_days', 'condition_value': 30},
]


class Command(BaseCommand):
    help = 'Заполняет базу данных начальным контентом Семейной Академии'

    def handle(self, *args, **options):
        self.stdout.write('Создаём источники...')
        source_map = {}
        for s in SOURCES:
            obj, _ = ArticleSource.objects.update_or_create(name=s['name'], defaults=s)
            source_map[s['name']] = obj
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(SOURCES)} источников'))

        self.stdout.write('Создаём статьи...')
        for a in ARTICLES:
            source_names = a.pop('sources', [])
            obj, _ = Article.objects.update_or_create(slug=a['slug'], defaults=a)
            obj.sources.set([source_map[n] for n in source_names if n in source_map])
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(ARTICLES)} статей'))

        self.stdout.write('Создаём тренировки...')
        for t in TRAININGS:
            Training.objects.update_or_create(slug=t['slug'], defaults=t)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(TRAININGS)} тренировок'))

        self.stdout.write('Создаём программы...')
        for p in PROGRAMS:
            days_data = p.pop('days', [])
            program, _ = Program.objects.update_or_create(slug=p['slug'], defaults=p)
            for d in days_data:
                ProgramDay.objects.update_or_create(
                    program=program, day_number=d['day_number'], defaults=d
                )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(PROGRAMS)} программ'))

        self.stdout.write('Создаём микро-практики...')
        for mp in MICRO_PRACTICES:
            AcademyMicroPractice.objects.update_or_create(title=mp['title'], defaults=mp)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(MICRO_PRACTICES)} практик'))

        self.stdout.write('Создаём достижения...')
        for ach in ACHIEVEMENTS:
            Achievement.objects.update_or_create(key=ach['key'], defaults=ach)
        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(ACHIEVEMENTS)} достижений'))

        self.stdout.write(self.style.SUCCESS('\n✅ Семейная Академия наполнена контентом!'))
