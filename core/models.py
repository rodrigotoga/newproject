from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class Cliente(AbstractUser):
    telefone = models.CharField(max_length=20)
    
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

class Corte(models.Model):  # Não herda de AbstractUser
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data = models.DateField()
    hora = models.TimeField()
    valor = models.DecimalField(max_digits=6, decimal_places=2)
    realizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.cliente.username} - {self.data} {self.hora}"