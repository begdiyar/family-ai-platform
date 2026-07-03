from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academy', '0004_rename_academy_art_cat_pub_idx_academy_art_categor_e9fe7e_idx_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='i18n',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
