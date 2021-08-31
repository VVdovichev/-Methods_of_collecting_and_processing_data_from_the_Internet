from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from Lesson_5.scrapy_job import settings
from Lesson_5.scrapy_job.spiders.Job import JobScraperSpider


crawler_settings = Settings()
crawler_settings.setmodule(settings)
process = CrawlerProcess(settings=crawler_settings)
process.crawl(JobScraperSpider)
process.start()
