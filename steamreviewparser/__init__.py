from collection.parser import parse_game
from elasticsearch import Elasticsearch
import os
import collections

ES_URL = os.environ.get('STEAMREVIEWPARSER_DB_1_PORT')
es = Elasticsearch(ES_URL)
TEST_GAMES = [295270, 250900, 730, 220, 241600, 317620, 4000, 252490,
              220200, 550, 8930, 620, 265930, 233450, 211820]


def nested_dict():
    """
    Credit to Cam and company
    """
    nested_dict = lambda: collections.defaultdict(nested_dict)
    return nested_dict()


def add_game_data(game_id):
    reviews = parse_game(game_id)
    for review in reviews:
        es.index(index='steamreviews', doc_type='review',
                 id=review.get('id'), body=review)


def get_reviews(game_name, must=None, must_not=None, rating=None):
    query = nested_dict()
    query['query']['filtered']['query']['bool']['must'] = []
    query['query']['filtered']['query']['bool']['must_not'] = []
    query['query']['filtered']['query']['bool']['must'].append(
        {'match_phrase': {'game_name': game_name}})

    if must:
        query['query']['filtered']['query']['bool']['must'].append(must)
    if must_not:
        query['query']['filtered']['query']['bool']['must_not'].append(
            must_not)
    if rating:
        query['query']['filtered']['query']['bool']['must'].append(
            {'match_phrase': {'rating': rating}})
    data = es.search(index='steamreviews', doc_type='review',
                     body=query, size=20)
    results = data.get('hits').get('hits')
    offset = 20
    while(len(results) != data.get('hits').get('total')):
        data = es.search(index='steamreviews', doc_type='review',
                         body=query, size=20, from_=offset)
        results.extend(data.get('hits').get('hits'))
        offset += 20

    return results


def set_mapping_and_index():
    es.indices.create('steamreviews')
    mapping = {
        'review': {
            'properties': {
                "game_name": {"type": "string", "index": "not_analyzed"},
            }
        }
    }
    es.indices.put_mapping(index='steamreviews', doc_type='review',
                           body=mapping)


def get_games():
    body = nested_dict()
    body['aggs']['names']['terms']['field'] = 'game_name'
    data = es.search(index='steamreviews', doc_type='review', body=body)
    return [name['key'] for name in data['aggregations']['names']['buckets']]


def weird_words(game_name=None):
    body = nested_dict()
    body['aggs']['rating']['terms']['field'] = 'rating'
    body['aggs']['rating']['aggs']['weird']['significant_terms']['field'] = 'review'
    data = es.search(index='steamreviews', doc_type='review', body=body)
    results = {'positive' : [], 'negative': []}
    for bucket in data['aggregations']['rating']['buckets']:
        results[bucket['key']].extend([weird['key'] for weird in bucket['weird']['buckets']])
    return results
