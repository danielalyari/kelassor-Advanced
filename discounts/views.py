from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from .models import Discount
from .serializers import DiscountSerializer, DiscountApplySerializer


class DiscountViewSet(viewsets.ModelViewSet):
    """
    CRUD برای کدهای تخفیف
    بهتره فقط ادمین‌ها به این دسترسی داشته باشن.
    """
    queryset = Discount.objects.all().order_by('-created_at')
    serializer_class = DiscountSerializer
    permission_classes = [IsAdminUser]


class ApplyDiscountView(APIView):
    """
    API برای اعمال کد تخفیف در مرحله‌ی checkout
    ورودی: code, price, (اختیاری: course_id)
    خروجی: price نهایی + اطلاعات کد
    """

    # اگر می‌خوای فقط کاربر لاگین کرده استفاده کنه:
    # permission_classes = [IsAuthenticated]

    # اگر می‌خوای مهمان هم تست کنه:
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = DiscountApplySerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # داده‌ی validate شده، شامل final_price و خود discount
            data = {
                'code': serializer.validated_data['code'],
                'course_id': serializer.validated_data.get('course_id'),
                'price': serializer.validated_data['price'],
                'final_price': serializer.validated_data['final_price'],
                'discount': DiscountSerializer(
                    serializer.validated_data['discount']
                ).data
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

