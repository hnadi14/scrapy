import scrapy
from middlewares.items import AparatItem

class AparatSpider(scrapy.Spider):
    name = "aparat"
    allowed_domains = ["aparat.com"]
    start_urls = ["https://www.aparat.com/"]

    def parse(self, response):
        videos = response.css('div.grid-item')
        for video in videos:
            item = AparatItem()
            item['title'] = video.css('div.thumb-content > div.details > a > span::text').get(default='N/A').strip()
            item['chanel'] = video.css('div.channel-wrapper > a > span::text').get(default='N/A').strip()
            item['views'] = video.css('div.meta-data > span:nth-child(1)::text').get(default='N/A').strip()
            item['upload_date'] = video.css('div.meta-data > span:nth-child(2)::text').get(default='N/A').strip()
            item['video_url'] = video.css('div.details > a::attr(href)').get(default='N/A').strip()
            item['duration'] = video.css('div.sc-hiCibw.cbpBrw.poster.column.video > div > a > div.meta-data > span > span::text').get(default='N/A').strip()

            yield item

        # Follow next page
        next_page = response.css('a.next-page::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)