import requests


class SteamClient(object):
    GAME_URL = 'http://store.steampowered.com/app/'

    def _get(self, url, params={}):
        response = requests.get(url, params=params)
        try:
            response.raise_for_status()
        except Exception as e:
            raise e

        return response

    def get_game(self, game_id):
        url = '{}{}'.format(self.GAME_URL, game_id)
        return self._get(url)
