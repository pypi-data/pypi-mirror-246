import datetime

from django.conf import settings
from django.core.management import BaseCommand
from django.utils.timezone import now

from model_hooks.models import HookLog


class Command(BaseCommand):
    """Prune old log records."""

    def handle(self, *args, **options):
        offset = now() - datetime.timedelta(days=getattr(settings, 'HOOK_LOG_RETENTION_DAYS', 7))
        HookLog.objects.filter(created__lt=offset).delete()
