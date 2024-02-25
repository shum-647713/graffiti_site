from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'users', views.UserViewSet)
router.register(r'graffiti', views.GraffitiViewSet)

urlpatterns = [
    path('', views.api_root),
    path('', include(router.urls)),
    path('photos/', views.PhotoList.as_view(), name='photo-list'),
    path('photos/<pk>/', views.PhotoDetail.as_view(), name='photo-detail'),
    path('auth/', views.auth_list, name='auth-list'),
    path('auth/', include('rest_framework.urls', namespace='auth')),
]
