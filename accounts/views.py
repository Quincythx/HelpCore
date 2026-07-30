from rest_framework import generics, permissions
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from .models import User, EmailVerificationToken
from .serializers import UserCreateSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import LoginOTP



class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == request.user.Role.ADMIN


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        with transaction.atomic():
            user = serializer.save()
            token = EmailVerificationToken.objects.create(user=user)

            verification_link = f"http://127.0.0.1:8000/api/verify-email/{token.token}/"

            subject = "Welcome to HelpCore — Verify Your Account"
            message = (
                f"Hi {user.first_name or user.employee_id},\n\n"
                f"Welcome to HelpCore, your organization's internal IT support platform.\n\n"
                f"Your account has been created with the following details:\n"
                f"  Employee ID: {user.employee_id}\n"
                f"  Role: {user.get_role_display()}\n"
                f"  Department: {user.get_department_display()}\n\n"
                f"Before you can log in, please verify your email address by clicking the link below:\n\n"
                f"  {verification_link}\n\n"
                f"This link will expire in 2 hours for security reasons. If it expires, please contact "
                f"your administrator to request a new one.\n\n"
                f"If you did not expect this email, please disregard it or contact your IT department.\n\n"
                f"Best regards,\n"
                f"The HelpCore Team"
            )

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
            )


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, token):
        verification = get_object_or_404(EmailVerificationToken, token=token)

        if not verification.is_valid():
            return Response({"error": "This verification link has expired."}, status=400)

        user = verification.user
        user.is_email_verified = True
        user.save()
        verification.delete()

        return Response({"message": "Email verified successfully. You can now log in."})



class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        employee_id = request.data.get("employee_id")
        password = request.data.get("password")

        user = authenticate(request, username=employee_id, password=password)

        if user is None:
            return Response({"error": "Invalid employee ID or password."}, status=401)

        if not user.is_email_verified:
            return Response({"error": "Please verify your email before logging in."}, status=403)

        code = LoginOTP.generate_code()
        LoginOTP.objects.create(user=user, code=code)

        send_mail(
            "Your HelpCore Login Code",
            f"Hi {user.first_name or user.employee_id},\n\nYour login verification code is: {code}\n\nThis code expires in 10 minutes.",
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
        )

        return Response({"message": "A verification code has been sent to your email."})



class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        employee_id = request.data.get("employee_id")
        code = request.data.get("code")

        try:
            user = User.objects.get(employee_id=employee_id)
        except User.DoesNotExist:
            return Response({"error": "Invalid employee ID."}, status=400)

        otp = LoginOTP.objects.filter(user=user, code=code).order_by("-created_at").first()

        if otp is None or not otp.is_valid():
            return Response({"error": "Invalid or expired code."}, status=400)

        otp.is_used = True
        otp.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })