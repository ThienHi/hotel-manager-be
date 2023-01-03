from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from hotel_manager.users.api.views import UserViewSet
from hotel_manager.users.api.hotel import HotelImageViewSet, HotelRoomViewSet, HotelView
from hotel_manager.users.api.product import ProductViewSet
from hotel_manager.users.api.bill import BillViewSet, BillDetailViewSet


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("hotel-image", HotelImageViewSet)
router.register("hotel", HotelView)
router.register("room", HotelRoomViewSet)
router.register("product", ProductViewSet)
router.register("bill", BillViewSet)
router.register("bill-detail", BillDetailViewSet)


app_name = "api"
urlpatterns = router.urls
