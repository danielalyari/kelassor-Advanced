from django.contrib import admin
from core.views import test_rabbitmq
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# تنظیمات Swagger UI
schema_view = get_schema_view(
    openapi.Info(
        title="کلاسور API",
        default_version='v1',
        description="مستندات API پروژه کلاسور",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
    # User Management
    path('api/users/', include('user.urls')),
    path('api/auth/', include('rest_framework.urls')),  # DRF auth views
    
    # Password Reset
    path('api/password-reset/', auth_views.PasswordResetView.as_view(),
         name='password_reset'),
    path('api/password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(), 
         name='password_reset_done'),
    path('api/reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('api/reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    # Social Authentication
    path('accounts/', include('allauth.urls')),
    
    # API Documentation (Swagger UI)
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
    
    # App URLs
    path('api/courses/', include('courses.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/tickets/', include('tickets.urls')),
    path('api/discounts/', include('discounts.urls')),
    path('test-rabbit/', test_rabbitmq), 
]

# اضافه کردن مسیرهای media در محیط توسعه
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)