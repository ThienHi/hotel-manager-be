from django.conf import settings
from rest_framework import permissions, status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from hotel_manager.users.api.serializers import MyTokenObtainPairSerializer, RefreshTokenSerializer


User = get_user_model()


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class LogoutView(generics.GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)