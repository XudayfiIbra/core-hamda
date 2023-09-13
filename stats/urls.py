from django.urls import path
from .views import main, dashboard, chart_data

app_name = 'stats'

urlpatterns = [
    path('', main, name='main'),
    path('<slug:slug>/', dashboard, name='dashboard'),
    path('<slug>/chart/', chart_data, name='chart'),

]
