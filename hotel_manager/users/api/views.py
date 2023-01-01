from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from .serializers import UserSerializer, RegisterSerializer
from hotel_manager import constants

User = get_user_model()


class UserViewSet(RetrieveModelMixin, ListModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

    @action(detail=False, methods=["GET"])
    def me(self, request):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(status=status.HTTP_200_OK, data=serializer.data)


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.user_type == constants.ADMIN:
            return self.create(request, *args, **kwargs)
        else:
            return Response("Not Permission!!!", status= status.HTTP_401_UNAUTHORIZED)


class RegisterCustomerView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        if data.get('user_type') != constants.CUSTOMER:
            return Response("Only create account guest!!!", status= status.HTTP_401_UNAUTHORIZED)
        else:
            return self.create(request, *args, **kwargs)
