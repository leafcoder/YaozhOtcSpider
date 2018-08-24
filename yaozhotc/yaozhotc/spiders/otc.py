# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import parse_qsl, urlsplit, urlencode

from yaozhotc.items import YaozhotcItem

HEADNAMES = [
    '药品名称', '药品规格', '药品类型', 'OTC类别', '备注', '公告', '公告日期'
]
HEADERS = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'
}

PAGE_SIZE = 20
START_URL = 'https://db.yaozh.com/otc'

from scrapy import Selector

class OtcSpider(scrapy.Spider):
    name = 'otc'
    allowed_domains = ['db.yaozh.com']

    def start_requests(self):
        args = {}
        args['p'] = 1
        args['pageSize'] = PAGE_SIZE
        url = START_URL + '?' + urlencode(args)
        yield scrapy.Request(
            START_URL, headers=HEADERS, callback=self.parse
        )

    def parse(self, response):
        url = response.url
        self.log(url)
        max_page = response.css(
            'div[data-widget=dbPagination]::attr(data-max-page)'
        )
        max_page = int(max_page.extract_first())
        trs = response.css('table.table-striped tbody tr')
        for tr in trs:
            data = []
            title = tr.css('th::text').extract_first()
            tds = tr.css('td')
            data.append(title.strip())
            data.extend([td.css('::text').extract_first() for td in tds])
            row = dict(zip(HEADNAMES, data))
            item = YaozhotcItem()
            item['drug_name'] = row['药品名称']
            item['drug_size'] = row['药品规格']
            item['drug_type'] = row['药品类型']
            item['otc_type'] = row['OTC类别']
            item['remark'] = row['备注']
            item['notice'] = row['公告']
            item['notice_date'] = row['公告日期']
            yield item
        form = dict(parse_qsl(urlsplit(url).query))
        page = int(form.get('p', 1))
        page += 1
        if page <= max_page:
            args = {}
            args['p'] = page
            args['pageSize'] = PAGE_SIZE
            url = START_URL + '?' + urlencode(args)
            self.log(url)
            yield scrapy.Request(
                url, headers=HEADERS, callback=self.parse
            )