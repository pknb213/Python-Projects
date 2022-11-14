import motor.motor_asyncio
import requests
import asyncio
import base64
from abc import ABCMeta, abstractmethod
from lxml import html
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

GOOGLE_TEMP_IMG = "//lh3.googleusercontent.com/AN8gkA6tFRLbkOs2RBfC8zCY3cHKEb2GD9kVURQJM3pKyNqv-kWP8-iHD1PdryPWfVc=w600-h600"


class AbstractEcommerce(metaclass=ABCMeta):
    host = "localhost"
    port = 27017
    client = motor.motor_asyncio.AsyncIOMotorClient(host, port)

    @abstractmethod
    async def main(self):
        pass

    @abstractmethod
    async def extract(self, _url):
        pass


class Gmarket(AbstractEcommerce):
    def __init__(self):
        self.url = "https://m.gmarket.co.kr/n/superdeal?categoryCode=400000{}&categoryLevel=1"
        self.category_id = [135,136,137,139,140,143,146,148,149,151,152,174]
        self.image_xpath = '//div[@class="box-product"]/span[@class="box-product__img-product"]/img/@data-src'
        self.price_xpath = '//div[@class="box__itemcard--price"]/span[@class="text__item--title"]/span/..'
        self.title_xpath = '//div[@class="box-product"]/span[@class="box-product__img-product"]/img/@alt'
        self.url_xpath = '//div[@class="box__itemcard-superdeal--img"]/a/@href'

    async def main(self):
        return await asyncio.gather(*[self.extract(self.url.format(str(i))) for i in self.category_id])

    async def extract(self, _url):
        with requests.Session() as s:
            try:
                req = s.get(_url, verify=False)
                html_tree = html.fromstring(req.content)

                img = html_tree.xpath(self.image_xpath)
                img = [v if v[:7] == "//image" else GOOGLE_TEMP_IMG for v in img]
                price = html_tree.xpath(self.price_xpath)
                price = [v for v in price if v != " "]
                title = html_tree.xpath(self.title_xpath)
                url_info = html_tree.xpath(self.url_xpath)
                print(len(img), len(price), len(title), len(url_info))
                res = [{
                    "title": title[i],
                    "price": price[i].text_content(),
                    "url": url_info[i],
                    "img": base64.b64encode(urlopen("http:" + img[i]).read()).decode('ascii')
                } for i in range(len(title))]
                print(title, price)  # Debug
            except Exception as e:
                print(">>>>", e, _url)
                res = []
            return res

    async def insert(self, _dic):
        return await self.client["shop_db"]["gmarket"].insert_many(_dic[:1000])


class Gsshop(AbstractEcommerce):
    def __init__(self):
        self.url = "https://www.gsshop.com/shop/sect/sectL.gs?sectid=1378{}#0_popular_{}"
        self.category_id = [773,781,794]
        self.page_num = [1,2,3,4,5,6]
        # Section Tag is Dynamic Table
        self.image_xpath = "//section[@id='prd-list']/ul/li/a[@class='prd-item']/div[@class='prd-img']/img/@src"
        self.price_xpath = "//section[@id='prd-list']/ul/li/a[@class='prd-item']/dl[@class='prd-info']/dd[@class='price-info']/span[@class='price']/span[@class='set-price']/strong/text()"
        self.title_xpath = "//section[@id='prd-list']/ul/li/a[@class='prd-item']/dl[@class='prd-info']/dt[@class='prd-name']"
        self.url_xpath = "//section[@id='prd-list']/ul/li/a[@class='prd-item']/@href"
        self.dynamic_xpath = "//section[@id='prd-list']/ul/li/a[@class='prd-item']"
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(executable_path="./chromedriver.exe",
                                       options=options)

    def __del__(self):
        self.driver.close()

    async def main(self):
        return await asyncio.gather(*[self.extract(self.url.format(str(i), str(j))) for i in self.category_id for j in self.page_num])

    async def extract(self, _url):
        try:
            self.driver.get(_url)
            WebDriverWait(self.driver, 3).until(EC.presence_of_all_elements_located((By.XPATH, self.dynamic_xpath)))
            html_tree = html.fromstring(self.driver.page_source)
            img = html_tree.xpath(self.image_xpath)
            price = html_tree.xpath(self.price_xpath)
            title = html_tree.xpath(self.title_xpath)
            title = [str(i.text_content()).strip() for i in title]
            url_info = html_tree.xpath(self.url_xpath)
            print(len(img), len(price), len(title), len(url_info))
            res = [{
                "title": title[i],
                "price": price[i],
                "url": url_info[i],
                "img": base64.b64encode(urlopen("http:" + img[i]).read()).decode('ascii')
            } for i in range(len(title))]
            print(res)  # Debug
        except Exception as e:
            print(">>>>", e, _url)
            res = []
        return res

    async def insert(self, _dic):
        return await self.client["shop_db"]["gsshop"].insert_many(_dic[:1000])