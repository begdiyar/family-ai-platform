import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_last_name_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='gender',
            field=models.CharField(
                blank=True, default='',
                choices=[
                    ('male', 'Мужчина'), ('female', 'Женщина'),
                    ('other', 'Другое'), ('prefer_not_to_say', 'Предпочитаю не указывать'),
                ],
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='user',
            name='native_language',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='user',
            name='occupation',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='education_level',
            field=models.CharField(
                blank=True, default='',
                choices=[
                    ('secondary', 'Среднее'), ('vocational', 'Среднее специальное'),
                    ('incomplete_higher', 'Неполное высшее'), ('higher', 'Высшее'),
                    ('postgraduate', 'Учёная степень'),
                ],
                max_length=30,
            ),
        ),
        migrations.CreateModel(
            name='CommunicationPreference',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('conflict_style', models.CharField(
                    blank=True, default='',
                    choices=[
                        ('avoidant', 'Избегающий'), ('confrontational', 'Конфронтационный'),
                        ('collaborative', 'Совместное решение'), ('competitive', 'Соревновательный'),
                        ('compromising', 'Компромисс'),
                    ],
                    max_length=30,
                )),
                ('support_style', models.CharField(
                    blank=True, default='',
                    choices=[
                        ('advice', 'Советы и решения'), ('empathy', 'Сочувствие и понимание'),
                        ('practical', 'Практическая помощь'), ('space', 'Пространство для осмысления'),
                    ],
                    max_length=30,
                )),
                ('user', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='communication_pref',
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={'db_table': 'communication_preferences'},
        ),
    ]
