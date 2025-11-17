from rest_framework import serializers
from .models import Notification, Achievement


class NotificationSerializer(serializers.ModelSerializer):
    """
    سریالایزر اعلان‌ها برای تبدیل مدل به JSON
    """
    level_display = serializers.CharField(source='get_level_display', read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'user',
            'message',
            'url',
            'level',
            'level_display',
            'is_read',
            'created_at',
        ]
        read_only_fields = ['created_at', 'level_display']


class AchievementSerializer(serializers.ModelSerializer):
    """
    سریالایزر دستاوردها (Achievements)
    """
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Achievement
        fields = [
            'id',
            'user',
            'title',
            'description',
            'type',
            'type_display',
            'meta',
            'date_achieved',
            'image',
        ]
        read_only_fields = ['date_achieved', 'type_display']

