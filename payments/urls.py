# payments/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, PaymentTransactionViewSet, GroupPaymentViewSet, RefundViewSet, PaymentEventViewSet

# تعریف یک DefaultRouter برای خودکار ایجاد URL ها
router = DefaultRouter()

# ثبت viewset ها در router
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'payment-transactions', PaymentTransactionViewSet, basename='payment-transaction')
router.register(r'group-payments', GroupPaymentViewSet, basename='group-payment')
router.register(r'refunds', RefundViewSet, basename='refund')
router.register(r'payment-events', PaymentEventViewSet, basename='payment-event')

# ایجاد URL ها برای اپ payments
urlpatterns = [
    path('api/', include(router.urls)),  # همه URL های مربوط به payment را در این مسیر شامل می‌کند
]
