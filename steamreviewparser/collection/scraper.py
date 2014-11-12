from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.support.ui import Select


class ChromeScraper(object):

    def __init__(self):
        self.initialize()

    def initialize(self):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.browser = webdriver.Chrome()

    def quit(self):
        self.browser.quit()
        self.display.stop()

    @property
    def html(self):
        return self.browser.page_source.encode('utf-8')

    def get(self, url):
        self.browser.get(url)

    def select_dropdown_option(self, element, value):
        select = Select(element)
        select.select_by_value(value)
