from django.views.generic import TemplateView

class LoginView(TemplateView):
    template_name = 'utiles/login.html'

class RegisterView(TemplateView):
    template_name = 'utiles/register.html'

class RegisterContinueView(TemplateView):
    template_name = 'utiles/signup-continue.html'

class UploadView(TemplateView):
    template_name = 'utiles/analyzer.html'

class GetAnalyzeView(TemplateView):
    template_name = 'utiles/yeild.html'

class UserDemoView(TemplateView):
    template_name = 'utiles/demo-book.html'

class DrDashboardBasicView(TemplateView):
    template_name = 'utiles/doctor-basic-dash.html'

class DrDashboardAdvanceView(TemplateView):
    template_name = 'utiles/doctor-basic-dash.html'

class AboutView(TemplateView):
    template_name = 'utiles/about.html'

class ProfileView(TemplateView):
    template_name = 'utiles/profile.html'