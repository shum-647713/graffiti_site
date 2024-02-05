from django.core.mail import send_mail
from django.conf import settings


def send_activation_link(link, send_to):
    send_mail(
        "Confirm your email to activate user",
        f"Follow the link: {link} to activate registered user. User will be deleted if not activated.",
        settings.DEFAULT_FROM_EMAIL,
        [send_to],
        fail_silently=False,
    )
