from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class Cliente(AbstractUser):
    telefone = models.CharField(max_length=20)
    is_barbeira = models.BooleanField(default=False)  # Campo para identificar se é barbeira
    
    # Adicione estas linhas para resolver os conflitos:
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='cliente_groups',  # Nome único
        related_query_name='cliente'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='cliente_permissions',  # Nome único
        related_query_name='cliente'
    )

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

class StatusBarbearia(models.Model):
    aberta = models.BooleanField(default=False)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    # Horários de funcionamento
    hora_abertura = models.TimeField(default='08:00', help_text='Horário de abertura')
    hora_fechamento = models.TimeField(default='18:00', help_text='Horário de fechamento')
    
    # Dias da semana
    segunda = models.BooleanField(default=True, verbose_name='Segunda-feira')
    terca = models.BooleanField(default=True, verbose_name='Terça-feira')
    quarta = models.BooleanField(default=True, verbose_name='Quarta-feira')
    quinta = models.BooleanField(default=True, verbose_name='Quinta-feira')
    sexta = models.BooleanField(default=True, verbose_name='Sexta-feira')
    sabado = models.BooleanField(default=True, verbose_name='Sábado')
    domingo = models.BooleanField(default=False, verbose_name='Domingo')
    
    class Meta:
        verbose_name = 'Status da Barbearia'
        verbose_name_plural = 'Status da Barbearia'
    
    def __str__(self):
        return f"Barbearia {'Aberta' if self.aberta else 'Fechada'}"
    
    def esta_aberta_agora(self):
        """Verifica se a barbearia está aberta no momento atual"""
        from datetime import datetime, time
        agora = datetime.now()
        
        # Verifica se é um dia de funcionamento
        dias_semana = {
            0: self.segunda,  # Segunda
            1: self.terca,     # Terça
            2: self.quarta,    # Quarta
            3: self.quinta,    # Quinta
            4: self.sexta,     # Sexta
            5: self.sabado,    # Sábado
            6: self.domingo,   # Domingo
        }
        
        if not dias_semana.get(agora.weekday(), False):
            return False
        
        # Verifica se está no horário de funcionamento
        hora_atual = agora.time()
        return self.hora_abertura <= hora_atual <= self.hora_fechamento

class Corte(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    realizado = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.cliente.username} - {self.data} {self.hora}"