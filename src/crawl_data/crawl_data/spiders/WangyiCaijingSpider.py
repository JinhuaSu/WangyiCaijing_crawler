import scrapy
import pickle
import os
import ast
from urllib import parse
from scrapy.selector import Selector
import json
import requests
 


class WangyiCaijingSpider(scrapy.Spider):
    name = "WangyiCaijing"
    code_dict = {'000002': '万科Ａ',
                '000006': '深振业Ａ',
                '000011': '深物业A',
                '000014': '沙河股份',
                '000029': '深深房Ａ',
                '000031': '中粮地产',
                '000036': '华联控股',
                '000040': '宝安地产',
                '000042': '中洲控股',
                '000043': '中航地产',
                '000046': '泛海控股',
                '000056': '皇庭国际',
                '000402': '金 融 街',
                '000502': '绿景控股',
                '000505': '*ST珠江',
                '000514': '渝开发',
                '000517': '荣安地产',
                '000526': '紫光学大',
                '000534': '万泽股份',
                '000537': '广宇发展',
                '000540': '中天城投',
                '000558': '莱茵体育',
                '000567': '海德股份',
                '000573': '粤宏远Ａ',
                '000608': '阳光股份',
                '000609': '绵石投资',
                '000615': '京汉股份',
                '000616': '海航投资',
                '000620': '新华联',
                '000631': '顺发恒业',
                '000656': '金科股份',
                '000667': '美好集团',
                '000668': '荣丰控股',
                '000671': '阳光城',
                '000691': 'ST亚太',
                '000711': '京蓝科技',
                '000718': '苏宁环球',
                '000732': '泰禾集团',
                '000736': '中房地产',
                '000797': '中国武夷',
                '000838': '财信发展',
                '000863': '三湘股份',
                '000882': '华联股份',
                '000886': '海南高速',
                '000897': '津滨发展',
                '000918': '嘉凯城',
                '000926': '福星股份',
                '000965': '天保基建',
                '000979': '中弘股份',
                '000981': '银亿股份',
                '001979': '招商蛇口',
                '002016': '世荣兆业',
                '002077': '大港股份',
                '002113': '天润数娱',
                '002133': '广宇集团',
                '002146': '荣盛发展',
                '002147': '新光圆成',
                '002208': '合肥城建',
                '002244': '滨江集团',
                '002285': '世联行',
                '002305': '南国置业',
                '002314': '南山控股',
                '200160': '南江B',
                '200168': '舜喆B',
                '600007': '中国国贸',
                '600048': '保利地产',
                '600052': '浙江广厦',
                '600053': '九鼎投资',
                '600064': '南京高科',
                '600067': '冠城大通',
                '600077': '宋都股份',
                '600094': '大名城',
                '600158': '中体产业',
                '600159': '大龙地产',
                '600162': '香江控股',
                '600173': '卧龙地产',
                '600177': '雅戈尔',
                '600185': '格力地产',
                '600208': '新湖中宝',
                '600215': '长春经开',
                '600223': '鲁商置业',
                '600225': '天津松江',
                '600239': '云南城投',
                '600240': '华业资本',
                '600246': '万通地产',
                '600266': '北京城建',
                '600322': '天房发展',
                '600325': '华发股份',
                '600340': '华夏幸福',
                '600376': '首开股份',
                '600383': '金地集团',
                '600393': '粤泰股份',
                '600466': '蓝光发展',
                '600503': '华丽家族',
                '600510': '黑牡丹',
                '600533': '栖霞建设',
                '600555': '海航创新',
                '600565': '迪马股份',
                '600604': '市北高新',
                '600606': '绿地控股',
                '600621': '华鑫股份',
                '600622': '嘉宝集团',
                '600638': '新黄浦',
                '600639': '浦东金桥',
                '600641': '万业企业',
                '600649': '城投控股',
                '600657': '信达地产',
                '600658': '电子城',
                '600663': '陆家嘴',
                '600665': '天地源',
                '600675': '*ST中企',
                '600683': '京投发展',
                '600684': '珠江实业',
                '600696': '匹凸匹',
                '600708': '光明地产',
                '600716': '凤凰股份',
                '600724': '宁波富达',
                '600730': '中国高科',
                '600732': '*ST新梅',
                '600733': 'S前锋',
                '600736': '苏州高新',
                '600743': '华远地产',
                '600748': '上实发展',
                '600773': '西藏城投',
                '600791': '京能置业',
                '600807': '天业股份',
                '600823': '世茂股份',
                '600848': '上海临港',
                '600890': '中房股份',
                '601155': '新城控股',
                '601588': '北辰实业',
                '900957': '凌云Ｂ股'}
    def start_requests(self):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        url_base = 'http://quotes.money.163.com/f10/gsxw_{0},{1}.html'
        for code in self.code_dict.keys():
            try:
                res = requests.get(url_base.format(code,0),headers=headers)
                selector = Selector(text=res.text,type='html')
                total_page = selector.css('div.mod_pages a')[-2].css('a::text').get()
                total_page = int(total_page)
            except:
                total_page = 1
            for i in range(total_page):
                yield scrapy.Request(url=url_base.format(code,i),headers=headers, callback=self.parse)

    def parse(self,response):
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        page_no = response.url.split('.htm')[0].split(',')[-1]
        code = response.url.split('.htm')[0].split(',')[-2].split('_')[-1]
        stock_name = self.code_dict[code]
        detail_page_links = []
        for i,tr in enumerate(response.css('div.tabs_panel table tr')[1:]):
            title = tr.css('td.td_text a::text').get()
            date = tr.css('td.align_c::text').get()
            url = tr.css('td.td_text a::attr(href)').get()
            UID = url.split('.htm')[-2].split('/')[-1]
            detail_page_links.append(url)
            yield {
                'UID': UID,
                'code':code,
                'title': title,
                'date':date,
                'url': url,
                'crawl state':'half',
                'pageNo':page_no,
                'No':i
            }
            yield scrapy.Request(url=url,headers=headers, callback=self.parse_content)

    def parse_content(self, response):
        UID = response.url.split('.htm')[-2].split('/')[-1]
        title_detail = response.css('div.post_content_main h1::text').get()
        time = response.css('div.post_content_main div.post_time_source::text').get()
        source = response.css('div.post_content_main div.post_time_source a#ne_article_source::text').get()
        try:
            time = time.strip().split('\u3000')[0]
        except:
            print('no time')
        content = '\n'.join(response.css('div.post_text p *::text').getall())
        
        if len(content) > 0:
            return {
                'UID': UID,
                'title_detail':title_detail,
                'time':time,
                'source':source,
                'content':content,
                'crawl state':'full'
            }
        else:
            return {
                'UID': UID,
                'title_detail':title_detail,
                'time':time,
                'source':source,
                'content':content,
                'crawl state':'empty'
            }
