from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
import random
import string


class EmailVerification(models.Model):
    # use settings.AUTH_USER_MODEL as a string to avoid import-time lookup
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    # allow null for existing rows when we add this field during migrations
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True)  # زمان ایجاد کد

    def generate_verification_code(self):
        # Generate a random 6-digit verification code
        characters = string.ascii_letters + string.digits
        return ''.join(random.choices(characters)for i in range(6))

    def is_expired(self):
        # چک کردن منقضی شدن کد (24 ساعت)
        from django.utils import timezone
        from datetime import timedelta
        return timezone.now() - self.created_at > timedelta(hours=24)

    def save(self, *args, **kwargs):
        if not self.verification_code:
            self.verification_code = self.generate_verification_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username}-{self.verification_code}"


class CustomUser(AbstractUser):
    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=False, blank=False)

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=False, blank=False)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True, null=True)  # بیوگرافی
    linkedin = models.URLField(blank=True, null=True)  # لینک LinkedIn
    github = models.URLField(blank=True, null=True)  # لینک GitHub

    def __str__(self):
        return f'{self.user.username} Profile'
# The following models were moved to their respective apps:
# - Achievement, Notification -> core app (core.models)
# - Cart, Payment, PurchaseHistory, Subscription, Invoice -> payments app (payments.models)
# - Review -> courses app (courses.models)
