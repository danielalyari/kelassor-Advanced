from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SupportTicket, IssueReport
from .serializers import SupportTicketSerializer, IssueReportSerializer


class SupportTicketCreateView(generics.CreateAPIView):
	"""ایجاد تیکت (POST) — user از request.user پر می‌شود."""
	permission_classes = [IsAuthenticated]
	queryset = SupportTicket.objects.all()
	serializer_class = SupportTicketSerializer

	def perform_create(self, serializer):
		# مالک تیکت همیشه کاربر جاری است؛ از ارسال user توسط کلاینت جلوگیری می‌کنیم
		serializer.save(user=self.request.user)


class SupportTicketListView(APIView):
	"""لیست تیکت‌های کاربر (GET)."""
	permission_classes = [IsAuthenticated]

	def get(self, request, *args, **kwargs):
		tickets = SupportTicket.objects.filter(user=request.user).order_by('-created_at')
		serializer = SupportTicketSerializer(tickets, many=True)
		return Response(serializer.data)


class SupportTicketDetailView(generics.RetrieveUpdateDestroyAPIView):
	"""مشاهده/ویرایش/حذف تیکت متعلق به کاربر (GET/PUT/DELETE)."""
	permission_classes = [IsAuthenticated]
	serializer_class = SupportTicketSerializer

	def get_queryset(self):
		# فقط تیکت‌های کاربر جاری
		return SupportTicket.objects.filter(user=self.request.user)


class IssueReportCreateView(generics.CreateAPIView):
	"""ایجاد گزارش مشکل (POST) — user از request.user پر می‌شود."""
	permission_classes = [IsAuthenticated]
	queryset = IssueReport.objects.all()
	serializer_class = IssueReportSerializer

	def perform_create(self, serializer):
		# گزارش به نام کاربر فعلی ثبت می‌شود
		serializer.save(user=self.request.user)
from django.shortcuts import render

# Create your views here.
