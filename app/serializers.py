from rest_framework import serializers
from .models import *


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields='__all__'

class SaleAdressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sales
        fields='__all__'  
