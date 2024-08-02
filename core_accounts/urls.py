from django.urls import path
from core_accounts.views import ChangePasswordView, Register, UserLogin, EmailChecker, UpdateTuteeProfileView
urlpatterns = [
     path('user/register/', Register.as_view(), name='register'),
     path('user/login/', UserLogin.as_view(), name='login'),
     path('user/email-check/', EmailChecker.as_view(), name='emailcheck'),
     path('user/update-profile/<str:user_type>/', UpdateTuteeProfileView.as_view(), name='updateProfile'),
     path('user/update-profile/change-password/', ChangePasswordView.as_view(), name='chngpass'),
]
