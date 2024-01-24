from django.urls import path, include
from graffiti_site_api.api import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='auth')),
    path('users/', views.UserListCreate.as_view(), name='user-list'),
    path('users/<username>/', views.UserRetrieve.as_view(), name='user-detail'),
    path('users/<username>/username/', views.UserChangeUsername.as_view(), name='user-username'),
    path('users/<username>/password/', views.UserChangePassword.as_view(), name='user-password'),
    path('users/<username>/graffiti/', views.UserAddGraffiti.as_view(), name='user-graffiti'),
    path('graffiti/', views.GraffitiListCreate.as_view(), name='graffiti-list'),
    path('graffiti/<pk>/', views.GraffitiRetrieve.as_view(), name='graffiti-detail'),
    path('graffiti/<pk>/photos/', views.GraffitiAddPhoto.as_view(), name='graffiti-photos'),
    path('photos/', views.PhotoList.as_view(), name='photo-list'),
    path('photos/<pk>/', views.PhotoRetrieve.as_view(), name='photo-detail'),
    path('', views.api_root),
    path('auth/', views.auth_list, name='auth-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
