"""
Sync i18n translations for existing practices from _practice_data.py.
No API calls needed — translations are already in the data file.

Usage:
    python manage.py translate_practices
"""
from django.core.management.base import BaseCommand
from apps.practices.models import Practice
from ._practice_data import PRACTICES


class Command(BaseCommand):
    help = 'Sync i18n translations from seed data into existing Practice records.'

    def handle(self, *args, **options):
        updated = 0
        skipped = 0
        not_found = 0

        for item in PRACTICES:
            i18n = item.get('i18n', {})
            if not i18n:
                skipped += 1
                continue

            # Remove uz_cyrl — not used
            i18n.pop('uz_cyrl', None)

            try:
                practice = Practice.objects.get(
                    title=item['title'],
                    slot_type=item['slot_type'],
                )
                practice.i18n = i18n
                practice.save(update_fields=['i18n'])
                updated += 1
            except Practice.DoesNotExist:
                not_found += 1

        self.stdout.write(self.style.SUCCESS(
            f'Done. Updated: {updated} | Skipped (no i18n): {skipped} | Not found in DB: {not_found}'
        ))
