# Uncredit_crawler

**声明:爬取内容皆为政府对外公示文件，使用用途为学术研究。**

爬取信用黑龙江所有失信被执行人数据。
开发与运行系统:ubuntu18


技术栈:

- python3
- mongodb默认配置
- scrapy2.0
- pymongo


## quick start

```
```



## project log


**useful index**

scrapy shell -s USER_AGENT="Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0"

if contain ?, url must have ''.

next_page = response.urljoin(next_page)

>>> from scrapy.selector import Selector
>>> body = '<html><body><span>good</span></body></html>'
>>> Selector(text=body).xpath('//span/text()').get()

js escape编码 https://www.cnblogs.com/yoyoketang/p/8058873.html

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/60.0",
    'Referer': "http://service.shanghai.gov.cn/pagemore/iframePagerIndex_12344_2_22.html?objtype=&nodeid=&pagesize=&page=13"
}

