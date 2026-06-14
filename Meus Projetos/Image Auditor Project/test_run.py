import os
from Image_Auditor import load_image, calculate_brightness, resize_to_web, convert_and_save_webp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(BASE_DIR, "test_images")

# ── Diagnóstico: lista o que realmente existe na pasta ──
print(f"📁 Conteúdo de test_images/:")
for f in os.listdir(TEST_DIR):
    print(f"   → '{f}'")

# ── Busca automática pela primeira imagem disponível ──
EXTENSOES = ('.jpg', '.jpeg', '.png', '.webp', '.bmp')
image_path = None

for nome in os.listdir(TEST_DIR):
    if nome.lower().endswith(EXTENSOES) and not nome.startswith('resultado'):
        image_path = os.path.join(TEST_DIR, nome)
        print(f"\n✅ Arquivo encontrado automaticamente: '{nome}'")
        break

if image_path is None:
    print("❌ Nenhuma imagem encontrada em test_images/. Verifique a pasta.")
    exit(1)

try:
    print("\n🚀 Iniciando testes do Image_Auditor...")

    img = load_image(image_path)
    print("✅ Imagem carregada com sucesso!")

    brightness = calculate_brightness(img)
    print(f"📊 Brilho médio da imagem: {brightness:.2f}")

    img_otimizada = resize_to_web(img, max_width=800)
    print(f"📐 Redimensionada! Nova largura: {img_otimizada.width}px")

    output_path = os.path.join(TEST_DIR, "resultado_final.webp")
    convert_and_save_webp(img_otimizada, output_path, quality=85)
    print(f"💾 Sucesso! Imagem salva em: {output_path}")

except Exception as e:
    print(f"\n⚠️ Erro: {e}")