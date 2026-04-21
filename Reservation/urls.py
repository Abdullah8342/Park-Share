from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ReservationViewset

router = DefaultRouter()
router.register('',ReservationViewset,basename='reservation')

urlpatterns = [
    path('api/',include(router.urls)),
]
