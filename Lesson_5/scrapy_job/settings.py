BOT_NAME = 'scrapy_job'

SPIDER_MODULES = ['scrapy_job.spiders']
NEWSPIDER_MODULE = 'scrapy_job.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:66.0.2) Gecko/20100101 Firefox/66.0.2'

ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    'scrapy_job.pipelines.ScrapyJobPipeline': 300,
}

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'
