from django.core.mail import send_mail
from celery import shared_task
from django.utils.timezone import now
from .models import Course

@shared_task
def send_reminder_to_users():
    """ ارسال یادآوری به کاربران برای دوره‌هایی که به زودی تمام می‌شوند. """
    now_time = now()
    soon_to_end_courses = Course.objects.filter(end_date__lte=now_time + timezone.timedelta(days=2))  # دوره‌هایی که ۲ روز دیگر تمام می‌شوند
    for course in soon_to_end_courses:
        users_to_notify = course.enrollments.filter(status='Enrolled')  # کاربرانی که در دوره ثبت‌نام کرده‌اند
        for enrollment in users_to_notify:
            send_mail(
                f"یادآوری: دوره شما در حال تمام شدن است!",
                f"دوره {course.title} که در آن ثبت‌نام کرده‌اید، به زودی تمام می‌شود. لطفاً هر چه زودتر آن را تکمیل کنید.",
                'from@example.com',
                [enrollment.user.email],
                fail_silently=False,
    
            )
@shared_task
def update_course_status():
    """ بروزرسانی وضعیت دوره‌ها به 'اتمام' بعد از تاریخ پایان دوره. """
    now_time = now()
    completed_courses = Course.objects.filter(end_date__lte=now_time, status='in_progress')
    for course in completed_courses:
        course.status = 'Completed'
        course.save()



@shared_task
def process_course_data():
    """ پردازش داده‌های دوره‌ها (مثلاً تحلیل پیشرفت یا محاسبات خاص) """
    courses = Course.objects.all()
    for course in courses:
        # محاسبات و پردازش‌های مورد نظر
        pass
