from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from core.submodule_views import submodule_detail
from core.views import home, module_detail, panel

urlpatterns = [
    path('', home, name='home'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('panel/', panel, name='panel'),
    path('modulos/<slug:slug>/', module_detail, name='module_detail'),
    path('modulos/<slug:module_slug>/<slug:submodule_slug>/', submodule_detail, name='submodule_detail'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
