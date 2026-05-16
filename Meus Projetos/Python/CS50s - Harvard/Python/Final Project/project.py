import sys
import os
import shutil
from deck import Deck
from scheduler import update_card
from image_generator import create_card_image
from image_viewer import show_image

def main():
    deck = Deck()
    if len(sys.argv) < 2:
        print("Uso: python project.py [add|review|stats]")
        sys.exit(1)

    match sys.argv[1]:
        case "add":
            add_card(deck)
        case "review":
            review(deck)
        case "stats":
            show_stats(deck)
        case _:
            print("Comando inválido.")

def add_card(deck: Deck) -> None:
    front = input("Frente do card: ").strip()
    back  = input("Verso do card: ").strip()
    if not front or not back:
        raise ValueError("Card não pode ter campos vazios.")
    deck.add_card(front, back)
    print("Card adicionado!")

def review(deck: Deck) -> None:
    due = deck.due_cards()
    if not due:
        print("Nenhum card para revisar hoje!")
        return

    print(f"\nIniciando revisão de {len(due)} card(s)... Preparando imagens visuais.")
    
    # Limpa pasta temporária antiga se existir
    if os.path.exists("temp_cards"):
        shutil.rmtree("temp_cards")

    for card in due:
        print("\n--- Novo Card ---")
        
        # 1. Gera e Mostra a FRENTE (Pergunta) visualmente
        front_img_path = create_card_image(card.front, type='frente')
        show_image(front_img_path)
        
        # Aguarda interação baseada na imagem aberta
        input("Pressione Enter no terminal após ler a PERGUNTA (imagem aberta) para ver a resposta...")
        
        # 2. Gera e Mostra o VERSO (Resposta) visualmente
        back_img_path = create_card_image(card.back, type='verso')
        show_image(back_img_path)
        
        # 3. Coleta o feedback de qualidade e aplica o algoritmo SM-2
        quality = get_quality()
        update_card(card, quality)

    deck.save()
    
    # Limpeza final das imagens temporárias para manter o projeto limpo
    if os.path.exists("temp_cards"):
        shutil.rmtree("temp_cards")
        
    print(f"\nRevisão concluída! {len(due)} card(s) revisados. As imagens temporárias foram apagadas.")

def get_quality() -> int:
    while True:
        try:
            q = int(input("Quão bem você lembrou? (0=esqueceu ... 5=perfeito): "))
            if 0 <= q <= 5:
                return q
        except ValueError:
            pass
        print("Digite um número entre 0 e 5.")

def show_stats(deck: Deck) -> None:
    s = deck.stats()
    print(f"Total de cards : {s['total']}")
    print(f"Para revisar hoje: {s['due_today']}")
    print(f"Dominados (intervalo ≥21d): {s['mastered']}")

if __name__ == "__main__":
    main()