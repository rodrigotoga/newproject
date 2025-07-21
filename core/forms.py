from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente, Corte

class ClienteRegisterForm(UserCreationForm):
    email = forms.EmailField()
    telefone = forms.CharField(max_length=20)

    class Meta:
        model = Cliente
        fields = ['username', 'email', 'telefone', 'password1', 'password2']

class CorteForm(forms.ModelForm):
    TIPO_CORTE_CHOICES = [
        ('Corte de cabelo', 'Corte de cabelo (R$25)'),
        ('Corte + Barba', 'Corte + Barba (R$40)'),
        ('Corte + Sobrancelha', 'Corte + Sobrancelha (R$30)'),
    ]
    tipo_corte = forms.ChoiceField(choices=TIPO_CORTE_CHOICES, required=False, label='Tipo de Corte (exemplo)')

    class Meta:
        model = Corte
        fields = ['data', 'hora', 'valor']