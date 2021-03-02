from django.conf.urls import include
from django.urls import path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, PostViewSet, UserViewSet

v1_router = DefaultRouter()

v1_router.register('users', UserViewSet, basename='users')
v1_router.register('posts', PostViewSet, basename='posts')
v1_router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
