from django.utils import timezone
from datetime import datetime
import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import smtplib


logger = logging.getLogger(__name__)

def check_and_send_reminders():
    """Main function to be called by the scheduler"""
    logger.info("Running event reminder check...")
    try:
        from events.models import Events
        from rsvp.models import RSVP
        
        now = timezone.localtime()
        events = Events.objects.all()
        
        for event in events:
            process_event_reminders(event, now)
    except Exception as e:
        logger.error(f"Error in reminder check: {e}")

def process_event_reminders(event, current_time):
    """Process reminders for a single event"""
    try:
        event_datetime = timezone.make_aware(
            datetime.combine(event.date, event.time),
            timezone=timezone.get_current_timezone()  
        )
        time_until = (event_datetime - current_time).total_seconds() / 60
        
        if 715 < time_until <= 720:
            send_event_reminders(event)
    except Exception as e:
        logger.error(f"Error processing event {event.id}: {e}")

def send_event_reminders(event):
    """Send reminders for a specific event"""
    from rsvp.models import RSVP
    
    try:
        rsvps = RSVP.objects.filter(event=event, status__in=["Attending", "Maybe"]).select_related('user')
        if not rsvps.exists():
            logger.info(f"No RSVPs found for event {event.id}")
            return
            
        for rsvp in rsvps:
            try:
                send_reminder_email(event, rsvp.user.email)
                logger.info(f"Sent reminder for event {event.id} to {rsvp.user.email}")
            except Exception as e:
                logger.error(f"Failed to send to {rsvp.user.email}: {e}")
    except Exception as e:
        logger.error(f"Error retrieving RSVPs for event {event.id}: {e}")

def send_reminder_email(event, recipient_email):
    try:
        # Render HTML template
        html_content = render_to_string("email_templates/event_reminder.html", {
            "event": event,
            "formatted_time": timezone.localtime(
                timezone.make_aware(datetime.combine(event.date, event.time))
            ).strftime('%I:%M %p %Z on %B %d, %Y')
        })

        # Create email
        email = EmailMultiAlternatives(
            subject=f"⏰ Reminder: {event.title} starts soon!",
            body=strip_tags(html_content),
            from_email="Momento <momento7641253@gmail.com>",
            to=[recipient_email],
            reply_to=["momento7641253@gmail.com"]  
        )
        email.attach_alternative(html_content, "text/html")

        # Send and log
        email.send(fail_silently=False) 
        logger.info(f"Email sent to {recipient_email}")
        return True

    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP Auth Error: Check email credentials.")
    except smtplib.SMTPException as e:
        logger.error(f"SMTP Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    return False