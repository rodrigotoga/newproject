from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('agendar/', views.agendar_corte, name='agendar'),
    path('fila/', views.fila_espera, name='fila'),
    path('agendados/', views.agendamentos_dia, name='agendados'),
]