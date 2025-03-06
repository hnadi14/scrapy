from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from scrapy import signals
from scrapy.http import HtmlResponse

class SeleniumMiddleware:
    def __init__(self):
        edge_options = Options()
        edge_options.use_chromium = True
        edge_options.add_argument("--headless")
        edgedriver_path = r"C:\Users\hn\Downloads\msgd\msedgedriver.exe"
        service = Service(executable_path=edgedriver_path)
        self.driver = webdriver.Edge(service=service)


    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        self.driver.get(request.url)
        body = str.encode(self.driver.page_source)
        return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)

    def spider_closed(self):
        self.driver.quit()