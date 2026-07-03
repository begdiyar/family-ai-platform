from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0005_achievement_i18n'),
        ('practices', '0009_alter_assignmentslot_slot_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='practice',
            name='academy_article',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='linked_practices',
                to='academy.article',
            ),
        ),
    ]
