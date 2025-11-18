import threading
import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

logger = logging.getLogger(__name__)

def send_mail(subject, recipient_list, body_content=None, html_content=None, attachments=None):
    def _send():
        try:
            email = EmailMultiAlternatives(
                subject=subject,
                body=body_content if body_content else "",
                from_email=settings.EMAIL_HOST_USER,
                to=recipient_list,
            )

            
            if html_content and not body_content:
                email.attach_alternative(html_content, "text/html")

            
            if attachments:
                for f in attachments:
                    email.attach(f.name, f.read(), f.content_type)

            email.send(fail_silently=False)
            logger.info(f"✅ Email sent to {recipient_list}")
        except Exception as e:
            logger.error(f"❌ Error sending email: {e}")

    threading.Thread(target=_send).start()
