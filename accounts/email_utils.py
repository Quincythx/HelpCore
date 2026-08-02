import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY


def send_email(subject, message, to_email):
    resend.Emails.send({
        "from": "HelpCore <onboarding@resend.dev>",
        "to": [to_email],
        "subject": subject,
        "text": message,
    })