import scrapy
import pickle
import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()
options.headless = True

class TianjinSpider(scrapy.Spider):
    name = "Tianjin"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
        
    def __init__(self):
        self.browser = webdriver.Firefox(options=options)
        self.browser.get('http://gk.tj.gov.cn/')
        super().__init__()
        
    def close(self,spider):
        self.browser.quit()

    def start_requests(self):
        total_page = 7516
        # total_page = 10
        url_base = 'http://gk.tj.gov.cn/govsearch/search.jsp?SType=1&page={0}'
        for i in range(total_page):
            req = scrapy.Request(url=url_base.format(str(i+1)), callback=self.parse)
            req.meta['dont_redirect'] = True
            req.meta['handle_httpstatus_list'] = [302]
            yield req

    def parse(self,response):
        detail_page_links = []
        for piece in response.css('div.index_right_content ul li'):
            href = piece.css('a::attr(href)').get()
            UID = href.split('/')[-1][:-6]
            if '?' not in UID:
                detail_page_links.append(href)
            date = piece.css('span.date3::text').get()
            if date and len(date) > 11:
                date = date[-11:].replace('年','-').replace('月','-').replace('日','')
            yield {
                'UID': UID,
                'title': piece.css('a::attr(title)').get(),
                'date2': piece.css('span.date2::text').get(),
                'date': date,
                'url': href,
                'crawl state':'half',
                'text length':0,
                'FileNumber':None,
            }
        for url in detail_page_links:
            req = scrapy.Request(url=url, callback=self.parse_content)
            req.meta['dont_redirect'] = True
            req.meta['handle_httpstatus_list'] = [302]
            yield  req

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-6]
        doc_info_dict = {}
        for line in response.css('table.table_key tr'):
            count = 0
            for td in line.css('td'):
                if count % 2 == 0:
                    key = td.css('*::text').get()
                else:
                    value = td.css('*::text').get()
                    doc_info_dict[key] = value
                count += 1
        FileNumber = ''
        if "文　　号：" in doc_info_dict.keys():
            FileNumber = doc_info_dict["文　　号："]
        paragraph_list = response.css('div.TRS_PreAppend p *::text').getall()
        attchment_list = response.css('div.article_content a::attr(href)').getall()
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
            'doc_info_dict': doc_info_dict,
            'mainText': paragraph_list,
            'attachment_link': attchment_list,
            'url':response.url,
            'FileNumber' :FileNumber,
            'crawl state':state,
            'text length':length,
        }

