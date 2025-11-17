from django.db import models
from django.conf import settings


class Payment(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار"),
        ("paid", "پرداخت شده"),
        ("failed", "ناموفق"),
        ("refunded", "برگشت داده شده"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment({self.user.username})"


# ---------------------------------------------------------
# 1) مدل سبد خرید
# ---------------------------------------------------------
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Cart({self.user.username})"


# ---------------------------------------------------------
# 2) مدل تراکنش پرداخت (نتیجهٔ درگاه)
# ---------------------------------------------------------
class PaymentTransaction(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار"),
        ("success", "موفق"),
        ("failed", "ناموفق"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    transaction_id = models.CharField(
        max_length=255,
        unique=True,  # شناسه بانک
    )
    gateway = models.CharField(
        max_length=100,
        null=True,
        blank=True,  # درگاه پرداخت
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PaymentTransaction({self.transaction_id})"


# ---------------------------------------------------------
# 3) مدل فاکتور (Invoice)
# ---------------------------------------------------------
class Invoice(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction = models.ForeignKey(
        PaymentTransaction,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    invoice_number = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    issued_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Invoice({self.invoice_number})"

# ---------------------------------------------------------
# 4) تاریخچه خرید (برای مشاهده سابقه)
# ---------------------------------------------------------
class PurchaseHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PurchaseHistory({self.user.username})"


# ---------------------------------------------------------
# 5) اشتراک کاربر (Subscription)
# ---------------------------------------------------------
class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan = models.CharField(max_length=255)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def __str__(self):
        return f"Subscription({self.plan})"


# ---------------------------------------------------------
# 6) پرداخت قسطی (Installments)
# ---------------------------------------------------------
class InstallmentPayment(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار"),
        ("paid", "پرداخت شده"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    transaction = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    installment_number = models.PositiveIntegerField()
    total_installments = models.PositiveIntegerField()
    due_date = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )

    def __str__(self):
        return f"Installment {self.installment_number}"


# ---------------------------------------------------------
# 7) پرداخت گروهی
# ---------------------------------------------------------
class GroupPayment(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار"),
        ("completed", "تکمیل شده"),
    ]

    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    transaction_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"GroupPayment({self.transaction_id})"


# ---------------------------------------------------------
# 8) بازپرداخت (Refund)
# ---------------------------------------------------------
class Refund(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار"),
        ("completed", "کامل شده"),
    ]

    transaction = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reason = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Refund({self.transaction.transaction_id})"


# ---------------------------------------------------------
# 9) مهم‌ترین مدل برای اتصال به RabbitMQ
#    PaymentEvent (ضد گم‌شدن پیام‌ها)
# ---------------------------------------------------------
class PaymentEvent(models.Model):
    EVENT_TYPES = [
        ("transaction_created", "تراکنش ایجاد شد"),
        ("transaction_success", "پرداخت موفق"),
        ("transaction_failed", "پرداخت ناموفق"),
        ("refund_requested", "درخواست بازپرداخت"),
        ("refund_completed", "بازپرداخت انجام شد"),
        ("invoice_created", "فاکتور ایجاد شد"),
    ]

    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    transaction = models.ForeignKey(
        PaymentTransaction,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    # اطلاعات لازم برای ارسال به RabbitMQ
    payload = models.JSONField()

    sent_to_queue = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PaymentEvent({self.event_type})"
