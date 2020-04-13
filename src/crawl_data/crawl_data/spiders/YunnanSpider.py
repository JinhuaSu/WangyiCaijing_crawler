import scrapy
import pickle
import os
import ast
from urllib import parse
from scrapy.selector import Selector

class YunnanSpider(scrapy.Spider):
    name = "Yunnan"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    def start_requests(self):
        total_page = 27
        # total_page = 3 
        url_base = 'http://www.yn.gov.cn/zwgk/zcwj/zxwj/index{0}.html'
        for i in range(total_page):
            page = '_'+ str(i) if i > 0 else ''
            yield scrapy.Request(url=url_base.format(page), callback=self.parse)

    def parse(self,response):
        detail_page_links = []
        for ul in response.css('ul.zclist'):
            url = response.urljoin(ul.css('li')[1].css("a::attr(href)").get())
            UID = url.split('/')[-1][:-5]
            if '?' not in UID:
                detail_page_links.append(url)
            date = ul.css('li')[2].css("::text").get()
            if date and len(date) > 10:
                date = date[:10]
            yield {
                'UID': UID,
                'title': ul.css('li')[1].css("::text").get(),
                'date': date,
                'FileNumber':ul.css('li')[0].css("::text").get(),
                'url': url,
                'text length':0,
                'crawl state':'half'
            }
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-5]
        paragraph_list =  response.css('div.view p *::text').getall() 
        length = len(''.join(paragraph_list))
        if length > 0:
            state = 'full'
            with open('../../data/HTML_pk/%s/%s.pkl' % (self.name,UID), 'wb') as f:
                pickle.dump(response.text,f)
            with open('../../data/text/%s/%s.txt' % (self.name,UID), 'w') as f:
                f.write('\n'.join(paragraph_list))
        else:
            state = 'empty'
        return {
            'UID': UID,
            'mainText': paragraph_list,
            'crawl state':state,
            'text length':length,
        }
