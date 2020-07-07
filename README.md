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


**test_url**

http://www.hljcredit.gov.cn/regController.do?getRandnum


http://www.hljcredit.gov.cn/WebCreditQueryService.do?gssearch&type=sxbzxrqg&detail=true&sxbzxrmc=&randRe=4CT64LX32IBGAJRBOTWM53Z4093OTS&proselect=&cityselect=&disselect=&curPageNO=5


http://www.hljcredit.gov.cn/WebCreditQueryService.do?sxbzxrQgDetail&dsname=hlj&dt=1&icautiouid=1230610016740648359&srandRe=3366X354121UO1UFVQG5WWXNAX9296


**MenuPage**

total page 12711

total detail num 127109

```
In [5]: response.css('table.list_2_tab tr')[1:][2].css('td a::attr(title)').get()                                                                                                 
Out[5]: '管晨君'

In [6]: response.css('table.list_2_tab tr')[1:][2].css('*::text').getall()                                                                                                        
Out[6]: 
['\r\n\t\t\t\t',
 '3',
 '\r\n\t\t\t\t',
 '\t\t\t\t\t\r\n\t\t\t\t\t',
 '\t\r\n\t\t\t\t\t\t管晨君\r\n\t\t\t\t\t',
 '\r\n\t\t\t\t',
 '\r\n\t\t\t\t',
 '\r\n\t\t\t\t\t310108******** 2844\r\n\t\t\t\t',
 '\t\t\t\t\t\t\t\t\r\n\t\t\t']

In [7]: response.css('table.list_2_tab tr')[1:][2].css('td a::attr(onclick)').get()                                                                                               
Out[7]: "godetail('1230610016705675444');"

In [8]: response.css('table.list_2_tab tr')[1:][2].css('td a::attr(onclick)').get().split("'")[-2]                                                                                
Out[8]: '1230610016705675444'

In [9]: response.css('table.list_2_tab tr')[1:][2].css('td')[-1].get()                                                                                                            
Out[9]: '<td style="text-align:center;">\r\n\t\t\t\t\t310108******** 2844\r\n\t\t\t\t</td>'

In [10]: response.css('table.list_2_tab tr')[1:][2].css('td')[-1].css('::text').get()                                                                                             
Out[10]: '\r\n\t\t\t\t\t310108******** 2844\r\n\t\t\t\t'

In [11]: response.css('table.list_2_tab tr')[1:][2].css('td')[-1].css('::text').get().strip()                                                                                     
Out[11]: '310108******** 2844'
```

**JS**

```
function toPage(num1) {
    var action=$("#myform");
    $.ajax("regController.do?getRandnum",{
        data:{},
        dataType:'json',//服务器返回json格式数据
        type:'post',//HTTP请求类型
        success:function(data){
            if(data.flag==true || data.flag=="true"){
                randRe = data.randD;
                var url = action.attr("action");
                url = url+'&randRe='+randRe;
                action.attr('action',url); 
            }
            $("#param2").val(parent.$("#xktyshxydm").val());
            $("#param3").val(parent.$("#proselect").val());	
            $("#param5").val(parent.$("#cityselect").val());
            $("#param6").val(parent.$("#disselect").val());
            var currpage=$("#curPageNO").val();
            currpage=parseInt(currpage);
            var pageCount=$("#pageCount").val();
            pageCount=parseInt(pageCount);
            if(num1=='1') {
                $("#param4").val("1");
                action.submit();
            }else if(num1=='2') {
                if(currpage>1) {
                    currpage=currpage-1;
                    $("#param4").val(currpage);
                    action.submit();
                }
                
            }else if(num1=='3') {
                if(currpage<pageCount) {
                    currpage=currpage+1;
                    $("#param4").val(currpage);
                    action.submit();
                }
            }else if(num1=='4') {
                $("#param4").val(pageCount);
                action.submit();
            }else if(num1=='5') {
                var govalue=$.trim($("#govalue").val());
                if(govalue=="") {
                    alert("请输入有效的页数");
                    return;
                }
                if(isNaN(govalue)||parseInt(govalue)<1||parseInt(govalue)>pageCount) {
                    alert("请输入有效的页数");
                    return;
                }
                $("#param4").val(govalue);
                action.submit();
            }
        }
});
}
function godetail(id){
    var url = "WebCreditQueryService.do?sxbzxrQgDetail&dsname=hlj&dt=1&icautiouid="+id;
    $.ajax("regController.do?getRandnum",{
        data:{},
        dataType:'json',//服务器返回json格式数据
        type:'post',//HTTP请求类型
        success:function(data){
            if(data.flag==true || data.flag=="true"){
                randRe = data.randD;
                url = url+'&srandRe='+randRe;
                var cz=document.getElementById("openwin");
                if(cz!=""&&cz!=null&&typeof(cz)!="undefined") {
                    document.body.removeChild(cz); 
                }
                var a = document.createElement("a");
                a.setAttribute("href", url);
                a.setAttribute("target", "_blank");
                a.setAttribute("id", "openwin");
                document.body.appendChild(a);
                a.click();
            }
        }
    });

}
```

**detail page**

```
In [5]: response.css('div.list.clearfix table.for_letter tr')[0].css('td')[0].css('::text').get()                                                                                 
Out[5]: '案号：'

In [6]: response.css('div.list.clearfix table.for_letter tr')[0].css('td')[1].css('::text').get()                                                                                 
Out[6]: '\xa0\xa0(2018)甘0302执恢59号'
```


