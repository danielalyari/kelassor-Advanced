# discounts/serializers.py
from rest_framework import serializers
from .models import DiscountCode, DiscountUsage, Referral


class DiscountCodeSerializer(serializers.ModelSerializer):
    """
    سریالایزر اصلی برای مدل DiscountCode
    شامل اعتبارسنجی تاریخ و مقدار تخفیف است.
    """

    # نمایش نام معرف در خروجی (در صورتی که وجود داشته باشد)
    referrer_name = serializers.SerializerMethodField()

    class Meta:
        model = DiscountCode
        fields = [
            'id', 'code', 'code_type', 'value',
            'valid_from', 'valid_to',
            'max_usage', 'per_user_limit',
            'is_active', 'course', 'user',
            'referrer', 'referrer_name', 'referral_uses'
        ]
        read_only_fields = ['referral_uses', 'referrer_name']

    def get_referrer_name(self, obj):
        """نمایش نام معرف در خروجی"""
        return obj.referrer.username if obj.referrer else None

    def validate(self, data):
        """بررسی اعتبار تاریخ و مقدار تخفیف"""
        if data['valid_to'] <= data['valid_from']:
            raise serializers.ValidationError("تاریخ پایان باید بعد از تاریخ شروع باشد.")
        if data['value'] <= 0:
            raise serializers.ValidationError("مقدار تخفیف باید بزرگتر از صفر باشد.")
        return data


class DiscountUsageSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای نمایش تاریخچه‌ی استفاده از کد تخفیف‌ها.
    """

    discount_code = serializers.CharField(source='discount.code', read_only=True)
    discount_type = serializers.CharField(source='discount.code_type', read_only=True)

    class Meta:
        model = DiscountUsage
        fields = [
            'id', 'discount', 'discount_code', 'discount_type',
            'user', 'used_at', 'order_id'
        ]
        read_only_fields = ['used_at', 'discount_code', 'discount_type']


class ReferralSerializer(serializers.ModelSerializer):
    """
    سریالایزر برای مدل Referral (ثبت معرفی کاربر جدید)
    """

    referrer_username = serializers.CharField(source='referrer.username', read_only=True)
    referred_username = serializers.CharField(source='referred_user.username', read_only=True)

    class Meta:
        model = Referral
        fields = [
            'id', 'referrer', 'referrer_username',
            'referred_user', 'referred_username',
            'created_at', 'reward_given'
        ]
        read_only_fields = ['created_at', 'referrer_username', 'referred_username']
