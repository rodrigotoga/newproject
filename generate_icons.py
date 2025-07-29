#!/usr/bin/env python3
"""
Script para gerar ícones básicos para PWA
Execute: python generate_icons.py
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
except ImportError:
    print("Pillow não está instalado. Instalando...")
    import subprocess
    subprocess.check_call(["pip", "install", "Pillow"])
    from PIL import Image, ImageDraw, ImageFont
    import os

def create_icon(size, text="B", bg_color="#0d6efd", text_color="white"):
    """Cria um ícone básico com texto"""
    # Criar imagem
    img = Image.new('RGB', (size, size), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Calcular tamanho da fonte (aproximadamente 60% do tamanho da imagem)
    font_size = int(size * 0.6)
    
    try:
        # Tentar usar uma fonte do sistema
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
        except:
            # Fonte padrão se não encontrar Arial
            font = ImageFont.load_default()
    
    # Calcular posição do texto (centralizado)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (size - text_width) // 2
    y = (size - text_height) // 2
    
    # Desenhar texto
    draw.text((x, y), text, fill=text_color, font=font)
    
    return img

def main():
    """Função principal para gerar todos os ícones"""
    # Tamanhos dos ícones necessários
    sizes = [16, 32, 72, 96, 128, 144, 150, 152, 180, 192, 384, 512]
    
    # Criar diretório se não existir
    icon_dir = "static/icons"
    os.makedirs(icon_dir, exist_ok=True)
    
    print("Gerando ícones para PWA...")
    
    for size in sizes:
        filename = f"icon-{size}x{size}.png"
        filepath = os.path.join(icon_dir, filename)
        
        # Criar ícone
        icon = create_icon(size)
        
        # Salvar ícone
        icon.save(filepath, "PNG")
        print(f"✓ Criado: {filename}")
    
    print(f"\n✅ Todos os ícones foram criados em: {icon_dir}")
    print("📱 Agora você pode instalar o app como PWA!")

if __name__ == "__main__":
    main() 