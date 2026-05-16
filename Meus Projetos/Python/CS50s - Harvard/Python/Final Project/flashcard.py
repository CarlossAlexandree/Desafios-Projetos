from dataclasses import dataclass, field
from datetime import date

@dataclass
class Flashcard:
    front: str
    back: str
    # campos do SM-2
    easiness: float = 2.5      # fator de facilidade (mín 1.3)
    interval: int = 1          # dias até a próxima revisão
    repetitions: int = 0       # quantas vezes foi respondido corretamente
    next_review: str = field(default_factory=lambda: str(date.today()))

    def to_dict(self) -> dict:
        return self.__dict__

    @classmethod
    def from_dict(cls, data: dict) -> "Flashcard":
        return cls(**data)

    def is_due(self) -> bool:
        return date.fromisoformat(self.next_review) <= date.today()