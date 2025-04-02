from django.apps import AppConfig
import os
import logging

logger = logging.getLogger(__name__)

class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'events'
    scheduler_started = False

    def ready(self):
        if not self.scheduler_started and os.environ.get('RUN_MAIN'):
            try:
                from .scheduler import start_scheduler
                start_scheduler()
                EventsConfig.scheduler_started = True
                logger.info("Event reminders scheduler initialized")
            except Exception as e:
                logger.error(f"Failed to start scheduler: {e}")