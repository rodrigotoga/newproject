from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import ClienteRegisterForm, CorteForm
from .models import Corte


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return redirect('login')
    
    
def register(request):
    if request.method == 'POST':
        form = ClienteRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = ClienteRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

#@login_required
def dashboard(request):
    historico = Corte.objects.filter(cliente=request.user).order_by('-data')
    return render(request, 'dashboard.html', {'historico': historico})

#@login_required
def agendar_corte(request):
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