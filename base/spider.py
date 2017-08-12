# -*- coding: utf-8 -*-
import cookielib
import random
import time
import json
import requests
import threading
import Queue
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class LingSpider(object):
    agent = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
    ]
    threads = []

    def __init__(self, pid_file_name):
        (name, ext) = os.path.splitext(pid_file_name)
        self.pid_file_name = name
        self.pid_file_path = None
        self.project_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.q = Queue.Queue(128)

    # pid 文件处理
    def create_pid_file(self):
        self.pid_file_path = '{0}/cache/{1}.pid'.format(self.project_path, self.pid_file_name)
        with open('{0}/cache/{1}.pid'.format(self.project_path, self.pid_file_name), 'w') as f:
            f.write('{}'.format(os.getpid()))

    def del_pid_file(self):
        if self.pid_file_path is not None:
            os.remove(self.pid_file_path)
            pass

    def run(self):
        print u'run'
        self.create_pid_file()
        th = []

        for name in self.threads:
            tf = threading.Thread(target=LingSpider.__start, args=(self,), name=name)
            th.append(tf)

        t = threading.Thread(target=LingSpider.queue_work, args=(self,), name='queue')
        th.append(t)

        for t in th:
            t.start()
        for t in th:
            t.join()

        print 'game over'
        if os.path.isfile(self.pid_file_path):
            self.del_pid_file()

    def __start(self):
        self.init()
        while os.path.isfile(self.pid_file_path):
            res = self.spider()
            if res is False:
                break
        self.end()

    def init(self):
        pass

    def end(self):
        pass

    def spider(self):
        print 'spider'

    def queue_work(self):
        print u'queue_work'
        # del pid 强制结束
        while os.path.isfile(self.pid_file_path) and threading.active_count() > 2:
            print u"当前线程数：", threading.active_count()
            if self.q.qsize() >= 1:
                item = self.q.get()
                res = self.save(item)
                print u"save response:", res
            else:
                print u'no item sleep 3s'
                time.sleep(3)
        print u"当前线程数：", threading.active_count()
        print 'queue is over'

    def save(self, item):
        print u'save'
        print u"save --> item:", item
        return {}

    def ling_request(self, url, header={}):
        name = threading.current_thread().name
        self.log(url)
        header['User-Agent'] = random.choice(self.agent)
        print 'threading:{} url:{} User-Agent:{}'.format(name, url, header.get('User-Agent'))
        session = requests.Session()
        session.cookies = cookielib.LWPCookieJar(filename="{}/cache/{}/{}_cookies.txt".format(self.project_path, self.pid_file_name, name))
        res = {}
        response = None

        try:
            # ignore_discard=True 忽略关闭浏览器丢失 , ignore_expires=True ,忽略失效  --load() 在文件中读取cookie
            session.cookies.load(ignore_discard=True)
        except Exception, e:
            print u"failed load cookie !! Exception:{}".format(e.message)
        try:
            response = session.get(url, headers=header, timeout=61)
            session.cookies.save()
            res['status_code'] = response.status_code
            res['reason'] = response.reason
        except Exception as e:
            res['status_code'] = 110
            res['reason'] = u"error:  e.message->{}".format(e.message)
            res['url'] = url
        print res
        self.log(res, 'ling')

        time.sleep((threading.active_count()-1) * 0.3)  # 多线程 请求 延时 时间 间隔
        return res, response

    # 日志 记录
    def log(self, content, key_str='default'):
        name = threading.current_thread().name
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        log_path = "{}/cache/{}".format(self.project_path, self.pid_file_name)
        if not os.path.exists(log_path):
            os.makedirs(log_path)

        with open("{}/{}_{}.log".format(log_path, time.strftime("%Y-%m-%d", time.localtime(time.time())), name), 'a') as f:
            f.write('{} -->>'.format(key_str))
            f.write('{}:\n'.format(now))
            f.write('\t')
            f.write(json.dumps(content, ensure_ascii=False, encoding='utf-8'))
            f.write('\n')

    def __del__(self):
        if os.path.isfile(self.pid_file_path):
            self.del_pid_file()

    pass
