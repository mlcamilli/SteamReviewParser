from scraper import ChromeScraper
from selenium.common.exceptions import NoSuchElementException


class SteamClient(object):

    GAME_URL = 'http://store.steampowered.com/app/'

    def __init__(self):
        self.client = ChromeScraper()
        self.client.browser.implicitly_wait(3)

    def get_game(self, game_id, pages=3):
        url = '{}{}'.format(self.GAME_URL, game_id)
        self.client.get(url)
        if 'agecheck' in self.client.browser.current_url:
            year_dropdown = self.client.find_element_by_id('ageYear')
            self.select_dropdown_option(year_dropdown, "1960")
            submit = self.client.browser.find_element_by_class_name(
                'btnv6_blue_hoverfade')
            submit.click()

        for i in range(0, pages):
            try:
                self.client.browser.find_element_by_class_name(
                    'btnv6_blue_blue_innerfade').click()
            except NoSuchElementException:
                break

        return self.client.html

    def __enter__(self):
        self.client.initialize()
        return self

    def __exit__(self, type, value, traceback):
        self.client.quit()
