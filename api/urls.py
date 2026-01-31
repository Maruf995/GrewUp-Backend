from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CrewUpViewSet

router = DefaultRouter()
router.register(r'game', CrewUpViewSet, basename='game')

urlpatterns = [path('', include(router.urls))]