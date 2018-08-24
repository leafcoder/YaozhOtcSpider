# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YaozhotcItem(scrapy.Item):
    # define the fields for your item here like:

    drug_name = scrapy.Field() # 药品名称
    drug_size = scrapy.Field() # 药品规格
    drug_type = scrapy.Field() # 药品类型
    otc_type = scrapy.Field() # OTC类别
    remark = scrapy.Field() # 备注
    notice = scrapy.Field() # 公告
    notice_date = scrapy.Field() # 公告日期