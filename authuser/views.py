from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegisterSerializer, UserLoginSerializer,UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
# Create your views here.

class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully", "user": {
                "id": serializer.data['id'],
                "username": serializer.data['username'],
                "email": serializer.data['email']
            }}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            print(username,password)
            try:
                user = authenticate(username=username, password=password)
                if user:
                    return Response({"message": "Login successful",
                                    "user": UserSerializer(user).data
                                     }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"error": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
