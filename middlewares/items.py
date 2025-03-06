import scrapy

class AparatItem(scrapy.Item):
    title = scrapy.Field()          # عنوان ویدئو
    chanel = scrapy.Field()         # نام کانال پخش‌کننده
    views = scrapy.Field()          # تعداد بازدیدها
    upload_date = scrapy.Field()    # تاریخ آپلود ویدئو
    video_url = scrapy.Field()      # لینک ویدئو
    duration = scrapy.Field()       # مدت زمان ویدئو