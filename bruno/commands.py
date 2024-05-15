import json
from . import db
from bruno.database.models import Card
from flask.cli import with_appcontext
import click
import os


@click.command(name='populate_cards')
@with_appcontext
def populate_cards_command():
    file_path = os.path.join(os.path.dirname(
        __file__), 'database', 'initializations', 'cards.json')
    with open(file_path, 'r') as file:
        data = json.load(file)

    for card_data in data['cards']:
        card = Card(
            color=card_data['color'],
            value=card_data['value'],
            type=card_data['type'],
            frequency=card_data['frequency'],
        )
        db.session.add(card)

    db.session.commit()
