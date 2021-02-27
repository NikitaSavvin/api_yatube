from django.urls import path
from django.conf.urls import include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, UserViewSet
from rest_framework.authtoken import views

v1_router = DefaultRouter()

v1_router.register('api/v1/users', UserViewSet, basename='users')
v1_router.register('posts', PostViewSet, basename='posts')
v1_router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
urlpatterns = [
    path('v1/', include(v1_router.urls)),  
]
urlpatterns += [
    path('v1/api-token-auth/', views.obtain_auth_token)
]
