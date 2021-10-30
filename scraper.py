
import requests
import selenium
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from bs4 import BeautifulSoup #might not be useful

class Scraper(object):

    """ To open a web scraping session """

    def __init__(self,time_sleep, time_wait):

        """ open headless browser driver and initialize attributes """

        self.data_list = []
        self.time_sleep = time_sleep
        self.time_wait = time_wait
        self.url_list = []
        self.not_loaded_url = []
        self.ffx_options = selenium.webdriver.firefox.options.Options()
        self.ffx_options.add_argument('--headless')
        self.driver = selenium.webdriver.Firefox(options=self.ffx_options)

    def _scrap_html(self,soup):

        """ scrap html source code"""

        result_location = []
        result_condition = []
        result_language = []
        result_first_ed = []
        result_price = []
        result_num = []

        table = soup.findAll('div', attrs={'class': 'row no-gutters article-row'})


        for row in table:

            condition_dict = {
                'Mint': 7,
                'Near Mint': 6,
                'Excellent': 5,
                'Good': 4,
                'Light Played': 3,
                'Played': 2,
                'Poor': 1
            }

            try:

                str_location = row.find('span', {'class': 'icon d-flex has-content-centered mr-1'})['data-original-title']

            except KeyError:

                str_location = row.find('span', {'class': 'icon d-flex has-content-centered mr-1'})['title']

            product_attribute = row.find('div', {'class': 'product-attributes col'})
            str_condition = product_attribute.find('span', {'class': 'icon'})['data-original-title']
            str_language = product_attribute.find('span', {'class': 'icon mr-2'})['data-original-title']
            first_ed = product_attribute.find('span', {'class': 'icon st_SpecialIcon mr-1'})
            str_price = row.find('span', {'class': 'font-weight-bold color-primary small text-right text-nowrap'}).text.replace('.','').replace(',','.')
            str_num = row.find('span', {'class': 'item-count small text-right'}).text

            if first_ed==None:

                str_first_ed = ''

            else :

                str_first_ed = first_ed['data-original-title']

            result_location.append(str_location.replace('Item location: ',''))
            result_condition.append(condition_dict[str_condition])
            result_language.append(str_language)
            result_first_ed.append(str_first_ed)
            result_price.append(float(str_price[:-2]))
            result_num.append(int(str_num))

        return {
            'date': datetime.now(),
            'location': result_location,
            'condition': result_condition,
            'language': result_language,
            '1st_ed': result_first_ed,
            'price': result_price,
            'num_of_cards': result_num
            }

    def _scrap_url(self, url):

        """ web scraping the input """

        driver = self.driver
        self.url_list.append(url)
        driver.get(url)
        WebDriverWait(driver,4)

        while True:

            try:

                WebDriverWait(driver, self.time_wait).until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="spinner"]')))

                try:

                    WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.XPATH, '//button[@id="loadMoreButton"]'))).click()

                except:

                    break

            except selenium.common.exceptions.TimeoutException:

                self.not_loaded_url.append(url)
                break

        response = driver.page_source
        soup = BeautifulSoup(response, 'html.parser')       

        if  soup.html ==BeautifulSoup('<html><head></head><body></body></html>', 'html.parser').html:

            time.sleep(self.time_sleep)
            driver.get(url)
            response = driver.page_source
            soup = BeautifulSoup(response, 'html.parser')

        return self._scrap_html(soup)

    def scrap_url(self, url_list_in):

        """
        Web scrap each url
        """

        for url in url_list_in:

            self.data_list.append(self._scrap_url(url))

    def reload(self):

        """
        Rescrap the not loaded url list
        """

        idx_not_loaded = []
        not_loaded_url = self.not_loaded_url
        self.not_loaded_url = []

        for url in not_loaded_url:

            self.data_list[self.url_list.index(url)] = self._scrap_url(url)         

    def scrap_quit(self):

        """ close driver """

        self.driver.quit()

    # def test_url(self,url_list_in):

    #    """ test urls to verify database """

    #     for url in url_list_in:

    #         response = requests.get(url)
    #         soup = BeautifulSoup(response.text, 'html.parser')
    #         card_name = database_cardmarket.loc[database_cardmarket.index[cm_index],'url_name'].replace('-V-1','').replace('-V-2','').replace('-', ' ')

    #         if soup.title == None or not (card_name in soup.title.text.replace(' - ',' ').replace(',','').replace(':','').replace(',','').replace(';','').replace('.','').replace("'"," ").replace('"','').replace('(','').replace(')','').replace('-',' ').replace('@','').replace(' & ',' '):

    #             print(url)


