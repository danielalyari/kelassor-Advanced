# kelassorAdvanced/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# تنظیمات محیطی Django را بارگذاری کنید
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kelassorAdvanced.settings')  

app = Celery('kelassorAdvanced')  # همین‌طور اسم پروژه در این قسمت هم تغییر داده شده است

# بارگذاری تنظیمات Celery از فایل settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# کشف task ها در تمام اپ‌ها
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
