from django.contrib import admin
from django.urls import path,include
from .views import *
from app import views
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
router = routers.DefaultRouter()
router.register('user',UserViewSet,basename='UserViewSet')
router.register('task',TaskViewSet,basename='TaskViewSet')
urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', UserLogin.as_view(), name='login'),
    path('tasks/<int:pk>/add_comment/', TaskViewSet.as_view({'post': 'add_comment'}), name='task-add-comment'),
    path('tass/<int:pk>/update_status/',TaskViewSet.as_view({'post':'update_status'}),name='update status'),
    path('create_user',views.create_user),


]+router.urls