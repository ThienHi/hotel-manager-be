from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from hotel_manager import constants
from hotel_manager.users.models import Bill, BillDetail, Product
from hotel_manager.users.api.bill_serializers import BillSerializer, BillDetailSerializer, BillDetailUpdateSerializer
from hotel_manager.users.api.pagination_class import CustomPagination


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]
    # pagination_class = CustomPagination

    def update(self, request, pk, *args, **kwargs):
        user = request.user
        sz = BillSerializer(data=request.data)
        if user.user_type == constants.CUSTOMER:
            return Response("NOT_PERMISSION", status=status.HTTP_401_UNAUTHORIZED)
        if sz.is_valid(raise_exception = True):
            bill = Bill.objects.filter(id=pk).first()
            if not bill:
                return Response("BILL_NOT_EXIST", status=status.HTTP_400_BAD_REQUEST)
            bill.refund_money = sz.data.get('refund_money')
            bill.receive_money = sz.data.get('receive_money')
            bill.payment = sz.data.get('payment')
            bill.from_date = sz.data.get('from_date')
            bill.save()
            return Response("UPDATE_BILL_SUCCESS", status=status.HTTP_200_OK)


class BillDetailViewSet(viewsets.ModelViewSet):
    queryset = BillDetail.objects.all()
    serializer_class = BillDetailSerializer
    permission_classes = [IsAuthenticated]
    # pagination_class = CustomPagination

    def update(self, request, pk, *args, **kwargs):
        user = request.user
        sz = BillDetailUpdateSerializer(data=request.data)
        sz.is_valid(raise_exception = True)
        if user.user_type == constants.CUSTOMER:
            return Response("NOT_PERMISSION", status=status.HTTP_401_UNAUTHORIZED)
        if sz.is_valid(raise_exception = True):
            bill_detail = BillDetail.objects.filter(id=pk).first()
            if not bill_detail:
                return Response("BILL_DETAIL_NOT_EXIST", status=status.HTTP_400_BAD_REQUEST)
            elif bill_detail.bill_id != sz.data.get('bill_id'):
                return Response("BILL_NOT_UPDATE", status=status.HTTP_400_BAD_REQUEST)
            _product = Product.objects.filter(id=sz.data.get('product_id'))
            bill_detail.amount = sz.data.get('amount')
            bill_detail.product_id = _product
            bill_detail.save()
            return Response("UPDATE_BILL_DETAIL_SUCCESS", status=status.HTTP_200_OK)
