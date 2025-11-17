

from django.db import models
from django.conf import settings


class SupportTicket(models.Model):
    """مدل تیکت پشتیبانی؛ مربوط به یک کاربر با وضعیت و زمان‌بندی."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    # عنوان کوتاهِ موضوع تیکت
    subject = models.CharField(max_length=255, verbose_name="موضوع تیکت")
    # توضیحات کامل تیکت (شرح مشکل یا درخواست)
    description = models.TextField(verbose_name="توضیحات تیکت")
    # وضعیت تیکت: باز، در حال انجام یا بسته شده
    status = models.CharField(
        max_length=50,
        choices=[('open', 'باز'), ('in_progress', 'در حال انجام'),
                 ('closed', 'بسته شده')],
        default='open',
        verbose_name="وضعیت",
    )
    # زمان ایجاد تیکت (تنها خواندنی)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ایجاد")
    # زمان آخرین به‌روزرسانی تیکت (بروزرسانی خودکار)
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="آخرین به‌روزرسانی")

    def __str__(self):
        return f"تیکت {self.subject} برای {self.user.username}"


class TicketStatus(models.Model):
    """مدل برای ثبت تغییرات وضعیت تیکت‌ها و زمان‌بندی آن‌ها."""
    ticket = models.ForeignKey('SupportTicket', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=[('open', 'باز'), (
        'closed', 'بسته شده'), ('in_progress', 'در حال انجام')], verbose_name="وضعیت تیکت")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="آخرین به‌روزرسانی")

    def __str__(self):
        return f"وضعیت {self.status} برای {self.ticket}"


class IssueReport(models.Model):
    """مدل گزارش مشکل/تخلف توسط کاربر برای ارسال به تیم پشتیبانی."""
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    # دسته یا عنوان کوتاه مشکل
    issue_type = models.CharField(max_length=255, verbose_name="نوع مشکل")
    # توضیحات کامل گزارش
    description = models.TextField(verbose_name="توضیحات")
    # زمان ثبت گزارش
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="تاریخ ثبت")

    def __str__(self):
        return f"گزارش از {self.user.username} - {self.issue_type}"
