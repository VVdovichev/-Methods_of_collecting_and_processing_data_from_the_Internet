BOT_NAME = 'leroy_scraper'

SPIDER_MODULES = ['leroy_scraper.spiders']
NEWSPIDER_MODULE = 'leroy_scraper.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:66.0.2) Gecko/20100101 Firefox/66.0.2'

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    'Lesson_5.leroy_scraper.pipelines.LeroyDataScraperPipeline': 300,
    'Lesson_5.leroy_scraper.pipelines.LeroyImagesScraperPipeline': 150,
}

IMAGES_STORE = 'images'

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'
