from django.contrib import admin
from django.urls import path,include
from .views import *
from app import views
from rest_framework_simplejwt import views as jwt_views
from rest_framework import routers
router = routers.DefaultRouter()

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', views.register, name='registration_register'),
    path('login/',views.login_view,name='login_view'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/order/create/', OrderCreateView.as_view(), name='order-create'),
    path('add_address/',AdressCreatView.as_view(),name='add_address'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('sales/',views.Salescreateview.as_view(),name='Salescreateview')




]+router.urls