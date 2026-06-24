"""
Binarização Avançada com Blur Gaussiano
========================================
Reproduz o exemplo exato mostrado na aula (slide 'ponte.jpg'):
  1. Lê a imagem
  2. Converte para cinza
  3. Aplica GaussianBlur para reduzir ruído
  4. Gera binarização normal e invertida
  5. Compõe painel 2×2 igual ao slide

Uso:
    python src/binarizacao_avancada.py
    python src/binarizacao_avancada.py assets/minha_foto.jpg 160
"""

import cv2
import numpy as np
import sys
import os


def pipeline_binarizacao(caminho: str, limiar: int = 160,
                         kernel_blur: int = 7) -> dict:
    """
    Executa o pipeline completo de binarização.

    Retorna um dicionário com todas as etapas:
        original, cinza, suave, bin, binI, resultado
    """
    # ── Passo 1: Leitura ──────────────────────────────────────────────────
    img = cv2.imread(caminho)
    if img is None:
        raise FileNotFoundError(f"Arquivo não encontrado: '{caminho}'")

    # ── Passo 2: Escala de cinza ──────────────────────────────────────────
    img_cinza = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # ── Passo 3: Blur Gaussiano (suavização) ─────────────────────────────
    # Reduz ruídos antes da binarização; kernel deve ser ímpar
    k = kernel_blur if kernel_blur % 2 == 1 else kernel_blur + 1
    suave = cv2.GaussianBlur(img_cinza, (k, k), 0)

    # ── Passo 4a: Binarização normal ──────────────────────────────────────
    # Pixels > limiar → 255 (branco); demais → 0 (preto)
    _, bin_normal = cv2.threshold(suave, limiar, 255, cv2.THRESH_BINARY)

    # ── Passo 4b: Binarização invertida ──────────────────────────────────
    # Pixels > limiar → 0 (preto); demais → 255 (branco) — útil como máscara
    _, bin_inv = cv2.threshold(suave, limiar, 255, cv2.THRESH_BINARY_INV)

    # ── Passo 5: Máscara bitwise (igual ao slide) ─────────────────────────
    # Aplica a máscara invertida sobre a imagem cinza original
    mascara = cv2.bitwise_and(img_cinza, img_cinza, mask=bin_inv)

    # ── Passo 6: Composição do painel 2×2 ────────────────────────────────
    resultado = np.vstack([
        np.hstack([suave,      bin_normal]),
        np.hstack([bin_inv,    mascara]),
    ])

    return {
        "original":  img,
        "cinza":     img_cinza,
        "suave":     suave,
        "bin":       bin_normal,
        "binI":      bin_inv,
        "mascara":   mascara,
        "resultado": resultado,
    }


def salvar(etapas: dict, pasta: str = "assets") -> None:
    """Salva todas as etapas do pipeline."""
    os.makedirs(pasta, exist_ok=True)

    for nome, img in etapas.items():
        if nome == "original":
            continue  # não sobrescreve o original
        caminho = os.path.join(pasta, f"{nome}.jpg")
        cv2.imwrite(caminho, img)
        print(f"  [✓] {caminho}")


def main():
    CAMINHO = "assets/lena.jpg"
    LIMIAR  = 160
    BLUR    = 7

    if len(sys.argv) > 1: CAMINHO = sys.argv[1]
    if len(sys.argv) > 2: LIMIAR  = int(sys.argv[2])
    if len(sys.argv) > 3: BLUR    = int(sys.argv[3])

    print(f"\n{'='*50}")
    print("  Binarização Avançada (com Blur Gaussiano)")
    print(f"{'='*50}")
    print(f"  Arquivo : {CAMINHO}")
    print(f"  Limiar  : {LIMIAR}   Kernel Blur: {BLUR}×{BLUR}")
    print(f"{'='*50}\n")

    etapas = pipeline_binarizacao(CAMINHO, LIMIAR, BLUR)

    print("Salvando etapas...")
    salvar(etapas)

    print("\nExibindo painel (pressione qualquer tecla para fechar)...")
    cv2.imshow("Binarização da imagem", etapas["resultado"])
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()