from rest_framework import serializers
from hotel_manager.users.models import Bill, BillDetail, HotelRoom, Product
from django.utils import timezone


class BillSerializer(serializers.ModelSerializer):
    room_id = serializers.IntegerField(required=True)
    customer = serializers.CharField(required=True)
    refund_money = serializers.FloatField(required=True)
    receive_money = serializers.FloatField(required=True)
    payment = serializers.FloatField(required=True)
    from_date = serializers.DateTimeField(required=True)
    to_date = serializers.DateTimeField(required=True)

    def validate(self, attrs):
        pass

    def create(self, validated_data):
        room_id = HotelRoom.objects.filter(id=validated_data['room_id'])
        bill = Bill.objects.create(
            room_id=room_id,
            customer=validated_data.get('customer'),
            refund_money=None,
            receive_money=None,
            payment=None,
            from_date=None,
            to_date=timezone.now()
        )
        bill.save()
        return bill

    class Meta:
        model = Bill
        fields = '__all__'


class BillDetailSerializer(serializers.ModelSerializer):
    bill_id = serializers.IntegerField(required=True)
    product_id = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(required=True)
    offer = serializers.IntegerField(required=True)

    def validate(self, attrs):
        pass

    def create(self, validated_data):
        bill_id = Bill.objects.filter(id=validated_data['bill_id']).first()
        product_id = Product.objects.filter(id=validated_data['product_id']).first()
        offer = validated_data['offer'] if validated_data['offer'] != 0 else 1
        bill_detail = BillDetail.objects.create(
            room_id=bill_id,
            product_id=product_id,
            amount=validated_data['amount'],
            price=(validated_data['amount'] * product_id.price) * offer,
            offer=offer
        )
        bill_detail.save()
        return bill_detail

    class Meta:
        model = BillDetail
        fields = '__all__'


class BillDetailUpdateSerializer(serializers.Serializer):
    bill_id = serializers.IntegerField(required=True)
    product_id = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(required=True)
