# -*- coding: utf-8 -*-
import unicodedata

import scrapy
import re
from datetime import datetime
from scrapy_redis.spiders import RedisSpider
from ..database.mysql_con import Mysql_Database


class ShuqugeSpider(RedisSpider):
    name = 'shuquge'
    allowed_domains = ['shuquge.com']
    # start_urls = ['http://www.shuquge.com/txt/5809/index.html']
    redis_key = 'shuquge:start_urls'

    def parse(self, response):
        self.handles_jianjie(response)
        all_div = response.xpath('/html/body/div[5]/dl/dd')
        for div in all_div:
            try:
                # print(div)
                # break
                xiaoshuo = {}
                xiaoshuo['zhangjie_index'] = div.xpath('./a/@href').extract_first().strip('.html')
                zhangjie = div.xpath('./a/text()').extract_first()
                # print(zhangjie)
                # zhangjie_1 = re.sub(r'\s+',',',zhangjie)
                # zhangjie_2 = zhangjie_1.split(',')
                # xiaoshuo['zhangjie_nub'] = zhangjie_2[-2]
                xiaoshuo['zhangjie_name'] = zhangjie
                # print(xiaoshuo)
                url = response.request.url
                zhangjie_url = re.sub(r'index',xiaoshuo['zhangjie_index'],url)
                # print(zhangjie_url)
                yield scrapy.Request(
                    # 发送请求的URL
                    url=zhangjie_url,
                    # dont_filter=True,
                    callback=self.handle_zhengwen,
                    errback=self.handle_err,
                    meta=xiaoshuo
                )
            except Exception as e:
                print('获取正文失败:',e)

    def handles_jianjie(self,response):
        '''获取简介'''
        try:
            jianjie = {}
            id = re.search(r".*?(\d{1,10}).*", response.request.url).group(1)
            jianjie['id'] = int(id)
            jianjie['书名'] = response.xpath('/html/body/div[4]/div[2]/h2/text()').extract_first()
            jianjie['作者'] = response.xpath('/html/body/div[4]/div[2]/div[2]/span[1]/text()').extract_first().split('：')[-1]
            jianjie['分类'] = response.xpath('//html/body/div[4]/div[2]/div[2]/span[2]/text()').extract_first().split('：')[-1]
            jianjie['状态'] = response.xpath('/html/body/div[4]/div[2]/div[2]/span[3]/text()').extract_first().split('：')[-1]
            num = response.xpath('/html/body/div[4]/div[2]/div[2]/span[4]/text()').extract_first().split('：')[-1]
            jianjie['字数'] = int(num)
            jianjie['更新时间'] = response.xpath('/html/body/div[4]/div[2]/div[2]/span[5]/text()').extract_first().strip('更新时间：')
            jianjie['简介'] = response.xpath('/html/body/div[4]/div[2]/div[3]/text()').extract()[1].strip('\n ')
            jianjie['封面'] = response.xpath('/html/body/div[4]/div[2]/div[1]/img/@src').extract_first()
        except Exception as e:
            print('获取简介失败:',e)
            return
        mysql_c = Mysql_Database()
        mysql_c.insert_data(**jianjie)
        # print('fffffff',jianjie)

    def handle_zhengwen(self,response):
        # print("请求")
        zhengwen_list = response.xpath('//*[@id="content"]/text()').extract()
        zhengwen_list[-3:-1] = []
        zhengwen_list.pop(-1)
        # print(zhengwen_list)
        #''.join(zhengwen_list)不行，有\xa0\r\n
        zhengwen = ''
        for i in zhengwen_list:
            j = re.sub(r'\s+','\n',i)
            # j = unicodedata.normalize('NFKC',i)
            zhengwen = zhengwen+j
        # print(zhengwen)
        # print(zhengwen_list)
        item = {}
        item['zhangjie_index'] = response.request.meta['zhangjie_index']
        # item['zhangjie_nub'] = response.request.meta['zhangjie_nub']
        item['zhangjie_name'] = response.request.meta['zhangjie_name']
        item['zhengwen'] = zhengwen
        item['shu_name'] = response.xpath('//*[@id="wrapper"]/div[4]/div[1]/div/a[2]/text()').extract_first()
        yield item

    def handle_err(self,failure):
        print('出错')