from django.db import migrations, models

_FIELDS = [
    'strengths_summary',
    'growth_summary',
    'attention_summary',
    'ai_analysis',
    'recommendation',
    'next_focus',
]

_FWD = '\n'.join(
    f"""
    ALTER TABLE analytics_insights
    ALTER COLUMN {f} TYPE jsonb
    USING CASE
        WHEN {f} IS NULL OR {f} = ''
            THEN '{{}}'::jsonb
        ELSE jsonb_build_object('ru', {f}, 'en', '', 'uz', '')
    END;
    """
    for f in _FIELDS
)

_REV = '\n'.join(
    f"""
    ALTER TABLE analytics_insights
    ALTER COLUMN {f} TYPE text
    USING COALESCE({f}->>'ru', '');
    """
    for f in _FIELDS
)


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0007_analyticsinsight'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[
                migrations.RunSQL(sql=_FWD, reverse_sql=_REV),
            ],
            state_operations=[
                migrations.AlterField(
                    model_name='analyticsinsight',
                    name=f,
                    field=models.JSONField(default=dict),
                )
                for f in _FIELDS
            ],
        ),
    ]
