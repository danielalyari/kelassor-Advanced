from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CustomUser
from .models import EmailVerification
from django.conf import settings

@receiver(post_save, sender=CustomUser)
def create_email_verification(sender, instance, created, **kwargs):
    if created:
        ev = EmailVerification.objects.create(user=instance)
        send_mail(
           'کد تایید ایمیل شما',
           f'کد تایید شما: {ev.verification_code}',
           settings.EMAIL_HOST_USER,
           [instance.email],
           fail_silently=False,
       )

@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        send_mail(
           'به کلاسور خوش آمدید',
           'ثبت نام شما با موفقیت انجام شد.',
           settings.EMAIL_HOST_USER,
           [instance.email],
           fail_silently=False,
        )
