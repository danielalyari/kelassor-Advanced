# discounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import DiscountUsage, DiscountCode, Referral

@receiver(post_save, sender=DiscountUsage)
def update_discount_usage(sender, instance, created, **kwargs):
    """هر بار که کاربر از کد تخفیف استفاده کرد، شمارنده‌ی استفاده افزایش پیدا می‌کنه."""
    if created:
        discount = instance.discount
        total_used = discount.usages.count()
        if total_used >= discount.max_usage:
            discount.is_active = False  # وقتی به حداکثر استفاده رسید، غیرفعال بشه
        discount.save(update_fields=['is_active'])

@receiver(post_save, sender=Referral)
def increase_referral_count(sender, instance, created, **kwargs):
    """وقتی کاربر جدید با کد معرف ثبت‌نام می‌کنه، شمارنده‌ی معرف زیاد می‌شه."""
    if created:
        if instance.referrer:
            codes = DiscountCode.objects.filter(referrer=instance.referrer, code_type='referral')
            for code in codes:
                code.increase_referral_count()
