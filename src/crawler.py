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
        self.pre = 'https://academic.microsoft.com/paper/'
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
        self.ids.append(paper_id)
        time.sleep(2)
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
                id_ = self._get_id(a)
                new_links.append(self.pre+id_+'/reference/')
                references.append(id_)
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
            links = self.links.copy()[:self.number-len(self.data)]
            self.links = []
            self._load_links(links)
            print(len(self.data))
        self._add_to_file()

    def _load_links(self, links):
        for link in links:
            paper_id = self._get_id(link)
            if paper_id in self.ids or 'paper' not in link:
                continue
            self.browser.get(link)
            try:
                self._get_data()
            except:
                time.sleep(5)
                try:
                    self._get_data()
                except:
                    continue


crawler = Crawler('../data/start.txt', 5000)
crawler.get_all_data()
