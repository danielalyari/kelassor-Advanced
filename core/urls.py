
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, AchievementViewSet

from .views import test_rabbitmq

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'achievements', AchievementViewSet, basename='achievement')

urlpatterns = [
    path('', include(router.urls)),
    # core/urls.py
    path("test-rabbit/", test_rabbitmq, name="test_rabbitmq"),
]



