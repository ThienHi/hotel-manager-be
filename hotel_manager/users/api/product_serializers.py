from rest_framework import serializers
from hotel_manager.users.models import Product


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False)
    amount = serializers.IntegerField(required=False)
    price = serializers.FloatField(required=False)
    detail = serializers.CharField(required=False)
    image = serializers.ImageField(required=False)

    def create(self, validated_data):
        product = Product.objects.create(
            name=validated_data.get('name'),
            amount=validated_data.get('amount'),
            price=validated_data.get('price'),
            detail=validated_data.get('detail'),
            image = validated_data.get('image')
        )
        product.save()
        return product

    class Meta:
        model = Product
        fields = '__all__'
