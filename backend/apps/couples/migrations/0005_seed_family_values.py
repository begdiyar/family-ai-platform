from django.db import migrations

FAMILY_VALUES = [
    ('respect',             'Уважение'),
    ('trust',               'Доверие'),
    ('love',                'Любовь'),
    ('children',            'Дети'),
    ('education',           'Образование'),
    ('financial_stability', 'Финансовая стабильность'),
    ('career',              'Карьера'),
    ('faith',               'Вера'),
    ('traditions',          'Традиции'),
    ('travel',              'Путешествия'),
    ('self_development',    'Саморазвитие'),
    ('health',              'Здоровье'),
]


def seed_values(apps, schema_editor):
    FamilyValue = apps.get_model('couples', 'FamilyValue')
    for slug, label_ru in FAMILY_VALUES:
        FamilyValue.objects.get_or_create(slug=slug, defaults={'label_ru': label_ru})


def remove_values(apps, schema_editor):
    FamilyValue = apps.get_model('couples', 'FamilyValue')
    FamilyValue.objects.filter(slug__in=[s for s, _ in FAMILY_VALUES]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('couples', '0004_extended_couple_profile'),
    ]

    operations = [
        migrations.RunPython(seed_values, remove_values),
    ]
