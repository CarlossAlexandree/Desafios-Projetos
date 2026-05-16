import json
from pathlib import Path
from flashcard import Flashcard

class Deck:
    def __init__(self, filepath: str = "data/deck.json"):
        self.filepath = Path(filepath)
        self.cards: list[Flashcard] = []
        self.load()

    def load(self) -> None:
        if self.filepath.exists():
            with open(self.filepath) as f:
                self.cards = [Flashcard.from_dict(d) for d in json.load(f)]

    def save(self) -> None:
        self.filepath.parent.mkdir(exist_ok=True)
        with open(self.filepath, "w") as f:
            json.dump([c.to_dict() for c in self.cards], f, indent=2, ensure_ascii=False)

    def add_card(self, front: str, back: str) -> None:
        self.cards.append(Flashcard(front=front, back=back))
        self.save()

    def due_cards(self) -> list[Flashcard]:
        return [c for c in self.cards if c.is_due()]

    def stats(self) -> dict:
        return {
            "total": len(self.cards),
            "due_today": len(self.due_cards()),
            "mastered": sum(1 for c in self.cards if c.interval >= 21),
        }