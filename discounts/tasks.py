# discounts/tasks.py
from django.utils import timezone
from celery import shared_task
from .models import Discount

@shared_task
def deactivate_expired_discounts():
    """هر شب اجرا میشه: کدهای منقضی‌شده رو غیرفعال کن."""
    now = timezone.now()
    expired = Discount.objects.filter(is_active=True, end_date__lt=now)
    count = expired.update(is_active=False)
    return f"{count} discount codes deactivated."
