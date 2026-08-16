from collections import Counter

from django.conf import settings
from django.core.management.base import BaseCommand

from apps.components.image_normalize import normalized_url
from apps.components.models import Components


class Command(BaseCommand):
    help = "Normalize component images onto a uniform canvas and rehost them on S3."

    def add_arguments(self, parser):
        parser.add_argument("--type", help="Only process one component_type")
        parser.add_argument("--limit", type=int, help="Stop after this many uploads")
        parser.add_argument("--dry-run", action="store_true")

    def handle(self, *args, **options):
        host = f"{settings.AWS_STORAGE_BUCKET_NAME}.s3."
        queryset = Components.objects.exclude(image_url="").order_by("component_type", "id")
        if options["type"]:
            queryset = queryset.filter(component_type=options["type"])

        tally = Counter()
        uploaded = 0
        for component in queryset:
            if host in component.image_url:
                tally["skipped"] += 1
                continue
            if options["limit"] and uploaded >= options["limit"]:
                tally["remaining"] += 1
                continue
            if options["dry_run"]:
                tally[component.component_type] += 1
                uploaded += 1
                continue
            try:
                url = normalized_url(component.image_url, component.component_type)
            except Exception as exc:
                tally["failed"] += 1
                self.stderr.write(f"  {type(exc).__name__}: {component.image_url}")
                continue
            Components.objects.filter(pk=component.pk).update(image_url=url)
            tally[component.component_type] += 1
            uploaded += 1

        for key in sorted(tally):
            self.stdout.write(f"  {key:16} {tally[key]}")
