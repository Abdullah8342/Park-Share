from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .views import PaymentViewset

router = DefaultRouter()
router.register('',PaymentViewset,basename='payment')

urlpatterns = [
    path('api/',include(router.urls)),
]
