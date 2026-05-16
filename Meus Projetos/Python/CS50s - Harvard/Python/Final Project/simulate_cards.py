from image_generator import create_card_image
from image_viewer import show_image
import os

def simulate():
    print("--- Simulando Visualização de Flashcards ---")
    
    # Simulando uma Pergunta
    pergunta = "O que é Gradiente Descendente?"
    print(f"Gerando imagem da pergunta: {pergunta}")
    path_frente = create_card_image(pergunta, type='frente')
    show_image(path_frente)
    
    input("\nPressione Enter no terminal para simular a visualização da RESPOSTA...")
    
    # Simulando uma Resposta
    resposta = "Algoritmo de otimização para encontrar o mínimo de uma função."
    print(f"Gerando imagem da resposta: {resposta}")
    path_verso = create_card_image(resposta, type='verso')
    show_image(path_verso)
    
    print("\nSimulação concluída! Verifique se as janelas de imagem abriram.")

if __name__ == "__main__":
    simulate()
    