"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path

from inventory.models import Product
from django.shortcuts import redirect


def inventory_dashboard_view(request):
    return admin.site._registry[Product].dashboard_view(request)


def site_root_view(request):
    """Redirect the site root to the admin index so 'View site' works."""
    return redirect('admin:index')

urlpatterns = [
    path('', site_root_view),
    path('admin/inventory/dashboard/', admin.site.admin_view(inventory_dashboard_view), name='inventory-dashboard'),
    path('admin/', admin.site.urls),
]
