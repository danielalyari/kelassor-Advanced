from rest_framework import serializers
from .models import Payment,PaymentTransaction, GroupPayment, Refund, PaymentEvent, Cart, Invoice, PurchaseHistory, Subscription, InstallmentPayment

# ---------------------------------------------------------
# سریالایزر برای مدل Payment
# ---------------------------------------------------------
class PaymentSerializer(serializers.ModelSerializer):
    """سریالایزر برای مدل Payment"""
    
    '''class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "amount_paid",
            "payment_date",
            "payment_status",
            "transaction_id",
        ]
        read_only_fields = ["id", "payment_status", "payment_date"]'''

# ---------------------------------------------------------
# سریالایزر برای مدل PaymentTransaction
# ---------------------------------------------------------
class PaymentTransactionSerializer(serializers.ModelSerializer):
    """سریالایزر برای مدل PaymentTransaction"""
    
    class Meta:
        model = PaymentTransaction
        fields = [
            "id",
            "user",
            "amount",
            "status",
            "transaction_id",
            "gateway",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

# ---------------------------------------------------------
# سریالایزر برای مدل GroupPayment
# ---------------------------------------------------------
class GroupPaymentSerializer(serializers.ModelSerializer):
    """سریالایزر برای مدل GroupPayment"""
    members_count = serializers.SerializerMethodField()

    class Meta:
        model = GroupPayment
        fields = [
            "id",
            "users",
            "total_amount",
            "status",
            "transaction_id",
            "created_at",
            "members_count",
        ]
        read_only_fields = ["id", "created_at", "members_count"]

    def get_members_count(self, obj):
        """محاسبه تعداد اعضای گروه"""
        return obj.users.count()

# ---------------------------------------------------------
# سریالایزر برای مدل Refund
# ---------------------------------------------------------
class RefundSerializer(serializers.ModelSerializer):
    """سریالایزر برای مدل Refund"""
    
    class Meta:
        model = Refund
        fields = [
            "id",
            "transaction",
            "amount",
            "reason",
            "status",
            "requested_at",
        ]
        read_only_fields = ["id", "requested_at"]

# ---------------------------------------------------------
# سریالایزر برای مدل PaymentEvent
# ---------------------------------------------------------
class PaymentEventSerializer(serializers.ModelSerializer):
    """سریالایزر برای مدل PaymentEvent"""
    
    class Meta:
        model = PaymentEvent
        fields = [
            "id",
            "event_type",
            "transaction",
            "payload",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]

# ---------------------------------------------------------
# سریالایزر برای مدل Cart
# ---------------------------------------------------------
class CartSerializer(serializers.ModelSerializer):
    """سریالایزر برای مدل Cart"""
    
    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "product_name",
            "quantity",
            "total_price",
        ]
        read_only_fields = ["id"]

# ---------------------------------------------------------
# سریالایزر برای مدل Invoice
# ---------------------------------------------------------
class InvoiceSerializer(serializers.ModelSerializer):
    """سریالایزر برای مدل Invoice"""
    
    class Meta:
        model = Invoice
        fields = [
            "id",
            "user",
            "transaction",
            "invoice_number",
            "amount",
            "issued_at",
        ]
        read_only_fields = ["id", "issued_at"]

# ---------------------------------------------------------
# سریالایزر برای مدل PurchaseHistory
# ---------------------------------------------------------
class PurchaseHistorySerializer(serializers.ModelSerializer):
    """سریالایزر برای مدل PurchaseHistory"""
    
    class Meta:
        model = PurchaseHistory
        fields = [
            "id",
            "user",
            "product_name",
            "amount",
            "purchased_at",
        ]
        read_only_fields = ["id", "purchased_at"]

# ---------------------------------------------------------
# سریالایزر برای مدل Subscription
# ---------------------------------------------------------
class SubscriptionSerializer(serializers.ModelSerializer):
    """سریالایزر برای مدل Subscription"""
    
    class Meta:
        model = Subscription
        fields = [
            "id",
            "user",
            "plan",
            "start_date",
            "end_date",
        ]
        read_only_fields = ["id", "start_date"]

# ---------------------------------------------------------
# سریالایزر برای مدل InstallmentPayment
# ---------------------------------------------------------
class InstallmentPaymentSerializer(serializers.ModelSerializer):
    """سریالایزر برای مدل InstallmentPayment"""
    
    class Meta:
        model = InstallmentPayment
        fields = [
            "id",
            "user",
            "transaction",
            "amount",
            "installment_number",
            "total_installments",
            "due_date",
            "status",
        ]
        read_only_fields = ["id"]
