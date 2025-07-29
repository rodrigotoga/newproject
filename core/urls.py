from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('register/barbeira/', views.register_barbeira, name='register_barbeira'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('agendar/', views.agendar_corte, name='agendar'),
    path('fila/', views.fila_espera, name='fila'),
    path('agendados/', views.agendamentos_dia, name='agendados'),
    
    # URLs da área da barbeira
    path('barbeira/', views.barbeira_dashboard, name='barbeira_dashboard'),
    path('barbeira/agendamentos/', views.barbeira_agendamentos, name='barbeira_agendamentos'),
    path('barbeira/corte/novo/', views.barbeira_corte_novo, name='barbeira_corte_novo'),
    path('barbeira/corte/<int:corte_id>/editar/', views.barbeira_corte_editar, name='barbeira_corte_editar'),
    path('barbeira/corte/<int:corte_id>/deletar/', views.barbeira_corte_deletar, name='barbeira_corte_deletar'),
    path('barbeira/corte/<int:corte_id>/realizado/', views.barbeira_marcar_realizado, name='barbeira_marcar_realizado'),
    path('barbeira/status/', views.barbeira_status, name='barbeira_status'),
    path('barbeira/relatorio/', views.barbeira_relatorio, name='barbeira_relatorio'),
]