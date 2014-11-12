from collection.parser import parse_game
from elasticsearch import Elasticsearch
import os

ES_URL = os.environ.get('STEAMREVIEWPARSER_DB_1_PORT')
es = Elasticsearch(ES_URL)


def add_game_data(game_id):
    reviews = parse_game(game_id)
    for review in reviews:
        es.index(index='steamreviews', doc_type='review',
                 id=review.get('id'), body=review)
