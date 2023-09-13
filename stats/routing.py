from django.urls import path
from .consumer import DashboardConsumer

websocket_urlpatterns = [
    path('ws/<str:dashboard_slug>/', DashboardConsumer.as_asgi()),
]
