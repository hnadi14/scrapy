import random
import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from scrapy import signals
from scrapy.http import HtmlResponse

class RotateUserAgentMiddleware:
    def process_request(self, request, spider):
        user_agent = random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1',
        ])
        request.headers['User-Agent'] = user_agent

class SeleniumMiddlewareAparat:
    def __init__(self):
        edge_options = Options()
        edge_options.use_chromium = True
        # edge_options.add_argument("--headless")
        edge_options.add_argument("--log-level=3")
        edgedriver_path = r"C:\Users\hn\Downloads\msgd\msedgedriver.exe"
        service = Service(executable_path=edgedriver_path)
        self.driver = webdriver.Edge(service=service, options=edge_options)

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)
        return middleware

    def process_request(self, request, spider):
        if 'aparat.com' in request.url:
            self.driver.get(request.url)
            time.sleep(2)
            

            # انجام اسکرول 5 بار
            for _ in range(25):  # محدود کردن تعداد اسکرول به 5 بار
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)  # انتظار 1 ثانیه بین هر اسکرول

            body = str.encode(self.driver.page_source)
            return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)

    def spider_closed(self):
        self.driver.quit()