# users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
     UserCreateView, UserProfileView, VerifyEmailView,
)
from rest_framework_simplejwt import views as jwt_views

# NOTE: model-specific CRUD endpoints (cart/payments/reviews/notifications/achievements/invoices)
# were moved to their respective apps (payments, courses, core). This router is kept empty for now.
router = DefaultRouter()

urlpatterns = [
    # ثبت‌نام و احراز هویت
    path('register/', UserCreateView.as_view(),
         name='register'),  # ثبت‌نام کاربر
    path('verify-email/', VerifyEmailView.as_view(),
         name='verify_email'),  # تایید ایمیل
    # مسیر برای ورود و دریافت توکن JWT
    path('login/', jwt_views.TokenObtainPairView.as_view(),
         name='token_obtain_pair'),  # ورود و دریافت توکن
    # پروفایل کاربر
    path('profile/', UserProfileView.as_view(),
         name='user_profile'),  # نمایش و ویرایش پروفایل
     # Include ViewSet URLs (currently empty in this app)
     path('', include(router.urls)),
]
