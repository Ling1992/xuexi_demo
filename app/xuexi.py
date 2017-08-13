# -*- coding: utf-8 -*-
from base.spider import LingSpider
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class xuexi(LingSpider):

    url = "http://www.xuexi111.com/yingyv/index_{}.html"
    index = 260

    def url_queue(self):
        url = self.url.format(self.index)
        self.index += 1
        res = self.simple_request(url)
        print res
        if res.get("status_code") == 110 or res.get("status_code") == 404:
            return ""
        else:
            return url
