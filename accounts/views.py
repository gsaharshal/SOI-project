from django.contrib.auth import login

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import User
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer
)


class AuthViewSet(GenericViewSet):

    queryset = User.objects.all()

    def get_permissions(self):

        if self.action in [
            "register",
            "login"
        ]:
            return [AllowAny()]

        return [IsAuthenticated()]

    @action(detail=False, methods=["post"])
    def register(self, request):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=["post"])
    def login(self, request):

        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        login(request, user)

        return Response({
            "message": "Login successful",
            "user": UserSerializer(user).data
        })

    @action(detail=False, methods=["get"])
    def profile(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)