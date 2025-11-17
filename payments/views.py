from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import  Payment,PaymentTransaction, GroupPayment, Refund, PaymentEvent
from .serializers import PaymentSerializer, PaymentTransactionSerializer, GroupPaymentSerializer, RefundSerializer, PaymentEventSerializer

# ---------------------------------------------------------
# ویو برای مدیریت پرداخت‌ها
# ---------------------------------------------------------
class PaymentViewSet(viewsets.ModelViewSet):
    """ویو برای مدیریت پرداخت‌ها"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ثبت پرداخت جدید"""
        serializer.save(user=self.request.user)

# ---------------------------------------------------------
# ویو برای مدیریت تراکنش‌های پرداخت
# ---------------------------------------------------------
class PaymentTransactionViewSet(viewsets.ModelViewSet):
    """ویو برای مدیریت تراکنش‌های پرداخت"""
    queryset = PaymentTransaction.objects.all()
    serializer_class = PaymentTransactionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ثبت تراکنش پرداخت جدید"""
        serializer.save(user=self.request.user)

# ---------------------------------------------------------
# ویو برای مدیریت پرداخت‌های گروهی
# ---------------------------------------------------------
class GroupPaymentViewSet(viewsets.ModelViewSet):
    """ویو برای مدیریت پرداخت‌های گروهی"""
    queryset = GroupPayment.objects.all()
    serializer_class = GroupPaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ثبت پرداخت گروهی جدید"""
        serializer.save()

# ---------------------------------------------------------
# ویو برای مدیریت درخواست‌های بازپرداخت
# ---------------------------------------------------------
class RefundViewSet(viewsets.ModelViewSet):
    """ویو برای مدیریت درخواست‌های بازپرداخت"""
    queryset = Refund.objects.all()
    serializer_class = RefundSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ثبت درخواست بازپرداخت جدید"""
        serializer.save()

# ---------------------------------------------------------
# ویو برای مدیریت رویدادهای پرداخت (برای ارسال به RabbitMQ)
# ---------------------------------------------------------
class PaymentEventViewSet(viewsets.ModelViewSet):
    """ویو برای مدیریت رویدادهای پرداخت (برای ارسال به RabbitMQ)"""
    queryset = PaymentEvent.objects.all()
    serializer_class = PaymentEventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ثبت رویداد پرداخت جدید"""
        serializer.save()
