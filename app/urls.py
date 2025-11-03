"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views as project_views    
from tickets import views as ticket_views
from dashboard import views as dash

urlpatterns = [
    path('admin/dashboard/', dash.dashboard_view, name='admin-dashboard'),
    path('admin/dashboard/asuntos-data/', dash.get_asuntos_data, name='asuntos-data'),
    path('admin/dashboard/municipios-data/', dash.get_citas_muni, name='municipios-data'),
    path('admin/dashboard/nivel-data/', dash.get_citas_niv, name='nivel-data'),
    path('admin/', admin.site.urls),
    path('', project_views.home_view, name='home'),
    path('tickets/', include('tickets.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', ticket_views.custom_login, name='custom_login'),
    path('captcha/', include('captcha.urls')), 
]
