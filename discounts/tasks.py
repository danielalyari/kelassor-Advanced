# discounts/tasks.py
from django.utils import timezone
from .models import DiscountCode

def deactivate_expired_discounts():
    """هر شب اجرا میشه: کدهای منقضی‌شده رو غیرفعال کن."""
    now = timezone.now()
    expired = DiscountCode.objects.filter(is_active=True, valid_to__lt=now)
    count = expired.update(is_active=False)
    return f"{count} discount codes deactivated."
