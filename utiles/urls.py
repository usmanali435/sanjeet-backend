from django.urls import path
from utiles.views import DrDashboardBasicView, LoginView, RegisterView,RegisterContinueView, UserDemoView, ProfileView, UploadView
urlpatterns = [
    path('signup',RegisterView.as_view(), name="signup"),
    path('signup-pass',RegisterContinueView.as_view(), name="signup-continue"),
    path('login',LoginView.as_view(), name="login"),
    path('book-demo/',UserDemoView.as_view(), name="demo"),
    path('myprofile/',ProfileView.as_view(), name="profile"),
    path('uploader/',UploadView.as_view(), name="upload"),
    path('dashboard-doctor/',DrDashboardBasicView.as_view(), name="dashboarddoctor"),

]
