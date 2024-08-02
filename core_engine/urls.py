from django.urls import path
from core_engine.views import EngineView
urlpatterns = [
    path('engine/', EngineView.as_view(), name="annovate")
]
