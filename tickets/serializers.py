from rest_framework import serializers
from .models import SupportTicket, TicketStatus, IssueReport


class SupportTicketSerializer(serializers.ModelSerializer):
    """سریالایزر برای مدل تیکت پشتیبانی."""
    class Meta:
        model = SupportTicket
        fields = ['id', 'subject', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']


class TicketStatusSerializer(serializers.ModelSerializer):
    """سریالایزر برای مدل وضعیت تیکت."""
    class Meta:
        model = TicketStatus
        fields = ['id', 'ticket', 'status', 'updated_at']
        read_only_fields = ['updated_at']


class IssueReportSerializer(serializers.ModelSerializer):
    """سریالایزر برای مدل گزارش مشکل."""
    class Meta:
        model = IssueReport
        fields = ['id', 'issue_type', 'description', 'created_at']
        read_only_fields = ['created_at']