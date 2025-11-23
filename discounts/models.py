from django.db import models
from django.utils import timezone
from django.conf import settings


class Discount(models.Model):
    PERCENTAGE = "percentage"
    FIXED = "fixed"

    DISCOUNT_TYPE_CHOICES = [
        (PERCENTAGE, "Percentage"),
        (FIXED, "Fixed Amount"),
    ]

    code = models.CharField(max_length=50, unique=True)

    discount_type = models.CharField(
        max_length=20,
        choices=DISCOUNT_TYPE_CHOICES,
        default=PERCENTAGE
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="If percentage: 0-100. If fixed: amount in currency."
    )

    # Optional: limit to a specific course
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="discounts"
    )

    # Optional: limit to a specific user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="discounts"
    )

    max_uses = models.PositiveIntegerField(default=1)
    used_count = models.PositiveIntegerField(default=0)

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.code} ({self.discount_type})"

    # ---------- VALIDATION LOGIC ----------
    def is_valid(self, user=None, course=None):
        """Basic validation for discount usability."""

        now = timezone.now()

        if not self.is_active:
            return False, "کد غیرفعال است."

        if self.start_date > now:
            return False, "کد هنوز شروع نشده."

        if self.end_date < now:
            return False, "کد منقضی شده."

        if self.used_count >= self.max_uses:
            return False, "ظرفیت کد تکمیل شده."

        if self.user and user and self.user != user:
            return False, "این کد مخصوص کاربر دیگری است."

        if self.course and course and self.course != course:
            return False, "این کد مخصوص دورهٔ دیگری است."

        return True, "کد معتبر است."

    def apply_discount(self, price):
        """Calculate price after discount."""
        if self.discount_type == self.PERCENTAGE:
            return price - (price * (self.amount / 100))

        if self.discount_type == self.FIXED:
            return max(price - self.amount, 0)

        return price

