import re
from concurrent.futures.thread import ThreadPoolExecutor

import requests
from lxml import etree
from ..database.redis_con import Redis_database


class XiaoShuoUrl(object):
    def __init__(self,url,header):
        self.url = url
        self.header = header
        html = requests.get(url=url,headers=self.header)
        response = etree.HTML(html.text)
        self.all_div = response.xpath('//div[@class="nav"]/ul/li')
        self.url_list = []
        self.url_type = None
        self.start = None

    def page_type(self):
        '''
        获取各种类小说首页数据，调用page_url方法构造各页url
        :return:
        '''
        for i in self.all_div:
            page_type = i.xpath('./a/@href')[0]
            pattern = re.compile(r'(http.*?\d_)(\d)')
            page_type = pattern.findall(page_type)
            # print(page_type)
            if page_type:
                self.url_type = page_type[0][0] + page_type[0][1] + ".html"
                self.start = page_type[0][0]
                # print(url_type)
                self.page_url()


    def num_page(self):
        '''
        获取各种类小说总页数
        :return:
        '''
        url_type_html = requests.get(url=self.url_type, headers=self.header)
        url_type_response = etree.HTML(url_type_html.text)
        #最后一页
        # < a class ="a-btn" href="/category/1_1134.html" > 尾页 < / a >
        pattern = re.compile(r".*\d_(\d+).html")
        tail_n = url_type_response.xpath('//a[@class="a-btn"][last()]/@href')
        # print(tail_n)
        num = pattern.search(tail_n[0])
        print(num.group(1))
        return num.group(1)

    def page_url(self):
        '''
        调用num_page方法获取各种类小说总页数，构造各页url，并调用url_xiaoshuo方法获取每页的小说url
        :return:
        '''
        tail_page = self.num_page()
        # print(type(tail_page))
        # print(page_url)
        # 获取该页的所有小说url
        num = int(tail_page) + 1
        l = []
        for i in range(1, num):
            # print("第{}页".format(i))
            page_url = self.start + str(i) + ".html"
            l.append(page_url)
        with ThreadPoolExecutor(100) as executor:
            # {executor.submit(self.url_xiaoshuo,j):j for j in l}
            url_list = executor.map(self.url_xiaoshuo, l)
            # for u in url_list:
            #     print(u)
        # return url_list

    def url_xiaoshuo(self,l):
        '''
        获取该页的所有小说url
        '''
        global n
        url_type_html = requests.get(url=l, headers=self.header)
        # print(url_type_html.text)
        url_type_response = etree.HTML(url_type_html.text)
        url_type_all = url_type_response.xpath('//div[@class="l bd"]/ul/li')
        for j in url_type_all:
            # print(j)
            url = j.xpath('./span[@class="s2"]/a/@href')[0]
            # print(url)
            self.url_list.append(url)
            print(n)
            n += 1
        return

    def url_text(self):
        with open("url.text",'wa',encoding='utf-8') as f:
            for url in self.url_list:
                f.write(url+'\n')
        return

n = 0

if __name__=='__main__':
    # header = {
    #         "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    #         "Accept-Encoding":"gzip, deflate",
    #         "Accept-Language":"zh-CN,zh;q=0.9",
    #         "Cache-Control":"max-age=0",
    #         "Connection":"keep-alive",
    #         "Upgrade-Insecure-Requests":"1",
    #         "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"
    #     }
    # test = XiaoShuoUrl(url='http://www.shuquge.com',header=header)
    # test.page_type()
    # test.url_text()

    with open("url.text", 'r', encoding='utf-8') as f:
        url = f.readlines()
    r_c = Redis_database()
    for i in url:
        r_c.sava_urls(i)











