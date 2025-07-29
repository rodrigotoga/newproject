#!/usr/bin/env python
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barbearia.settings')
django.setup()

from core.models import Cliente

# Marcar o usuário 'barbeira' como barbeira
try:
    barbeira = Cliente.objects.get(username='barbeira')
    barbeira.is_barbeira = True
    barbeira.save()
    print("✅ Usuário 'barbeira' marcado como barbeira com sucesso!")
except Cliente.DoesNotExist:
    print("❌ Usuário 'barbeira' não encontrado. Crie primeiro com: python manage.py createsuperuser")

# Criar status inicial da barbearia
from core.models import StatusBarbearia

status, created = StatusBarbearia.objects.get_or_create(id=1, defaults={'aberta': False})
if created:
    print("✅ Status inicial da barbearia criado (FECHADA)")
else:
    print("ℹ️ Status da barbearia já existe")

print("\n🎉 Configuração concluída!")
print("📝 Agora você pode:")
print("   1. Acessar http://localhost:8000")
print("   2. Fazer login com usuário: barbeira")
print("   3. Usar todas as funcionalidades da área da barbeira") 