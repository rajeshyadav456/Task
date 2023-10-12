from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,status
from rest_framework import status

from .models import *
from .serializers import *
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

# Then you can use it to reference the User model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from rest_framework import generics


# registration/views.py
from django.shortcuts import render, redirect
from .forms import RegistrationForm

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login/')  # Redirect to a success page
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})

# registration/views.py
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard or any other page upon successful login
        else:
            # Handle login failure (e.g., display an error message)
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})

    return render(request, 'login.html')


# dashboard/views.py
from django.shortcuts import render
from .models import Stock, Sales, Order
from django.db.models import Sum
from datetime import date

def dashboard(request):
    today = date.today()

    total_stock = Stock.objects.filter(created_at__date=today).aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_sales = Sales.objects.filter(sale_date__date=today).aggregate(Sum('quantity_sold'))['quantity_sold__sum'] or 0

    # Calculate profit and loss based on your business logic
    # This is just a placeholder, replace it with your actual calculation
    profit_loss = total_sales * 0.2

    new_orders = Order.objects.filter(order_date__date=today)

    return render(request, 'dashboard.html', {
        'total_stock': total_stock,
        'total_sales': total_sales,
        'profit_loss': profit_loss,
        'new_orders': new_orders,
    })

class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class AdressCreatView(generics.CreateAPIView):
    queryset=Address.objects.all()
    serializer_class=AddressSerializer


class Salescreateview(generics.CreateAPIView):
    queryset=Sales.objects.all()
    serializer_class=SaleAdressSerializer