from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Cliente, Corte, StatusBarbearia

class ClienteRegisterForm(UserCreationForm):
    email = forms.EmailField()
    telefone = forms.CharField(max_length=20)

    class Meta:
        model = Cliente
        fields = ['username', 'email', 'telefone', 'password1', 'password2']

class BarbeiraRegisterForm(UserCreationForm):
    email = forms.EmailField()
    telefone = forms.CharField(max_length=20)
    is_barbeira = forms.BooleanField(initial=True, widget=forms.HiddenInput())

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

class CorteBarbeiraForm(forms.ModelForm):
    class Meta:
        model = Corte
        fields = ['cliente', 'data', 'hora', 'valor', 'realizado', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }

class StatusBarbeariaForm(forms.ModelForm):
    class Meta:
        model = StatusBarbearia
        fields = ['aberta']
        widgets = {
            'aberta': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }