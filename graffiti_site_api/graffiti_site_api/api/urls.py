from django.urls import path, include
from graffiti_site_api.api import views


urlpatterns = [
    path('auth/', include('rest_framework.urls')),
    path('users/', views.UserListCreate.as_view(), name='user-list'),
    path('users/<username>/', views.UserRetrieve.as_view(), name='user-detail'),
    path('users/<username>/graffiti/', views.UserAddGraffiti.as_view(), name='user-graffiti'),
    path('graffiti/', views.GraffitiListCreate.as_view(), name='graffiti-list'),
    path('graffiti/<pk>/', views.GraffitiRetrieve.as_view(), name='graffiti-detail'),
]
