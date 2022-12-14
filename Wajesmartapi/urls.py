"""Wajesmartapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
from books.views import IndexTemplateView
from rest_framework import permissions

from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view

schema_view = swagger_get_schema_view(
    openapi.Info(
        title="Wajesmart API",
        default_version='1.0.0',
        description="API documentation of App",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)  # for documentation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',
         include([
             path('', include(('books.api.urls', 'post'), namespace='books')),
             path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name="swagger-schema"),
         ])
         ),
    re_path(r"^$", IndexTemplateView.as_view(), name="entry-point"),  # for serving base template for vue

]
