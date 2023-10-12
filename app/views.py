from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,status
from rest_framework import status

from .models import Task, User,Comment
from .serializers import *
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

# Then you can use it to reference the User model
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(["POST"])
def create_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user_type=request.data.get('user_type')

    if not username or not password:
        return Response({
            "success": False,
            "message": "Username and password are required fields.",
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        password = make_password(password)  
        user = User.objects.create(username=username, password=password,user_type=user_type)
        serializer = UserSerializer(user)
        return Response({
            "success": True,
            "message": "User created successfully",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({
            "success": False,
            "message": "User creation failed",
            "error": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    def create(self, request, *args, **kwargs):
        assignee = request.user

        if assignee.user_type == 'Manager':
            return super().create(request, *args, **kwargs)
        else:
            return Response({'detail': 'Permission denied. Only managers can create tasks.'}, status=status.HTTP_403_FORBIDDEN)


    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        task = self.get_object()
        user = request.user 

        if user.user_type in ['MANAGER', 'DEVELOPER'] or user == task.assignee:
            data = request.data.copy() 
            data['task'] = task.pk
            data['user'] = user.pk
            serializer = CommentSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        task = self.get_object()
        assignee = request.user
        status = request.data.get('status')

        if assignee.user_type in ['Manager', 'DEVELOPER']:
            allowed_statuses = ['TODO', 'IN_PROGRESS', 'DONE']

            if status in allowed_statuses:
                task.status = status
                task.save()
                return Response({'detail': 'Task status updated successfully.'})
            else:
                return Response({'detail': 'Invalid status value.'})
        else:
            return Response({'detail': 'Permission denied. Only managers and developers can change task status.'})
  


class UserLogin(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        username = data['username']
        password = data['password']
        user_type=data['user_type']

        try:
            user = get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return Response({
                "success": False,
                "message": "User does not exist",
            }, status=status.HTTP_404_NOT_FOUND)

        if user.is_superuser:
            return Response({
                "success": False,
                "message": "Superusers are not allowed to log in.",
            }, status=status.HTTP_403_FORBIDDEN)

        if check_password(password, user.password):  
            user.last_login = timezone.now()
            user.save()
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return Response({
                "success": True,
                "message": "Logged In Successfully",
                "user": UserSerializer(user, context={'request': request}).data,
                "access_token": access_token,
                "refresh_token": refresh_token,
            })
        else:
            return Response({
                "success": False,
                "message": "Invalid credentials",
            }, status=status.HTTP_401_UNAUTHORIZED)
