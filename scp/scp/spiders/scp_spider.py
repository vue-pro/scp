import scrapy
from scrapy.selector import HtmlXPathSelector

from scp.items import ScpItem


class DmozSpider(scrapy.Spider):
    name = "scp"
    allowed_domains = ["scp.org"]

    start_urls = [
        # "http://scp-wiki-cn.wikidot.com/scp-cn-001",
        # "http://scp-wiki-cn.wikidot.com/scp-cn-002"
    ]

    url_lens = ""
    i = 1
    while i < 20:
        if len(str(i)) == 1:
            url_lens = "00" + str(i)
        elif len(str(i)) == 2:
            url_lens = "0" + str(i)
        elif len(str(i)) == 3:
            url_lens = str(i);
        start_urls.append('http://scp-wiki-cn.wikidot.com/scp-cn-'+ url_lens)
        i = i + 1


    def parse(self, response):

        hxs = HtmlXPathSelector(response)
        a_page = hxs.xpath('//div[@id="page-title"]')
        for pages in a_page:
            title = pages.xpath('text()').extract()
            for s in title:
                print s.encode('utf8').replace(" ","")
                # item = ScpItem()
                #
                # item['name'] = s.encode('utf8')
                # item['content'] = s.encode('utf8')
                # item['imgs'] = s.encode('utf8')
                #
                # yield item


        # pagecontent = hxs.xpath('//div[@id="page-content"]/div')
        # for contents in pagecontent:
        #     p_content_title = contents.xpath('p/strong/text()').extract()
        #     p_contents = contents.xpath('p/text()').extract()
        #
        #     for content_title in p_content_title:
        #         print content_title.encode('utf8')
        #
        #
        #     for content in p_contents:
        #         print content.encode('utf8')




            # for s in p_content_title:
            #     print s.encode('utf8')
            #
            # for cs in p_contents:
            #     print cs.encode('utf8')


        # filename = response.url.split("/")[-2]
        # with open(filename, 'wb') as f:
        #     f.write(a_page)


