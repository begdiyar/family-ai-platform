import uuid
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0006_zonescore_zone_finance_relatives'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnalyticsInsight',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('analytics_result', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='insight',
                    to='analytics.analyticsresult',
                )),
                ('strengths_summary', models.TextField(blank=True, default='')),
                ('growth_summary', models.TextField(blank=True, default='')),
                ('attention_summary', models.TextField(blank=True, default='')),
                ('ai_analysis', models.TextField(blank=True, default='')),
                ('recommendation', models.TextField(blank=True, default='')),
                ('next_focus', models.TextField(blank=True, default='')),
            ],
            options={'db_table': 'analytics_insights'},
        ),
    ]
