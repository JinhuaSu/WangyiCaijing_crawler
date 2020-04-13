import scrapy
import pickle
import os

class ShanghaiSpider(scrapy.Spider):
    name = "Shanghai"
    if not os.path.exists('../../data/HTML_pk/%s' % name):
        os.makedirs('../../data/HTML_pk/%s' % name)
    if not os.path.exists('../../data/text/%s' % name):
        os.makedirs('../../data/text/%s' % name)
    def start_requests(self):
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0",
            'Referer': "http://service.shanghai.gov.cn/pagemore/iframePagerIndex_12344_2_22.html?objtype=&nodeid=&pagesize=&page=13"
        }
        total_page = 1305
        #url_base = 'http://www.shanghai.gov.cn/nw2/nw2314/nw2319/nw12344/index{0}.html'
        url_base = 'http://service.shanghai.gov.cn/pagemore/iframePagerIndex_12344_2_22.html?objtype=&nodeid=&pagesize=&page={0}'
        for i in range(total_page):
            yield scrapy.Request(url=url_base.format(str(i+1)),headers=headers, callback=self.parse)

    def parse(self,response):
        detail_page_links = []
        for piece in response.css('ul.pageList li'):
            href = piece.css('a::attr(href)').get()
            UID = href.split('/')[-1][:-5]
            if '?' not in UID:
                detail_page_links.append(href)
            date = piece.css('span::text').get()
            if date and len(date) > 3:
                date = date.replace('.','-')
            yield {
                'UID': UID,
                'title': piece.css('a::attr(title)').get(),
                'date': date,
                'href': href,
                'text length':0,
                'crawl state':'half',
                'FileNumber':None,
            }
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-5]
        doc_info_dict = {}
        doc_info_dict['relative_doc_titles'] = response.css('ul.nowrapli li a::attr(title)').getall()
        doc_info_dict['relative_doc_links'] = response.css('ul.nowrapli li a::attr(href)').getall()
        paragraph_list = response.css('div#ivs_content p::text').getall()
        Filenum = None
        if len(paragraph_list) > 0 and '号' in paragraph_list[0]:
            Filenum = paragraph_list[0]
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
            'url':response.url,
            'mainText': paragraph_list,
            'FileNumber':Filenum,
            'crawl state':state,
            'text length':length,
        }

