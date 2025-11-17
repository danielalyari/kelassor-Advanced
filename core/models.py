from django.db import models
from django.conf import settings


# ---------------------------------------------------------
# Notification (اعلان‌ها)
# ---------------------------------------------------------
class Notification(models.Model):
    LEVEL_CHOICES = (
        ('info', 'اطلاعاتی'),
        ('success', 'موفقیت'),
        ('warning', 'هشدار'),
        ('error', 'خطا'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
    )
    message = models.TextField(verbose_name="پیام")
    url = models.CharField(
        max_length=512,
        null=True,
        blank=True,
        verbose_name="آدرس مرتبط",  # لینک به جزئیات
    )
    level = models.CharField(
        max_length=10,
        choices=LEVEL_CHOICES,
        default='info',
        verbose_name="نوع پیام",
    )
    is_read = models.BooleanField(default=False, verbose_name="خوانده شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return f"اعلان برای {self.user.username} ({self.get_level_display()})"

    class Meta:
        ordering = ['-created_at']


# ---------------------------------------------------------
# Achievement (موفقیت‌ها / دستاوردها)
# ---------------------------------------------------------
class Achievement(models.Model):
    ACHIEVEMENT_TYPES = (
        ('course', 'تکمیل دوره'),
        ('score', 'امتیاز بالا'),
        ('referral', 'معرفی کاربر جدید'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='achievements',
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(
        max_length=20,
        choices=ACHIEVEMENT_TYPES,
        default='course',
    )
    # مثلا {'course_id': 3, 'score': 95}
    meta = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="اطلاعات اضافی",
    )
    date_achieved = models.DateField(auto_now_add=True)
    image = models.ImageField(
        upload_to='achievements/',
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.title} ({self.get_type_display()}) برای {self.user.username}"

    class Meta:
        ordering = ['-date_achieved']
