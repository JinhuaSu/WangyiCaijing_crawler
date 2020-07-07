import scrapy
import pickle
import os
import ast
from urllib import parse
from scrapy.selector import Selector
import json
import requests
 

def get_rand():
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    
    # params 接收一个字典或者字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()

    response = requests.get("http://www.hljcredit.gov.cn/regController.do?getRandnum", headers = headers)
    
    # 查看响应内容，response.text 返回的是Unicode格式的数据
    x = json.loads(response.text.strip())
    if x['flag'] == 'true':
        return x
    else:
        print('fail to get randD')
        return {"flag":"true","randD":"9L3VMGK4CQ7873B7TJI5KZPT3A74BX"}
    


class UncreditSpider(scrapy.Spider):
    name = "Uncredit"
    def start_requests(self):
        total_page = 12711
        # total_page = 10

        headers = {
            'Cookie':'yfx_c_g_u_id_10006888=_ck20032823561110758413715353987; yfx_f_l_v_t_10006888=f_t_1585410971071__r_t_1585410971071__v_t_1585410971071__r_c_0; UM_distinctid=17121db9612ad6-0ec7fe709cb527-31760856-ff000-17121db9613ce3; CNZZDATA3688016=cnzz_eid%3D1930396560-1585409032-%26ntime%3D1585409032; membercenterjsessionid=MWViOWE2ZDktYmRlNC00NWMzLWFiMWUtNjQ3NWU0OGYzNTFl; wzws_cid=7187a7347902f0d7885c71d456e608136714b577f2ee24a43314ebd9d84b64b6f438b3bf396c3d7cf59f1f30cc019242417df6f600b6f2ee80692577b8f7754ab14524ba3008de665fdf770f7f231f9a; SHIROJSESSIONID=82f1243e-8bc8-4770-8f88-8438524086a6',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
        url_base = 'http://www.hljcredit.gov.cn/WebCreditQueryService.do?gssearch&type=sxbzxrqg&detail=true&sxbzxrmc=&randRe={0}&proselect=&cityselect=&disselect=&curPageNO={1}'
        for i in range(total_page):
            yield scrapy.Request(url=url_base.format(get_rand()['randD'],i+1),headers=headers, callback=self.parse)

    def parse(self,response):
        page_no = response.url.split('=')[-1]
        detail_page_links = []
        detail_base = 'http://www.hljcredit.gov.cn/WebCreditQueryService.do?sxbzxrQgDetail&dsname=hlj&dt=1&icautiouid={0}&srandRe={1}'
        for i,tr in enumerate(response.css('table.list_2_tab tr')[1:]):
            
            name = tr.css('td a::attr(title)').get()
            UID = tr.css('td a::attr(onclick)').get().split("'")[-2]
            url = detail_base.format(UID,get_rand()['randD'])
            detail_page_links.append(url)
            IdentityNum = tr.css('td')[-1].css('::text').get().strip()
        
            yield {
                'UID': UID,
                'name': name,
                'IdentityNum':IdentityNum,
                'url': url,
                'crawl state':'half',
                'pageNo':page_no,
                'No':i
            }
        try:
            yield from response.follow_all(detail_page_links, callback = self.parse_content)
        except:
            print(response.text)

    def parse_content(self, response):
        UID = response.url.split('&')[-2].split('=')[-1]
        doc_info_dict = {}
        tr_list = response.css('div.list.clearfix table.for_letter tr')
        for tr in tr_list:
            key = tr.css('td')[0].css('::text').get()
            value = tr.css('td')[1].css('::text').get()
            doc_info_dict[key] = value
        
        if len(doc_info_dict) > 0:
            return {
                'UID': UID,
                'doc_info_dict':doc_info_dict,
                'crawl state':'full'
            }
        else:
            return {
                'UID': UID,
                'crawl state':'empty'

            }
