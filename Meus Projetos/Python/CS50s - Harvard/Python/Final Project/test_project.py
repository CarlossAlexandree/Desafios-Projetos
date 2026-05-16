import pytest
from flashcard import Flashcard
from scheduler import update_card
from project import get_quality, add_card

def test_update_card_correct():
    card = Flashcard("Q", "A")
    update_card(card, quality=5)
    assert card.repetitions == 1
    assert card.interval == 1
    assert card.easiness > 2.5  # ficou mais fácil

def test_update_card_wrong_resets():
    card = Flashcard("Q", "A", repetitions=5, interval=20)
    update_card(card, quality=1)
    assert card.repetitions == 0
    assert card.interval == 1

def test_invalid_quality_raises():
    card = Flashcard("Q", "A")
    with pytest.raises(ValueError):
        update_card(card, quality=6)

def test_is_due_today():
    card = Flashcard("Q", "A")   # next_review = hoje por padrão
    assert card.is_due() is True