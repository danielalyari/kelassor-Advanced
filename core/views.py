from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import JsonResponse
from .rabbitmq import publish_event
from .models import Notification, Achievement
from .serializers import NotificationSerializer, AchievementSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    """
    ViewSet برای اعلان‌ها (Notification)
    کاربران معمولی فقط اعلان‌های خودشونو می‌بینن
    ادمین‌ها همه رو می‌بینن
    """
    queryset = Notification.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Notification.objects.all().order_by('-created_at')
        return Notification.objects.filter(user=user).order_by('-created_at')

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """
        اکشن اختصاصی برای خوانده‌شده علامت‌زدن اعلان
        """
        notif = self.get_object()
        notif.is_read = True
        notif.save(update_fields=['is_read'])
        return Response({'detail': 'اعلان خوانده شد ✅'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """
        علامت‌زدن همه اعلان‌های کاربر به عنوان خوانده‌شده
        """
        count = Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return Response({'detail': f'{count} اعلان خوانده شد ✅'}, status=status.HTTP_200_OK)


class AchievementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet فقط‌خواندنی برای دستاوردهای کاربر (Achievements)
    """
    queryset = Achievement.objects.all().order_by('-date_achieved')
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Achievement.objects.all().order_by('-date_achieved')
        return Achievement.objects.filter(user=user).order_by('-date_achieved')
    # core/views.py



def test_rabbitmq(request):
    publish_event(
        "test.hello",
        {"message": "salam from Django via RabbitMQ!"}
    )
    return JsonResponse({"status": "ok", "detail": "event sent to RabbitMQ"})


