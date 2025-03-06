import scrapy

class AparatSpider(scrapy.Spider):
    name = "aparat_spider"
    allowed_domains = ["aparat.com"]
    start_urls = ["https://www.aparat.com/"]

    def parse(self, response):
        # استخراج اطلاعات ویدئوها
        videos = response.css('div.video-box')
        for video in videos:
            title = video.css('h3.title::text').get()
            views = video.css('span.view-couXRnt::text').get()
            upload_date = video.css('span.upload-date::text').get()
            video_url = video.css('a.video-thumb::attr(href)').get()

            yield {
                'title': title,
                'views': views,
                'upload_date': upload_date,
                'video_url': video_url,
            }