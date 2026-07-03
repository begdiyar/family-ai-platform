"""
Management command: seed the practices library.

Usage:
    python manage.py seed_practices           # add only new records
    python manage.py seed_practices --clear   # wipe existing first
"""
from django.core.management.base import BaseCommand
from apps.practices.models import Practice
from ._practice_data import PRACTICES   # data module (same directory)


class Command(BaseCommand):
    help = 'Seed the practices library with initial content.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Delete all existing practices before seeding.',
        )

    def handle(self, *args, **options):
        if options['clear']:
            deleted, _ = Practice.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'Deleted {deleted} practices.'))

        created = 0
        skipped = 0

        for item in PRACTICES:
            _, was_created = Practice.objects.get_or_create(
                title=item['title'],
                slot_type=item['slot_type'],
                defaults={
                    'description':      item.get('description', ''),
                    'instructions':     item.get('instructions', ''),
                    'category':         item['category'],
                    'difficulty':       item.get('difficulty', 'easy'),
                    'duration_minutes': item.get('duration_minutes', 10),
                    'is_active':        True,
                    'i18n':             item.get('i18n', {}),
                    'tags':             item.get('tags', []),
                },
            )
            if was_created:
                created += 1
            else:
                skipped += 1

        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Created: {created}  |  Skipped (already exist): {skipped}'
        ))
        self._print_stats()

    def _print_stats(self):
        from django.db.models import Count
        self.stdout.write('\nDistribution by slot_type:')
        for row in Practice.objects.values('slot_type').annotate(n=Count('id')).order_by('slot_type'):
            self.stdout.write(f"  {row['slot_type']:15s} {row['n']:>4}")

        self.stdout.write('\nDistribution by category:')
        for row in Practice.objects.values('category').annotate(n=Count('id')).order_by('category'):
            self.stdout.write(f"  {row['category']:15s} {row['n']:>4}")

        total = Practice.objects.count()
        self.stdout.write(f'\nTotal practices in DB: {total}\n')
