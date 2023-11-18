from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from datetime import timedelta


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rambutan.settings')

app = Celery('rambutan')
app.conf.enable_utc = False
app.config_from_object(settings, namespace='CELERY')
app.autodiscover_tasks()

# Celery beat Settings:

# TODO: Schedule beat for adding generated resources
app.conf.beat_schedule = {
    "update_silos_with_mine_production every second": {
        "task": "game_engine.background.tasks.update_silos_with_mine_production",
        "schedule": timedelta(seconds=10)

    }
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request:{self.request!r}')

