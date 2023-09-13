from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from stats import consumer

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('stats.urls')),
    path('admin/', admin.site.urls),
    re_path(r'ws/test-stat/$', consumer.DashboardConsumer.as_asgi()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
