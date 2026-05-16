from datetime import date, timedelta
from flashcard import Flashcard

def update_card(card: Flashcard, quality: int) -> Flashcard:
    """
    Aplica o algoritmo SM-2.
    quality: 0-5  (0-2 = errou, 3-5 = acertou com dificuldade crescente)
    """
    if not 0 <= quality <= 5:
        raise ValueError("Qualidade deve ser entre 0 e 5")

    if quality >= 3:
        if card.repetitions == 0:
            card.interval = 1
        elif card.repetitions == 1:
            card.interval = 6
        else:
            card.interval = round(card.interval * card.easiness)
        card.repetitions += 1
    else:
        card.repetitions = 0
        card.interval = 1

    # atualiza o fator de facilidade
    card.easiness = max(1.3, card.easiness + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    card.next_review = str(date.today() + timedelta(days=card.interval))
    return card