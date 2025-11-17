from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import Course, Enrollment, Progress, Notification, Achievement

# سیگنال ارسال اعلان دوره جدید
@receiver(post_save, sender=Course)
def ارسال_اعلان_دوره_جدید(sender, instance, created, **kwargs):
    """
    این سیگنال زمانی که یک دوره جدید ایجاد می‌شود، یک اعلان برای همه کاربران ارسال می‌کند.
    """
    if created:
        # ارسال پیام به تمامی کاربران
        پیام = f"دوره جدید '{instance.title}' به پلتفرم اضافه شد."
        کاربران = instance.user.__class__.objects.all()  # ارسال به همه کاربران
        for کاربر in کاربران:
            Notification.objects.create(user=کاربر, message=پیام, created_at=now())

# سیگنال بروزرسانی تعداد ثبت‌نام‌کنندگان در دوره
@receiver(post_save, sender=Enrollment)
def بروزرسانی_تعداد_ثبت_نام(sender, instance, created, **kwargs):
    """
    این سیگنال بعد از هر ثبت‌نام در دوره، تعداد ثبت‌نام‌کنندگان آن دوره را بروزرسانی می‌کند.
    """
    if created:
        دوره = instance.course
        دوره.total_enrolled = دوره.enrollments.count()  # تعداد ثبت‌نام‌کنندگان را می‌شمارد
        دوره.save()

# سیگنال تغییر وضعیت دوره به "اتمام دوره" پس از تکمیل تمامی جلسات
@receiver(post_save, sender=Progress)
def تغییر_وضعیت_دوره_اتمام(sender, instance, **kwargs):
    """
    این سیگنال زمانی که کاربر تمامی ویدیوهای دوره را مشاهده می‌کند،
    وضعیت دوره را به 'اتمام دوره' تغییر می‌دهد.
    """
    دوره = instance.course
    # اگر تمام ویدیوهای دوره توسط کاربر مشاهده شده باشد
    if دوره.sessions == Progress.objects.filter(course=دوره, status=True).count():
        دوره.status = 'Completed'  # تغییر وضعیت به 'اتمام دوره'
        دوره.save()

# سیگنال صدور گواهی‌نامه بعد از تکمیل دوره
@receiver(post_save, sender=Course)
def صدور_گواهی_نامه_بعد_از_اتمام(sender, instance, **kwargs):
    """
    این سیگنال بعد از اتمام دوره، یک گواهی‌نامه برای کاربر صادر می‌کند.
    """
    for enrollment in instance.enrollments.all():
        if enrollment.status == 'Completed':  # اگر دوره تکمیل شده باشد
            Achievement.objects.create(
                user=enrollment.user,
                course=instance,
                achievement_type="Course Completion",
                description="دوره با موفقیت تکمیل شد"
            )



