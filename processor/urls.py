
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from processor.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    # Landing page conf
    path('', index, name="Home"),
    path('bud-apps/', include('utiles.urls')),

    # DB APIS
    path('account/', include('core_accounts.urls')),
    path('annovate/', include('core_engine.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
