# -*- coding: utf-8 -*-

# Scrapy settings for shuquge_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'shuquge_spider'

SPIDER_MODULES = ['shuquge_spider.spiders']
NEWSPIDER_MODULE = 'shuquge_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'shuquge_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'shuquge_spider.middlewares.ShuqugeSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'shuquge_spider.middlewares.ShuqugeSpiderDownloaderMiddleware': 543,
    # 'shuquge_spider.middlewares.My_Proxy':400,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    # 'scrapy_redis.pipelines.RedisPipeline': 400,
    'shuquge_spider.pipelines.ShuqugeSpiderPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
# DOWNLOAD_DELAY = 0.1
#默认是180秒
DOWNLOAD_TIMEOUT = 5

#是否进行重试
RETRY_ENABLED = True
#重试的次数
RETRY_TIMES = 3

#不要清理Redis的队列，允许暂停/继续爬。
SCHEDULER_PERSIST = True

#使能Redis调度存储请求队列功能。
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

#确保所有蜘蛛通过redis共享相同的重复筛选器。
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

#指定主机和端口连接到Redis的（可选）时使用
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PARAMS = {
    'password': 'abc123456',
}

# 指定完整的Redis URL用于连接（可选）。
# 如果设置，它将优先于REDIS_HOST和REDIS_PORT设置。
#  REDIS_URL = 'redis：//用户：通过@主机名：9001'
# 使用其他编码UTF-8以外为redis的。
# # REDIS_ENCODING = 'latin1的'


