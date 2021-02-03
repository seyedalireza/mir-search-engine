from selenium import webdriver
#from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
from fake_useragent import UserAgent
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException
import os
import time
import random


class Crawler(object):
    def __init__(self, link_file, number=50):
        self.links_file = link_file
        self.number = number
        with open(self.links_file, 'r') as file:
            self.links = file.read().split()
        self.user_agent = UserAgent()

        self.data = []
        self.browser = webdriver.Chrome(executable_path='./chromedriver')
        self.browser.set_page_load_timeout(40)
        # options.add_argument('user-agent='+self.user_agent.ff)
        self.ids = []
        print('here u go!')
        # self.browser = webdriver.Firefox(options=options)

    def _get_id(self, url: str):
        url = url[url.find('/paper/')+7:]
        paper_id = url[:url.find('/')]
        return paper_id

    def _get_data(self):
        paper_id = self._get_id(self.browser.current_url)
        if paper_id in self.ids:
            return
        self.ids.append(paper_id)
        time.sleep(5)
        year = self.browser.find_element_by_class_name('year').text
        title = self.browser.find_element_by_class_name('name').text
        authors_elements = self.browser.find_element_by_class_name('authors').find_elements_by_class_name('author')
        authors = [e.text for e in authors_elements if len(e.text)]
        ps = self.browser.find_elements_by_tag_name('p')
        abstract = None
        for p in ps:
            if not p.get_attribute('class'):
                abstract = p.text
                break
        references = []
        new_links = []
        try:
            references_elements = self.browser.find_elements_by_class_name('primary_paper')
        except:
            time.sleep(5)
            references_elements = self.browser.find_elements_by_class_name('primary_paper')
        for el in references_elements:
            try:
                a = el.find_element_by_tag_name('a').get_attribute('href')
                new_links.append(a)
                references.append(self._get_id(a))
            except:
                continue
        self.links.extend(new_links)
        self.data.append({
            'title': title,
            'authors': authors,
            'date': year,
            'id': paper_id,
            'references': references,
            'abstract': abstract
        })

    def _add_to_file(self):
        import json
        with open('outputfile.json', 'w') as file_out:
            json.dump(self.data, file_out)

    def get_all_data(self):
        while len(self.data) < self.number:
            print(len(self.data))
            links = self.links.copy()[:self.number-len(self.data)]
            self.links = []
            self._load_links(links)
        self._add_to_file()

    def _load_links(self, links):
        for link in links:
            self.browser.get(link)
            self._get_data()


crawler = Crawler('../data/start.txt', 5000)
crawler.get_all_data()
