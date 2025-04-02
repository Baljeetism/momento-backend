from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.conf import settings
from django_apscheduler import util
import logging
from django.utils import timezone
import pytz  # Make sure to install pytz if not already present

logger = logging.getLogger(__name__)

def start_scheduler():
    # Get the timezone from Django settings
    try:
        tz = pytz.timezone(settings.TIME_ZONE)
    except pytz.UnknownTimeZoneError:
        logger.error(f"❌ Unknown timezone: {settings.TIME_ZONE}. Falling back to UTC.")
        tz = pytz.UTC
    
    # Initialize scheduler with the timezone
    scheduler = BackgroundScheduler(timezone=tz)
    scheduler.add_jobstore(DjangoJobStore(), "default")
    
    # Import inside function to avoid circular imports
    from events.tasks import check_and_send_reminders
    
    # Add jobs with explicit timezone
    scheduler.add_job(
        check_and_send_reminders,
        'interval',
        minutes=1,
        id='event_reminders',
        replace_existing=True,
        max_instances=1,
        timezone=tz  # Use the timezone object directly
    )
    
    scheduler.add_job(
        delete_old_job_executions,
        'interval',
        days=1,
        id='delete_old_job_executions',
        replace_existing=True,
        timezone=tz
    )
    
    try:
        scheduler.start()
        logger.info(f"✅ Scheduler started successfully in {tz.zone} timezone")
        logger.info(f"Current time: {timezone.localtime(timezone.now())}")
    except Exception as e:
        logger.error(f"❌ Scheduler startup failed: {e}")
        raise

@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)