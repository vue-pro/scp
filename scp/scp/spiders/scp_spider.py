import scrapy

from scp.items import ScpItem


class DmozSpider(scrapy.Spider):
    name = "scp"
    allowed_domains = ["scp.org"]

    base_urls = "http://scp-wiki-cn.wikidot.com"
    start_urls = [
        'http://scp-wiki-cn.wikidot.com/scp-002'
    ]



    def parse(self, response):
        # scp 获取下一页
        next_page = response.xpath('//div[@class="footer-wikiwalk-nav"]/div/p/a/@href').extract()
        next_page_url = self.base_urls + next_page[1]
        yield scrapy.Request(next_page_url, callback=self.parse_dat, dont_filter=True)
        yield scrapy.Request(next_page_url, callback=self.parse, dont_filter=True)


        # for next_page_info in next_page:
        #
        #     print(next_page_url)
        #     yield scrapy.Request(next_page_url, callback=self.parse)
    def parse_dat(self, response):
        item = ScpItem()
        # scp标题
        page_title = response.xpath('//div[@id="page-title"]/text()').extract()
        for titleInfo in page_title:
            item['name'] = titleInfo.replace("\n", "").replace(" ", "")

        # scp 正文
        page_content_info = response.xpath('//div[@id="page-content"]')
        for contentInfo in page_content_info:
            page_content_string = contentInfo.xpath('//p/strong/text()').extract()
            page_content_p = contentInfo.xpath('//p/text()').extract()
            for page_content_string_info in page_content_string:
                for page_content_p_info in page_content_p:
                    item['content'] = page_content_string_info.replace("\n", "") + page_content_p_info.replace("\n", "")

        # scp 图片
        page_content_info = response.xpath('//div[@id="page-content"]')
        page_img = page_content_info.xpath('//div[@class="scp-image-block block-right"]/img/@src').extract()
        for page_img_info in page_img:
            item['imgs'] = page_img_info
        yield item