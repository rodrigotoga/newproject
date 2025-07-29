from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import ClienteRegisterForm, CorteForm, BarbeiraRegisterForm, CorteBarbeiraForm, StatusBarbeariaForm
from .models import Corte, StatusBarbearia
from datetime import date, datetime


def home(request):
    if request.user.is_authenticated:
        if request.user.is_barbeira:
            return redirect('barbeira_dashboard')
        else:
            return redirect('dashboard')
    else:
        # Verificar status da barbearia para mostrar na página inicial
        status, created = StatusBarbearia.objects.get_or_create(id=1)
        return render(request, 'home.html', {'status_barbearia': status})

def offline(request):
    """Página offline para PWA"""
    return render(request, 'offline.html')
    
    
def register(request):
    if request.method == 'POST':
        form = ClienteRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = ClienteRegisterForm()
    return render(request, 'register.html', {'form': form})

def register_barbeira(request):
    if request.method == 'POST':
        form = BarbeiraRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_barbeira = True
            user.save()
            messages.success(request, 'Conta da barbeira criada com sucesso!')
            return redirect('login')
    else:
        form = BarbeiraRegisterForm()
    return render(request, 'register_barbeira.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            if user.is_barbeira:
                return redirect('barbeira_dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
    return render(request, 'login.html')

#@login_required
def dashboard(request):
    # Verificar se a barbearia está aberta
    status, created = StatusBarbearia.objects.get_or_create(id=1)
    barbearia_aberta = status.aberta and status.esta_aberta_agora()
    
    historico = Corte.objects.filter(cliente=request.user).order_by('-data')
    return render(request, 'dashboard.html', {
        'historico': historico,
        'barbearia_aberta': barbearia_aberta,
        'status_barbearia': status
    })

#@login_required
def agendar_corte(request):
    # Verificar se a barbearia está aberta
    status, created = StatusBarbearia.objects.get_or_create(id=1)
    barbearia_aberta = status.aberta and status.esta_aberta_agora()
    
    if not barbearia_aberta:
        messages.warning(request, 'A barbearia está fechada no momento. Tente novamente durante o horário de funcionamento.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CorteForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data['data']
            hora = form.cleaned_data['hora']
            if Corte.objects.filter(data=data, hora=hora).exists():
                erro = "Horário já ocupado."
                return render(request, 'agendar.html', {'form': form, 'erro': erro})
            corte = form.save(commit=False)
            corte.cliente = request.user
            corte.save()
            return redirect('dashboard')
    else:
        form = CorteForm()
    return render(request, 'agendar.html', {'form': form})

# @login_required
def fila_espera(request):
    data = request.GET.get('data')
    fila = 0
    horarios = []
    if data:
        cortes = Corte.objects.filter(data=data).order_by('hora')
        fila = cortes.count()
        horarios = [c.hora.strftime('%H:%M') for c in cortes]
    return render(request, 'fila.html', {'fila': fila, 'data': data, 'horarios': horarios})

#@login_required
def agendamentos_dia(request):
    from datetime import date
    hoje = date.today()
    agendados = Corte.objects.filter(data=hoje)
    return render(request, 'agendados.html', {'agendados': agendados})

def logout_view(request):
    logout(request)
    return redirect('login')

# ========== ÁREA DA BARBEIRA ==========

@login_required
def barbeira_dashboard(request):
    if not request.user.is_barbeira:
        return redirect('dashboard')
    
    hoje = date.today()
    agendamentos_hoje = Corte.objects.filter(data=hoje).order_by('hora')
    total_agendamentos = agendamentos_hoje.count()
    agendamentos_realizados = agendamentos_hoje.filter(realizado=True).count()
    
    # Status da barbearia
    status, created = StatusBarbearia.objects.get_or_create(id=1)
    
    context = {
        'agendamentos_hoje': agendamentos_hoje,
        'total_agendamentos': total_agendamentos,
        'agendamentos_realizados': agendamentos_realizados,
        'status_barbearia': status,
    }
    return render(request, 'barbeira/dashboard.html', context)

@login_required
def barbeira_agendamentos(request):
    if not request.user.is_barbeira:
        return redirect('dashboard')
    
    data_filtro = request.GET.get('data', date.today().strftime('%Y-%m-%d'))
    agendamentos = Corte.objects.filter(data=data_filtro).order_by('hora')
    
    context = {
        'agendamentos': agendamentos,
        'data_filtro': data_filtro,
    }
    return render(request, 'barbeira/agendamentos.html', context)

@login_required
def barbeira_corte_novo(request):
    if not request.user.is_barbeira:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CorteBarbeiraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Corte agendado com sucesso!')
            return redirect('barbeira_agendamentos')
    else:
        form = CorteBarbeiraForm()
    
    return render(request, 'barbeira/corte_form.html', {'form': form, 'titulo': 'Novo Corte'})

@login_required
def barbeira_corte_editar(request, corte_id):
    if not request.user.is_barbeira:
        return redirect('dashboard')
    
    corte = get_object_or_404(Corte, id=corte_id)
    
    if request.method == 'POST':
        form = CorteBarbeiraForm(request.POST, instance=corte)
        if form.is_valid():
            form.save()
            messages.success(request, 'Corte atualizado com sucesso!')
            return redirect('barbeira_agendamentos')
    else:
        form = CorteBarbeiraForm(instance=corte)
    
    return render(request, 'barbeira/corte_form.html', {'form': form, 'titulo': 'Editar Corte'})

@login_required
def barbeira_corte_deletar(request, corte_id):
    if not request.user.is_barbeira:
        return redirect('dashboard')
    
    corte = get_object_or_404(Corte, id=corte_id)
    if request.method == 'POST':
        corte.delete()
        messages.success(request, 'Corte deletado com sucesso!')
        return redirect('barbeira_agendamentos')
    
    return render(request, 'barbeira/corte_confirm_delete.html', {'corte': corte})

@login_required
def barbeira_marcar_realizado(request, corte_id):
    if not request.user.is_barbeira:
        return redirect('dashboard')
    
    corte = get_object_or_404(Corte, id=corte_id)
    corte.realizado = not corte.realizado
    corte.save()
    
    return JsonResponse({'realizado': corte.realizado})

@login_required
def barbeira_status(request):
    if not request.user.is_barbeira:
        return redirect('dashboard')
    
    status, created = StatusBarbearia.objects.get_or_create(id=1)
    
    if request.method == 'POST':
        form = StatusBarbeariaForm(request.POST, instance=status)
        if form.is_valid():
            form.save()
            messages.success(request, f'Configurações da barbearia atualizadas com sucesso!')
            return redirect('barbeira_dashboard')
    else:
        form = StatusBarbeariaForm(instance=status)
    
    return render(request, 'barbeira/status.html', {'form': form, 'status': status})

@login_required
def barbeira_relatorio(request):
    if not request.user.is_barbeira:
        return redirect('dashboard')
    
    data_inicio = request.GET.get('data_inicio', date.today().strftime('%Y-%m-%d'))
    data_fim = request.GET.get('data_fim', date.today().strftime('%Y-%m-%d'))
    
    cortes = Corte.objects.filter(
        data__gte=data_inicio,
        data__lte=data_fim
    ).order_by('data', 'hora')
    
    total_valor = sum(corte.valor for corte in cortes if corte.realizado)
    total_cortes = cortes.filter(realizado=True).count()
    
    context = {
        'cortes': cortes,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'total_valor': total_valor,
        'total_cortes': total_cortes,
    }
    return render(request, 'barbeira/relatorio.html', context)