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
        total_page = 3
        url_base = 'http://www.shanghai.gov.cn/nw2/nw2314/nw2319/nw12344/index{0}.html'
        for i in range(total_page):
            page = str(i) if i > 0 else ''
            yield scrapy.Request(url=url_base.format(page), callback=self.parse)

    def parse(self,response):
        detail_page_links = []
        for piece in response.css('ul.pageList li'):
            href = piece.css('a::attr(href)').get()
            UID = href.split('/')[-1][:-5]
            detail_page_links.append(href)
            yield {
                'UID': UID,
                'title': piece.css('a::attr(title)').get(),
                'date': piece.css('span::text').get(),
                'href': href,
                'crawl state':'half'
            }
        yield from response.follow_all(detail_page_links, callback = self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('/')[-1][:-5]
        with open('../../data/HTML_pk/%s/%s.pkl' % (self.name,UID), 'wb') as f:
            pickle.dump(response.text,f)
        doc_info_dict = {}
        doc_info_dict['relative_doc_titles'] = response.css('ul.nowrapli li a::attr(title)').getall()
        doc_info_dict['relative_doc_links'] = response.css('ul.nowrapli li a::attr(href)').getall()
        paragraph_list = response.css('div#ivs_content p::text').getall()
        with open('../../data/text/%s/%s.txt' % (self.name,UID), 'w') as f:
            f.write('\n'.join(paragraph_list))
        return {
            'UID': UID,
            'doc_info_dict': doc_info_dict,
            'mainText': paragraph_list,
            'crawl state':'full',
        }

