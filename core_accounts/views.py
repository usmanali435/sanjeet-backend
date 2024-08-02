from urllib.request import urlopen
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import Response
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils import timezone
from django.db import transaction
from django.core.cache import cache
from core_accounts.renderers import UserRenderer
from core_accounts.serializers import ChangePasswordSerializer, CreateUserSerializer, PatientModelUpdateSerializer, UserInfoSerializer
from core_accounts.token import get_tokens_for_user
User = get_user_model()

import logging
logger = logging.getLogger(__name__)

class Register(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [UserRenderer]

    def error_format(self, errors):
        error_messages = []

        for field, field_errors in errors.items():
            if field == 'non_field_errors':
                for error in field_errors:
                    error_messages.append(str(error))  # Convert ErrorDetail to string
            else:
                for error in field_errors:
                    error_messages.append(str(error))  # Convert ErrorDetail to string

        return error_messages
    
    def post(self, request):
        user_type = request.data.get('user_type', 'Patient')  # Default to 'Patient'
        if user_type not in ['Patient', 'Doctor']:
            return Response({"Success": False, "Error": "Invalid user type"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_serializer = CreateUserSerializer(data=request.data)
        
        if user_serializer.is_valid():
            try:
                with transaction.atomic():  # Ensure the transaction is handled properly
                    current_user = user_serializer.save()
                    current_user.user_type = user_type
                    current_user.save()

                token = get_tokens_for_user(current_user)
                profile_url = current_user.profile_url.url if current_user.profile_url else None
                user ={
                    "_id":current_user._id,
                    "profile_url":profile_url, 
                    'email': current_user.email,
                    'bio': current_user.bio,
                    'class': user_type,
                    'first_name': current_user.first_name,
                    'last_name': current_user.last_name,
                    'token': token
                }

                return Response({"success": True,  "user":user}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"success": False, "Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            errors = user_serializer.errors
            error_messages = self.error_format(errors)
            return Response({"success": False, "errors": error_messages}, status=status.HTTP_400_BAD_REQUEST)


class EmailChecker(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [UserRenderer]

    def post(self, request):
        email = request.data.get('email', None)

        if not email:
            return Response({"success": False, "message": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Use cache to store and retrieve email checks to reduce database hits
        cache_key = f"email_exists_{email}"
        email_exists = cache.get(cache_key)

        if email_exists is None:
            email_exists = User.objects.filter(email=email).exists()
            # Cache the result for a certain period
            cache.set(cache_key, email_exists, timeout=60*5)  # Cache for 5 minutes

        if email_exists:
            return Response({"success": False, "message": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"success": True}, status=status.HTTP_202_ACCEPTED)

        
                
       
class UserLogin(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [UserRenderer]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"errors": ["Email and password are required"]}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"errors": ["Email for this user not found"]}, status=status.HTTP_400_BAD_REQUEST)

        authenticated_user = authenticate(request, username=user.email, password=password)

        if authenticated_user is None:
            return Response({"errors": ["Invalid credentials"]}, status=status.HTTP_401_UNAUTHORIZED)

        if authenticated_user.is_blocked:
            return Response({"errors": ["Account banned"]}, status=status.HTTP_400_BAD_REQUEST)

        token = get_tokens_for_user(authenticated_user)

        # Check if profile image is available
        profile_url = authenticated_user.profile_url.url if authenticated_user.profile_url else None

        user_data = {
            "_id": authenticated_user._id,
            "profile_url": profile_url,
            'email': authenticated_user.email,
            'first_name': authenticated_user.first_name,
            'last_name': authenticated_user.last_name,
            'bio': authenticated_user.bio,
            "class": authenticated_user.user_type,
            "token": token,
        }

        return Response({"message": "Logged in", "success": True, "user": user_data}, status=status.HTTP_202_ACCEPTED)
    

class UpdateTuteeProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def error_format(self, errors):
        error_messages = []

        for field, field_errors in errors.items():
            if field == 'non_field_errors':
                for error in field_errors:
                    error_messages.append(str(error))  # Convert ErrorDetail to string
            else:
                for error in field_errors:
                    error_messages.append(str(error))  # Convert ErrorDetail to string

        return error_messages
    
    def put(self, request, user_type, *args, **kwargs):
        user = request.user

        serializer = PatientModelUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            current_data = serializer.save()
            file = request.FILES.get('profile')

            if file:
                current_data.profile_url = file
                current_data.save()
            return Response({"Success": True, "Info": "Profile updated successfully.", 'user':UserInfoSerializer(current_data).data}, status=status.HTTP_200_OK)
        
        errors = serializer.errors
        
        error_messages = self.error_format(errors)
        return Response({"Success": False, "Error": error_messages}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"Success": True, "Info": "Password updated successfully."}, status=status.HTTP_200_OK)
        
        return Response({"Success": False, "Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)