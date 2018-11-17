import scrapy
from scrapy.selector import HtmlXPathSelector

class DmozSpider(scrapy.Spider):
    name = "scp"
    allowed_domains = ["scp.org"]
    start_urls = [
        "http://scp-wiki-cn.wikidot.com/scp-cn-001",
        "http://scp-wiki-cn.wikidot.com/scp-cn-002"
    ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        a_page = hxs.xpath('//div[@id="page-title"]')
        for pages in a_page:
            title = pages.xpath('text()').extract()
            for s in title:
                print s.encode('utf8')


        pagecontent = hxs.xpath('//div[@id="page-content"]/div')
        for contents in pagecontent:
            p_content_title = contents.xpath('p/strong/text()').extract()
            p_contents = contents.xpath('p/text()').extract()

            for content_title in p_content_title:
                print content_title.encode('utf8')

            for content in p_contents:
                print content.encode('utf8')



            # for s in p_content_title:
            #     print s.encode('utf8')
            #
            # for cs in p_contents:
            #     print cs.encode('utf8')


        # filename = response.url.split("/")[-2]
        # with open(filename, 'wb') as f:
        #     f.write(a_page)
