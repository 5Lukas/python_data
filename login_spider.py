import scrapy
from scrapy.http import FormRequest, Request
import json
from ecommerce_scraper.items import ProductItem

from urllib.parse import urlencode


class LoginSpider(scrapy.Spider):
    name = 'login_spider'
    start_urls = ['https://shopee.co.id/buyer/login']

    def parse(self, response):
        # 此处我们需要发送一个POST请求到登录API
        # 由于这是一个POST请求，我们使用urlencode来编码POST数据
        data = {
            'username': '(+62) 851 7341 3262',  # 请确保使用URL编码，如果用户名有特殊字符的话
            'password': '123123Xue',
            # 假设我们已经从某个地方获取了csrf_token
            'csrf_token': 'Q3hpwm3VyQEUFawUTIVBlIxQkXmdOqRl'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': '; '.join([
                'SPC_SI=0hfwZQAAAABWRUNHbWloTfvEOwAAAAAAcmMwOHNDQTQ=',
                'SPC_R_T_ID=xmB8EfHraGG6F+R9EQr+piaFETBRHJRGC6xxQUAXtNsy70jxYnRWmc6QXwdGo2dL43TafOJO4zS7hJ2FPcIL//vf+yvh3ub5H8+ViLG0Ii1NbyHsKMP/jD1h8Jc2gvHL84wNDl642pMWQj7iVgBrC/k9iG93bZdEvXohHdtD/Bk=',
                'SPC_R_T_IV=TWRoS2l2M01zQ1Bra0pSdw==',
                'SPC_T_ID=xmB8EfHraGG6F+R9EQr+piaFETBRHJRGC6xxQUAXtNsy70jxYnRWmc6QXwdGo2dL43TafOJO4zS7hJ2FPcIL//vf+yvh3ub5H8+ViLG0Ii1NbyHsKMP/jD1h8Jc2gvHL84wNDl642pMWQj7iVgBrC/k9iG93bZdEvXohHdtD/Bk=',
                'SPC_T_IV=TWRoS2l2M01zQ1Bra0pSdw==',
                'SPC_EC=.V1ZHWlJpQ2I1TGhHZXJjc+LZzsp7P255bLdr9c+jj7/UPIpcGzkxVtu9+BY8jmssh0xMQXJKwQN2AFY8TnhlY8RKiNlj67mmoGiW7a9x0eVh8Il562aSpWQluzTYTnziY+3OQGUAKpp1rtzJ+FhnGPsw43tXZoO913C5azsGhViq+EqAg+Q/lnfSYJD0WkctPH8WSCFjPksWilfP8XwYqQ==',
                'SPC_ST=.V1ZHWlJpQ2I1TGhHZXJjc+LZzsp7P255bLdr9c+jj7/UPIpcGzkxVtu9+BY8jmssh0xMQXJKwQN2AFY8TnhlY8RKiNlj67mmoGiW7a9x0eVh8Il562aSpWQluzTYTnziY+3OQGUAKpp1rtzJ+FhnGPsw43tXZoO913C5azsGhViq+EqAg+Q/lnfSYJD0WkctPH8WSCFjPksWilfP8XwYqQ=='
            ])
        }

        # 发送登录请求
        return [FormRequest(
            url='https://shopee.co.id/api/v4/account/basic/login_ivs',
            formdata=data,
            headers=headers,
            callback=self.after_login
        )]

    def parse_api(self, response):
        # 将响应的文本内容解析为JSON
        json_response = json.loads(response.text)

        # 循环遍历JSON中的每个项目
        for item_data in json_response['items']:
            # 创建ProductItem实例
            item = ProductItem()

            # 提取 'sold' 字段，并将其值赋给Item
            item['stock'] = item_data['stock']

            # 返回Item，由Scrapy进一步处理
            yield item

    def after_login(self, response):
        # 检查登录是否成功
        if response.status != 200 or '错误关键字' in response.text:
            self.logger.error('登录失败')
            return

        # 登录成功，继续抓取需要的数据
        self.logger.info('登录成功，开始抓取数据')
        # 这里替换成您想要抓取的页面URL
        yield scrapy.Request(
            url='https://shopee.co.id/api/v4/flash_sale/flash_sale_get_items?limit=16&need_personalize=true&offset=0&sort_soldout=true&tracker_info_version=1&with_dp_items=true',
            callback=self.parse_api
        )

    def parse_items(self, response):
        # 解析页面，提取商品信息等数据
        pass