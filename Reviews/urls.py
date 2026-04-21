from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewset

router = DefaultRouter()
router.register(r'reviews', ReviewViewset, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
