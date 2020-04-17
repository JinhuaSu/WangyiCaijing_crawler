import scrapy
import pickle
import os
import json

# from selenium import webdriver
# from selenium.webdriver.firefox.options import Options
# options = Options()
# options.headless = True
import random

def get_proxy():
    s = """58.218.92.78:5534
58.218.92.69:7747
58.218.92.75:7476
58.218.92.75:4365
58.218.92.75:2827
58.218.92.75:6485
58.218.92.72:2116
58.218.92.73:9468
58.218.92.75:6387
58.218.92.78:5215
58.218.92.78:9543
58.218.92.72:5049
58.218.92.69:8833
58.218.92.73:6617
58.218.92.73:7820
58.218.92.73:7205
58.218.92.73:9438
58.218.92.75:7360
58.218.92.78:8745"""
    ip_list = ['http://'+ ip for ip in s.split('\n')]
    return random.choice(ip_list)

class CentralSpider(scrapy.Spider):
    name = "Central"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    # def __init__(self):
    #     self.browser = webdriver.Firefox(options=options)
    #     self.browser.get('http://sousuo.gov.cn')
    #     super().__init__()
    # def close(self,spider):
    #     self.browser.quit()
    def start_requests(self):
        total_page = 2466
        total_page =  50
        url_base = 'http://sousuo.gov.cn/data?t=zhengcelibrary&q=&timetype=timeqb&mintime=&maxtime=&sort=pubtime&sortType=1&searchfield=title&pcodeJiguan=&childtype=&subchildtype=&tsbq=&pubtimeyear=&puborg=&pcodeYear=&pcodeNum=&filetype=&p={0}&n=5&inpro=&bmfl=&dup=&orpro='
        for i in range(total_page):
            req = scrapy.Request(url=url_base.format(i), callback=self.parse)
            req.meta['proxy'] = get_proxy()
            yield req

    def parse(self,response):
        detail_page_links = []
        for item in json.loads(response.text)['searchVO']['catMap']['gongbao']['listVO']:
            url = item['url']
            UID = url.split('/')[-1][:-4]
            item['UID'] = UID
            item['date'] = item['pubtimeStr'].replace('.','-')
            item['FileNumber'] = item['wenhao']
            item['crawl state'] = 'half'
            item['text length'] = 0 
            if '?' not in UID:
                detail_page_links.append(url)
            yield item
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-4]
        
        paragraph_list = response.css('div.pages_content p *::text').getall()        
        
        if len(paragraph_list) == 0:
            paragraph_list =  response.css('p *::text').getall() 
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
            
