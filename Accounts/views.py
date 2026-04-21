"""
Views.py
"""

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import (
    UserSerializers,
    RequestOTPSerializer,
    VerifyOTPSerializer,
    PasswordResetSerializer,
)
from .utils import generate_otp, save_otp, verify_otp
from .tasks import send_otp_email

# Create your views here.


class Signup(CreateAPIView):
    """
    Signup
    """

    serializer_class = UserSerializers


class ForgetPassword(APIView):
    """
    Forget Password
    """

    def post(self, request):
        """
        Post Request
        """
        serializers = RequestOTPSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        email = serializers.validated_data["email"]
        user = get_object_or_404(User, email=email)
        if user is None:
            return Response({"message": f"User With That {email} Does Not Exist"})
        otp = generate_otp()
        save_otp(email, otp)
        send_otp_email.delay(email, otp)
        print("send otp mail")
        return Response({"message": "opt sent to your Mail"})


class PasswordReset(APIView):
    """
    Password Reset
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        POST
        """
        serializers = PasswordResetSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        password = serializers.validated_data["password"]
        current_user = request.user
        current_user.set_password(password)
        current_user.save()
        return Response({"message": "Password Changed Successfuly"})


class RequestOTPView(APIView):
    """
    reqest otp
    """

    def post(self, request):
        """
        Post Request
        """
        serializers = RequestOTPSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        email = serializers.validated_data["email"]
        user = get_object_or_404(User, email=email)
        if user is None:
            print("user is None")
            return Response({"message": f"User With That {email} Does Not Exist"})
        otp = generate_otp()
        save_otp(email, otp)
        send_otp_email.delay(email, otp)
        print("send otp mail")
        return Response({"message": "opt sent"})


class VerifyOTPView(APIView):
    """
    VerifyOTPView
    """

    def post(self, request):
        """
        POST
        """
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        if not verify_otp(email, otp):
            return Response({"error": "Invalid OTP"}, status=400)

        user, _ = User.objects.get_or_create(email=email)
        user.is_verified = True
        user.save()
        refresh = RefreshToken.for_user(user)

        return Response({"access": str(refresh.access_token), "refresh": str(refresh)})
