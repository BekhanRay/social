import config
from django.core.mail import send_mail
from django.utils.crypto import get_random_string

from apps.users.models import CustomUser


def send_verification_mail(email):
    generated_code = get_random_string(6, '0123456789')
    subject = 'Код подтверждения от Amici'
    message = f'Ваш код подтверждения:\n{generated_code}\n' \
              f'Вы получили это письмо, потому что ваш адрес электронной почты был использован для регистрации или изменения настроек на нашем сайте.\n\n' \
              f'Пожалуйста, введите этот код на сайте, чтобы подтвердить ваш адрес электронной почты.\n\n' \
              f'Спасибо, что используете наш сайт.'

    from_email = config.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])
    return generated_code
