from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models import CustomUser as User
from apps.users.email.tasks import send_appeal_email_task


@receiver(post_save, sender=User)
def send_appeal_email(sender, instance, created, **kwargs):
    if created:
        send_appeal_email_task(instance.id)
