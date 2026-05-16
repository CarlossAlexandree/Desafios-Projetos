# Flashcard Quiz — Spaced Repetition with SM-2

## Video Demo
https://youtu.be/TdkhqEImSy8

## Description

This project is a command-line flashcard application that implements the
SM-2 (SuperMemo 2) spaced repetition algorithm to optimize the scheduling
of card reviews. The goal is to help users memorize information efficiently
by showing cards at increasing intervals based on how well they remember each one.

### How it works

When a user reviews a card, they rate their recall from 0 (complete
blackout) to 5 (perfect response). The SM-2 algorithm then calculates
the next review date based on that rating, an easiness factor (EF), and
the number of successful repetitions. Cards answered correctly are shown
less frequently over time, while cards answered poorly are reset and shown
again the next day.

### Project structure

- `project.py` — Entry point. Contains `main()`, `add_card()`, `review()`,
  `get_quality()`, and `show_stats()`. Run with `add`, `review`, or `stats`
  as command-line arguments.
- `flashcard.py` — Defines the `Flashcard` dataclass with all SM-2 fields:
  `front`, `back`, `easiness`, `interval`, `repetitions`, and `next_review`.
- `deck.py` — Defines the `Deck` class, which handles loading and saving
  cards to a local `deck.json` file and filtering cards due for review today.
- `scheduler.py` — Implements the SM-2 algorithm in `update_card()`. It
  updates the easiness factor, interval, and next review date after each session.
- `test_project.py` — Unit tests using pytest, covering correct answers,
  wrong answers, invalid input, and the is_due logic.

### Design choices

The decision to separate the algorithm (`scheduler.py`) from the data model
(`flashcard.py`) and persistence (`deck.py`) makes each component independently
testable and easy to extend. Storing data as JSON instead of a database keeps
the project dependency-free and portable. The `next_review` field is stored as
an ISO date string so it survives serialization without any custom encoder.
EOF