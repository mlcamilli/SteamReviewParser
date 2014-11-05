from bs4 import BeautifulSoup
from client import SteamClient
import re


def parse_game(game_id):
    reviews = []
    client = SteamClient()
    response = client.get_game(game_id)
    soup = BeautifulSoup(response.content)
    review_divs = soup.find(id='Reviews_all').div.find_all('div', 'review_box')
    for div in review_divs:
        positive = 'thumbsUp' in div.find('div', 'thumb').img.attrs.get('src')
        div_id = [div for div in div.find_all('div', recursive=False) if
                  'id' in div.attrs][0].attrs.get('id')

        numbers_text = div.find('div', 'header', recursive=False).text.strip()
        votes, total = [int(n) for n in re.findall(
            r"[\d]+ of [\d]+", numbers_text)[0].split(' of ')]

        reviews.append({'review': div.find('div', 'content').text.strip(),
                        'rating': 'positive' if positive else 'negative',
                        'id': div_id, 'votes': votes, 'total': total})

    return reviews
