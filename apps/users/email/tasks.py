import config
from core.celery import celery_app
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib import messages
from apps.users.models import CustomUser as User, CustomUser


@celery_app.task
def send_appeal_email_task(appeal_id):
    try:
        instance = CustomUser.objects.get(pk=appeal_id)
        email = CustomUser.objects.get(email=instance.email)
        subject = 'Golden Hut Properties'

        html_message = render_to_string('email/code_template.html', {'instance': instance})

        from_email = config.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        email = EmailMessage(
            subject,
            html_message,
            from_email,
            recipient_list,
        )
        email.content_subtype = 'html'

        email.send()
    except CustomUser.DoesNotExist:
        if instance:
            instance.send_error()
            messages.error(instance, 'The email cannot be send')
