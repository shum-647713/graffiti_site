from django.urls import path, include
from rest_framework.routers import DefaultRouter
from graffiti_site_api.api import views


router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('', include(router.urls)),
]
