from rest_framework import serializers
from .models import Discount
from courses.models import Course


class DiscountSerializer(serializers.ModelSerializer):
    """
    سریالایزر اصلی مدل Discount
    برای ساخت، ویرایش و نمایش کد تخفیف
    """

    class Meta:
        model = Discount
        fields = [
            'id',
            'code',
            'discount_type',
            'amount',
            'course',
            'user',
            'max_uses',
            'used_count',
            'start_date',
            'end_date',
            'is_active',
            'created_at',
        ]
        read_only_fields = ['used_count', 'created_at']

    def validate(self, attrs):
        """
        اعتبارسنجی کلی:
        - چک بازه زمانی
        - چک محدوده‌ی amount برای تخفیف درصدی (۰ تا صد)
        """

        # وقتی instance وجود دارد (update)، بعضی فیلدها ممکن است تو attrs نباشند
        discount_type = attrs.get(
            'discount_type',
            getattr(self.instance, 'discount_type', None)
        )
        amount = attrs.get(
            'amount',
            getattr(self.instance, 'amount', None)
        )

        start_date = attrs.get(
            'start_date',
            getattr(self.instance, 'start_date', None)
        )
        end_date = attrs.get(
            'end_date',
            getattr(self.instance, 'end_date', None)
        )

        errors = {}

        # اعتبارسنجی بازه زمانی
        if start_date and end_date and end_date <= start_date:
            errors['end_date'] = 'تاریخ پایان باید بعد از تاریخ شروع باشد.'

        # اعتبارسنجی مقدار تخفیف درصدی
        if discount_type == Discount.PERCENTAGE and amount is not None:
            # اینجا فرض می‌کنیم amount برای درصدی باید بین ۰ و ۱۰۰ باشد
            if amount < 0 or amount > 100:
                errors['amount'] = 'برای نوع درصدی، مقدار تخفیف باید بین صفر تا صد باشد.'
        
        # اعتبارسنجی مقدار تخفیف ثابت
        if discount_type == Discount.FIXED and amount is not None:
            if amount < 0:
                errors['amount'] = 'برای نوع ثابت، مقدار تخفیف باید مثبت باشد.'

        if errors:
            raise serializers.ValidationError(errors)

        return attrs
        

class DiscountApplySerializer(serializers.Serializer):
    """
    سریالایزر برای مرحله‌ی اعمال کد تخفیف در checkout
    - ورودی: code, course_id (اختیاری)، price
    - خروجی: قیمت نهایی + اطلاعات خود کد
    """

    code = serializers.CharField(label='کد تخفیف', trim_whitespace=True)
    course_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        label='شناسه دوره'
    )
    price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0,
        label='مبلغ اولیه'
    )

    # فیلدهای خروجی (read-only)
    final_price = serializers.DecimalField(
        max_digits=12,
        decimal_places=2,
        read_only=True,
        label='مبلغ بعد از تخفیف'
    )
    discount_detail = DiscountSerializer(source='discount', read_only=True)

    def validate(self, data):
        """
        - پیدا کردن Discount بر اساس code
        - پیدا کردن Course (اگر course_id داده شده)
        - صدا زدن متد is_valid مدل
        - محاسبه‌ی قیمت نهایی با apply_discount
        """

        request = self.context.get('request')
        user = getattr(request, 'user', None)

        code = data.get('code')
        if code:
            code = code.strip()  # حذف فاصله‌های اضافی
        
        course_id = data.get('course_id')
        price = data.get('price')

        # ۱. پیدا کردن کد تخفیف (case-insensitive)
        try:
            discount = Discount.objects.get(code__iexact=code)
        except Discount.DoesNotExist:
            raise serializers.ValidationError({
                'code': 'کد تخفیف پیدا نشد.'
            })

        # ۲. اگر course_id داده شده، دوره را پیدا کن
        course = None
        if course_id is not None:
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                raise serializers.ValidationError({
                    'course_id': 'دوره‌ای با این شناسه پیدا نشد.'
                })

        # ۲.۵. اگر کد تخفیف مخصوص یک دوره است، باید course_id ارسال شود
        if discount.course and course_id is None:
            raise serializers.ValidationError({
                'course_id': 'این کد تخفیف مخصوص یک دوره است. لطفاً شناسه دوره را ارسال کنید.'
            })

        # ۲.۶. اگر کد تخفیف مخصوص یک کاربر است، باید کاربر لاگین کرده باشد
        if discount.user and (user is None or not user.is_authenticated):
            raise serializers.ValidationError({
                'code': 'این کد تخفیف مخصوص کاربران خاص است. لطفاً وارد حساب کاربری خود شوید.'
            })

        # ۳. اعتبارسنجی با متد is_valid خود مدل
        is_valid, message = discount.is_valid(user=user, course=course)
        if not is_valid:
            raise serializers.ValidationError({
                'code': message
            })

        # ۴. محاسبه‌ی مبلغ نهایی
        final_price = discount.apply_discount(price)

        # داده‌های کمکی را اضافه می‌کنیم تا در Response استفاده کنیم
        data['discount'] = discount
        data['final_price'] = final_price

        return data
