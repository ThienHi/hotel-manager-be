from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from hotel_manager import constants
from hotel_manager.users.models import Product
from hotel_manager.users.api.product_serializers import ProductSerializer
from hotel_manager.users.api.pagination_class import CustomPagination


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user.id
        if user.user_type != constants.ADMIN or user.user_type != constants.MANAGER:
            return Response("NOT_PERMISSION", status=status.HTTP_401_UNAUTHORIZED)
        sz = ProductSerializer(data=request.data)
        if sz.is_valid(raise_exception = True):
            sz.save()
        return Response(sz.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk, *args, **kwargs):
        user = request.user.id
        sz = ProductSerializer(data=request.data)
        if user.user_type != constants.ADMIN or user.user_type != constants.MANAGER:
            return Response("NOT_PERMISSION", status=status.HTTP_401_UNAUTHORIZED)
        if sz.is_valid(raise_exception = True):
            product = Product.objects.filter(id=pk).first()
            if not product:
                return Response("PRODUCT_NOT_EXIST", status=status.HTTP_400_BAD_REQUEST)
            product.name = sz.data.get('name')
            product.amount = sz.data.get('amount')
            product.price = sz.data.get('price')
            product.detail = sz.data.get('detail')
            product.image = sz.data.get('image')
            product.save()
            return Response("UPDATE_HOTEL_SUCCESS", status=status.HTTP_200_OK)

    def destroy(self, request, pk, *args, **kwargs):
        user = request.user.id
        if user.user_type != constants.ADMIN or user.user_type != constants.MANAGER:
            return Response("NOT_PERMISSION", status=status.HTTP_401_UNAUTHORIZED)
        product = Product.objects.filter(id=pk).first()
        if not product:
            return Response("PRODUCT_NOT_EXIST", status=status.HTTP_400_BAD_REQUEST)
        product.delete()
        return Response("DELETE_PRODUCT_SUCCESS", status=status.HTTP_204_NO_CONTENT)
