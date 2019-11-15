BOT_NAME = 'sina'

SPIDER_MODULES = ['sina.spiders']
NEWSPIDER_MODULE = 'sina.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
    'sina.pipelines.SinaPipeline': 300
}
