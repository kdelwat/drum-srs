# Anki decks for drumming

This repository is a work-in-progress attempt to generate [Anki](https://apps.ankiweb.net/) decks and use spaced repetition when practicing drumming.

The first available deck is based on "Stick Control for the Snare Drummer", and contains rudiments extracted from the book at various tempos.

## Usage

To import a deck straight into Anki, use the relevant `.apkg` file.

## Customising

To customise the cards (e.g. change the included tempos), edit the script `generate_deck.py`.

Run it with:

1. `pip install -r requirements.txt`
2. `python generate_deck.py`

## Legal note

This repository includes scans of the Stick Control book. The book's legal status is questionable, but since it was published in 1935 I don't see any real moral objections to doing so. For future decks involving newer books, the cards will reference pages and exercises without including the exercises themselves.
