from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import EmailVerification, UserProfile, CustomUser
from .serializers import (
    UserSerializer, UserProfileSerializer, EmailVerificationSerializer
)


class UserProfileView(APIView):
    """نمایش و ویرایش پروفایل کاربر (فقط user profile).

    توجه: دستاوردها (achievements) اکنون در اپ `core` قرار دارند و از این ویو حذف شدند.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profile = UserProfile.objects.get(user=request.user)
        profile_serializer = UserProfileSerializer(profile)
        return Response({
            "profile": profile_serializer.data,
        })

    def put(self, request, *args, **kwargs):
        profile = UserProfile.objects.get(user=request.user)
        profile_serializer = UserProfileSerializer(
            profile, data=request.data.get('profile'))

        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response({
                "profile": profile_serializer.data,
            })
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):

    def post(self, request, *args, **kwargs):
        verification_code = request.data.get('verification_code')
        user_id = request.data.get('user_id')
        try:
            email_verification = EmailVerification.objects.get(
                user__id=user_id, verification_code=verification_code)
            email_verification.is_verified = True
            email_verification.save()
            return Response({'message': 'ایمیل با موفقیت تایید شد.'}, status=status.HTTP_200_OK)
        except EmailVerification.DoesNotExist:
            return Response({'error': 'کد تایید نامعتبر است.'}, status=status.HTTP_400_BAD_REQUEST)


# signup registration
class UserCreateView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


# Note: Cart/Payment/Review/PurchaseHistory/Notification/Achievement
# related views were moved to their respective apps:
# - payments app (cart/payment/invoice/subscription)
# - courses app (review)
# - core app (achievement/notification)

# Support ticket and issue-report views were moved to the `tickets` app.
