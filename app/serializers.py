from rest_framework import serializers
from .models import *
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# class LoginSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=200)
#     # user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES)
#     password = serializers.CharField(max_length=200, required=False, allow_null=True)
    
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims if needed
#         token['username'] = user.username

#         return token

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id','username','user_type','password')

# class TaskSerializer(serializers.ModelSerializer):
#     # assignee=UserSerializer()
#     class Meta:
#         model = Task
#         fields = '__all__'

# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = '__all__'


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
