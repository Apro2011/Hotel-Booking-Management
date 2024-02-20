from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from hotel_core.permissions import IsAuthenticated, IsAdminUser


# Create your views here.
class RegistrationAndListUserView(APIView):
    def get(self, request, format=None):
        users = User.objects.all().order_by("id")
        serializer = UserSerializer(users, many=True)
        return Response(
            {
                "data": serializer.data,
                "errors": [],
                "status": "Success",
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=serializer.validated_data.get("username"))
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "data": serializer.data,
                    "access": str(refresh.access_token),
                    "errors": [],
                    "status": "Success",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(
            {
                "data": [],
                "errors": serializer.errors,
                "status": "Failure",
            },
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )


class LoginAndUserDetailView(APIView):
    def post(self, request, format=None):
        username = request.data["username"]
        password = request.data["password"]
        try:
            user = User.objects.get(username=username, password=password)
        except Exception as e:
            return Response(
                {
                    "data": [],
                    "errors": ["User doesn't exist!"],
                    "status": "Failure",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "data": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                "errors": [],
                "status": "Success",
            },
            status=status.HTTP_202_ACCEPTED,
        )


class LogoutUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(
                {
                    "data": ["Logged out successfully!"],
                    "errors": [],
                    "status": "Success",
                },
                status=status.HTTP_205_RESET_CONTENT,
            )
        except TokenError as e:
            return Response(
                {
                    "data": [],
                    "errors": [f"{e}"],
                    "status": "Failure",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
