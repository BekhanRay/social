import config
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from apps.users.models import CustomUser


def send_verification_mail(email):
    generated_code = get_random_string(6, '0123456789')
    user = CustomUser.objects.get(email=email)
    user.code = generated_code
    user.save()
    subject = 'Your verification code'
    message = f'Your verification code:\n{generated_code}\nThanks for using our application.'
    from_email = config.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])
