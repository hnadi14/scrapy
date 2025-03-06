BOT_NAME = "middlewares"
SPIDER_MODULES = ["middlewares.spiders"]
NEWSPIDER_MODULE = "middlewares.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy
CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website
DOWNLOAD_DELAY = 1
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Disable cookies
COOKIES_ENABLED = False

# Enable HTTP Cache
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 86400
HTTPCACHE_DIR = "httpcache"

# Item pipelines
ITEM_PIPELINES = {
    'middlewares.pipelines.SQLitePipeline': 300,
}

# Downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    "middlewares.middlewares.RotateUserAgentMiddleware": 520,
    "middlewares.middlewares.SeleniumMiddlewareAparat": 530,
}

# Set settings whose default value is deprecated to a future-proof value
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"