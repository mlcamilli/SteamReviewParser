from scraper import ChromeScraper
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SteamClient(object):

    GAME_URL = 'http://store.steampowered.com/app/'

    def __init__(self):
        self.client = ChromeScraper()

    def get_game(self, game_id, pages=10):
        url = '{}{}'.format(self.GAME_URL, game_id)
        self.client.get(url)
        if 'agecheck' in self.client.browser.current_url:
            year_dropdown = self.client.browser.find_element_by_id('ageYear')
            self.client.select_dropdown_option(year_dropdown, "1960")
            submit = self.client.browser.find_element_by_class_name(
                'btnv6_blue_hoverfade')
            submit.click()

        for i in range(0, pages):
            try:
                button = WebDriverWait(self.client.browser, 10).until(
                    EC.presence_of_element_located(
                        (By.LINK_TEXT, 'Load More Reviews')
                    ))
                button.click()
            except TimeoutException:
                break

        return self.client.html

    def __enter__(self):
        self.client.initialize()
        return self

    def __exit__(self, type, value, traceback):
        self.client.quit()
