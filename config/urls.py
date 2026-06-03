from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from core.sigefar_public_views import public_home, public_module_detail, public_submodule_detail, public_submodule_index
from core.views import panel

urlpatterns = [
    path('', public_home, name='home'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('panel/', panel, name='panel'),
    path('modulos/<slug:slug>/', public_module_detail, name='module_detail'),
    path('modulos/<slug:module_slug>/submodulos/', public_submodule_index, name='submodule_index'),
    path('modulos/<slug:module_slug>/<slug:submodule_slug>/', public_submodule_detail, name='submodule_detail'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
