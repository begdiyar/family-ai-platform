import uuid
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleSource',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=200)),
                ('source_type', models.CharField(choices=[('researcher', 'Исследователь'), ('organization', 'Организация'), ('book', 'Книга'), ('journal', 'Журнал')], max_length=20)),
                ('trust_level', models.CharField(choices=[('high', 'Высокий'), ('medium', 'Средний')], default='high', max_length=10)),
                ('url', models.URLField(blank=True, null=True)),
            ],
            options={'db_table': 'academy_sources', 'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('category', models.CharField(choices=[('communication', 'Общение в семье'), ('trust', 'Доверие'), ('conflict', 'Управление конфликтами'), ('intimacy', 'Эмоциональная близость'), ('love', 'Любовь и уважение'), ('finance', 'Финансы в семье'), ('husband_role', 'Роль мужа'), ('wife_role', 'Роль жены'), ('relatives', 'Отношения с родственниками'), ('parenting', 'Воспитание детей'), ('traditions', 'Семейные традиции'), ('stress', 'Стресс и выгорание'), ('marriage_prep', 'Подготовка к браку'), ('crisis_recovery', 'Восстановление после кризиса')], max_length=30)),
                ('title', models.CharField(max_length=300)),
                ('brief', models.TextField()),
                ('body', models.TextField()),
                ('read_time_minutes', models.PositiveSmallIntegerField(default=5)),
                ('difficulty', models.CharField(choices=[('beginner', 'Начальный'), ('intermediate', 'Средний'), ('advanced', 'Продвинутый')], default='beginner', max_length=20)),
                ('tags', models.JSONField(default=list)),
                ('sources', models.ManyToManyField(blank=True, related_name='articles', to='academy.articlesource')),
                ('is_published', models.BooleanField(default=True)),
                ('order_index', models.SmallIntegerField(default=0)),
            ],
            options={'db_table': 'academy_articles', 'ordering': ['category', 'order_index']},
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['category', 'is_published'], name='academy_art_cat_pub_idx'),
        ),
        migrations.AddIndex(
            model_name='article',
            index=models.Index(fields=['slug'], name='academy_art_slug_idx'),
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('skill_type', models.CharField(choices=[('active_listening', 'Активное слушание'), ('emotion_management', 'Управление эмоциями'), ('gratitude', 'Навык благодарности'), ('partner_support', 'Поддержка партнёра'), ('constructive_dialogue', 'Конструктивный диалог'), ('conflict_resolution', 'Решение конфликтов'), ('joint_planning', 'Совместное планирование')], max_length=30)),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('theory', models.TextField()),
                ('exercise_instruction', models.TextField()),
                ('completion_check', models.TextField()),
                ('duration_minutes', models.PositiveSmallIntegerField(default=10)),
                ('difficulty', models.CharField(choices=[('beginner', 'Начальный'), ('intermediate', 'Средний'), ('advanced', 'Продвинутый')], default='beginner', max_length=20)),
                ('order_index', models.SmallIntegerField(default=0)),
            ],
            options={'db_table': 'academy_trainings', 'ordering': ['order_index']},
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField()),
                ('duration_days', models.PositiveSmallIntegerField()),
                ('category_focus', models.CharField(max_length=50)),
                ('cover_gradient', models.CharField(default='linear-gradient(135deg, #6558A8, #4A88B8)', max_length=200)),
                ('order_index', models.SmallIntegerField(default=0)),
            ],
            options={'db_table': 'academy_programs', 'ordering': ['order_index']},
        ),
        migrations.CreateModel(
            name='ProgramDay',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='days', to='academy.program')),
                ('day_number', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=300)),
                ('material', models.TextField()),
                ('exercise', models.TextField()),
                ('reflection_prompt', models.TextField()),
            ],
            options={'db_table': 'academy_program_days', 'ordering': ['day_number']},
        ),
        migrations.AlterUniqueTogether(
            name='programday',
            unique_together={('program', 'day_number')},
        ),
        migrations.CreateModel(
            name='AcademyMicroPractice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=300)),
                ('instruction', models.TextField()),
                ('category', models.CharField(choices=[('communication', 'Общение в семье'), ('trust', 'Доверие'), ('conflict', 'Управление конфликтами'), ('intimacy', 'Эмоциональная близость'), ('love', 'Любовь и уважение'), ('finance', 'Финансы в семье'), ('husband_role', 'Роль мужа'), ('wife_role', 'Роль жены'), ('relatives', 'Отношения с родственниками'), ('parenting', 'Воспитание детей'), ('traditions', 'Семейные традиции'), ('stress', 'Стресс и выгорание'), ('marriage_prep', 'Подготовка к браку'), ('crisis_recovery', 'Восстановление после кризиса')], max_length=30)),
                ('duration_minutes', models.PositiveSmallIntegerField(default=5)),
                ('is_active', models.BooleanField(default=True)),
                ('order_index', models.SmallIntegerField(default=0)),
            ],
            options={'db_table': 'academy_micro_practices', 'ordering': ['order_index']},
        ),
        migrations.CreateModel(
            name='UserArticleProgress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_progress', to=settings.AUTH_USER_MODEL)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_progress', to='academy.article')),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'academy_user_article_progress'},
        ),
        migrations.AlterUniqueTogether(
            name='userarticleprogress',
            unique_together={('user', 'article')},
        ),
        migrations.AddIndex(
            model_name='userarticleprogress',
            index=models.Index(fields=['user'], name='academy_uap_user_idx'),
        ),
        migrations.CreateModel(
            name='UserTrainingProgress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_progress', to=settings.AUTH_USER_MODEL)),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_progress', to='academy.training')),
                ('status', models.CharField(choices=[('started', 'Начата'), ('completed', 'Завершена')], default='started', max_length=20)),
                ('reflection_note', models.TextField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={'db_table': 'academy_user_training_progress'},
        ),
        migrations.AlterUniqueTogether(
            name='usertrainingprogress',
            unique_together={('user', 'training')},
        ),
        migrations.AddIndex(
            model_name='usertrainingprogress',
            index=models.Index(fields=['user'], name='academy_utp_user_idx'),
        ),
        migrations.CreateModel(
            name='UserProgramEnrollment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='program_enrollments', to=settings.AUTH_USER_MODEL)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enrollments', to='academy.program')),
                ('current_day', models.PositiveSmallIntegerField(default=1)),
                ('status', models.CharField(choices=[('active', 'Активна'), ('completed', 'Завершена'), ('paused', 'Пауза')], default='active', max_length=20)),
                ('enrolled_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'academy_user_program_enrollments'},
        ),
        migrations.AlterUniqueTogether(
            name='userprogramenrollment',
            unique_together={('user', 'program')},
        ),
        migrations.AddIndex(
            model_name='userprogramenrollment',
            index=models.Index(fields=['user', 'status'], name='academy_upe_user_status_idx'),
        ),
        migrations.CreateModel(
            name='UserProgramDayProgress',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('enrollment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='day_progress', to='academy.userprogramenrollment')),
                ('day', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academy.programday')),
                ('reflection', models.TextField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'academy_user_program_day_progress'},
        ),
        migrations.AlterUniqueTogether(
            name='userprogramdayprogress',
            unique_together={('enrollment', 'day')},
        ),
        migrations.AddIndex(
            model_name='userprogramdayprogress',
            index=models.Index(fields=['enrollment'], name='academy_updp_enrollment_idx'),
        ),
        migrations.CreateModel(
            name='UserMicroPracticeLog',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='micro_practice_logs', to=settings.AUTH_USER_MODEL)),
                ('practice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academy.academymicropractice')),
                ('date', models.DateField()),
                ('completed_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'academy_user_micro_practice_logs'},
        ),
        migrations.AlterUniqueTogether(
            name='usermicropracticelog',
            unique_together={('user', 'date')},
        ),
        migrations.AddIndex(
            model_name='usermicropracticelog',
            index=models.Index(fields=['user', 'date'], name='academy_umpl_user_date_idx'),
        ),
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('key', models.CharField(max_length=100, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('icon', models.CharField(max_length=10)),
                ('condition_type', models.CharField(choices=[('articles_count', 'Количество статей'), ('trainings_count', 'Количество тренировок'), ('programs_count', 'Количество программ'), ('streak_days', 'Серия дней')], max_length=50)),
                ('condition_value', models.IntegerField()),
            ],
            options={'db_table': 'academy_achievements', 'ordering': ['condition_type', 'condition_value']},
        ),
        migrations.CreateModel(
            name='UserAchievement',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to=settings.AUTH_USER_MODEL)),
                ('achievement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_achievements', to='academy.achievement')),
                ('earned_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'db_table': 'academy_user_achievements'},
        ),
        migrations.AlterUniqueTogether(
            name='userachievement',
            unique_together={('user', 'achievement')},
        ),
        migrations.AddIndex(
            model_name='userachievement',
            index=models.Index(fields=['user'], name='academy_ua_user_idx'),
        ),
    ]
