"""
Redução de Dimensionalidade - Binarização de Imagem
====================================================
Converte imagem colorida → escala de cinza → binarizada (P&B)

Dependências: opencv-python, numpy
Instalação:   pip install opencv-python numpy
"""

import cv2
import numpy as np
import sys
import os


def carregar_imagem(caminho: str) -> np.ndarray:
    """Carrega a imagem do disco — compatível com caminhos com acentos e espaços."""
    import numpy as np
    with open(caminho, "rb") as f:
        dados = np.frombuffer(f.read(), dtype=np.uint8)
    img = cv2.imdecode(dados, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Imagem não encontrada ou corrompida: '{caminho}'")
    return img


def converter_cinza(img: np.ndarray) -> np.ndarray:
    """Converte imagem BGR (colorida) para escala de cinza (0–255)."""
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


def binarizar(img_cinza: np.ndarray, limiar: int = 127) -> np.ndarray:
    """
    Aplica threshold simples: pixels acima do limiar → 255 (branco),
    demais → 0 (preto).

    Parâmetros
    ----------
    img_cinza : imagem em escala de cinza
    limiar    : valor de corte (padrão 127, metade de 255)
    """
    _, img_bin = cv2.threshold(img_cinza, limiar, 255, cv2.THRESH_BINARY)
    return img_bin


def salvar_resultados(img_cinza: np.ndarray, img_bin: np.ndarray,
                      pasta_saida: str = "assets") -> None:
    """Salva as imagens geradas na pasta de saída."""
    os.makedirs(pasta_saida, exist_ok=True)

    caminho_cinza = os.path.join(pasta_saida, "imagem_cinza.jpg")
    caminho_bin   = os.path.join(pasta_saida, "imagem_binaria.jpg")

    cv2.imwrite(caminho_cinza, img_cinza)
    cv2.imwrite(caminho_bin,   img_bin)

    print(f"[✓] Salvo: {caminho_cinza}")
    print(f"[✓] Salvo: {caminho_bin}")


def exibir_resultados(img_original: np.ndarray,
                      img_cinza:    np.ndarray,
                      img_bin:      np.ndarray) -> None:
    """
    Exibe as três versões da imagem lado a lado em uma única janela.
    Pressione qualquer tecla para fechar.
    """
    # Converte cinza/bin para BGR para que cv2.hstack funcione
    cinza_bgr = cv2.cvtColor(img_cinza, cv2.COLOR_GRAY2BGR)
    bin_bgr   = cv2.cvtColor(img_bin,   cv2.COLOR_GRAY2BGR)

    # Redimensiona para mesma altura antes de empilhar (caso dimensões difiram)
    h = img_original.shape[0]
    def resize_h(im, altura):
        fator = altura / im.shape[0]
        return cv2.resize(im, (int(im.shape[1] * fator), altura))

    painel = np.hstack([
        resize_h(img_original, h),
        resize_h(cinza_bgr,    h),
        resize_h(bin_bgr,      h),
    ])

    cv2.imshow("Original | Cinza | Binária", painel)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    # ── Configurações ────────────────────────────────────────────────────────
    # Altere o caminho abaixo para a sua imagem de entrada
    CAMINHO_IMAGEM = "assets/lena.jpg"   # imagem de entrada
    LIMIAR         = 127                 # limiar de binarização (0–255)
    # ─────────────────────────────────────────────────────────────────────────

    # Permite passar o caminho via argumento de linha de comando
    if len(sys.argv) > 1:
        CAMINHO_IMAGEM = sys.argv[1]
    if len(sys.argv) > 2:
        LIMIAR = int(sys.argv[2])

    print(f"\n{'='*50}")
    print("  Redução de Dimensionalidade — Binarização")
    print(f"{'='*50}")
    print(f"  Imagem : {CAMINHO_IMAGEM}")
    print(f"  Limiar : {LIMIAR}")
    print(f"{'='*50}\n")

    # 1. Carregar
    print("[1/4] Carregando imagem...")
    img_original = carregar_imagem(CAMINHO_IMAGEM)
    print(f"      Dimensões: {img_original.shape[1]}×{img_original.shape[0]} px  |  Canais: {img_original.shape[2]}")

    # 2. Escala de cinza
    print("[2/4] Convertendo para escala de cinza...")
    img_cinza = converter_cinza(img_original)

    # 3. Binarizar
    print("[3/4] Binarizando a imagem...")
    img_bin = binarizar(img_cinza, LIMIAR)

    # 4. Salvar e exibir
    print("[4/4] Salvando resultados...")
    salvar_resultados(img_cinza, img_bin)

    print("\n[✓] Processamento concluído! Exibindo janela...\n")
    exibir_resultados(img_original, img_cinza, img_bin)


if __name__ == "__main__":
    main()