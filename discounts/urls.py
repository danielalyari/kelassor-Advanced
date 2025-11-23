from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DiscountViewSet, ApplyDiscountView

router = DefaultRouter()
router.register('codes', DiscountViewSet, basename='discount')

urlpatterns = [
    # مدیریت کدهای تخفیف (CRUD)
    path('', include(router.urls)),

    # endpoint برای اعمال تخفیف در checkout
    path('apply/', ApplyDiscountView.as_view(), name='discount-apply'),
]