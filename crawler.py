# -*- coding: cp936 -*-
import urllib2
import urllib
import re
from bs4 import BeautifulSoup
import json
import os
import thread
import threading
import sys
import math

class TaobaoCrawler:
    def __init__(self, max_page=5, max_thread=25):
        self.MAX_PAGE = max_page
        self.MAX_THREAD = max_thread
        print 'use function crawl to download'

    def crawl(self, query_word):
        if not os.path.exists(query_word):
            os.mkdir(query_word)
        detail_ids = self.search(query_word)
        thread_num = 0
        while thread_num < len(detail_ids):
            batch = detail_ids[thread_num : thread_num + self.MAX_THREAD]
            threads = []
            for the_id in batch:
                # create the folder name for this item
                folder = query_word + '/' + the_id
                t = threading.Thread(target = self.__saveById,
                                         args = (the_id, folder))
                t.start()
                threads.append(t)
            for th in threads:
                th.join(300)
            thread_num += self.MAX_THREAD
        print 'Finish'

    def __saveById(self, the_id, folder):
        try:
            if not os.path.exists(folder):
                os.mkdir(folder)
            else:
                return
            # get the images of the item and save
            images = self.getPictures(the_id)
            for i in range(len(images)):
                data = urllib2.urlopen('http:' + images[i]).read()
                f = open(folder + '/' + str(i) + '.jpg', 'wb')
                f.write(data)
                f.close()
            # get the comments of the item and save
            comments = self.getComments(the_id)
            f = open(folder + '/' + 'comments.txt', 'w')
            for comment in comments:
                f.write(comment['content'].encode('utf8', 'ignore'))
                f.write('\n')
            f.close()
            print 'Crawl ' + the_id + r' succeed'
        except:
            print 'Crawl ' + the_id + r' failed'
            # raise
        
    def search(self, query_word):
        query_dict = {'q' : query_word.encode('gb2312'), 's' : 0}
        parameter = urllib.urlencode(query_dict)
        url = 'https://s.taobao.com/search?' + parameter
        ids = []
        text = urllib2.urlopen(url).read()
        count = 0
        while text and count < self.MAX_PAGE:
            pat = re.compile('"allNids":(\[.*?\])')
            result = pat.search(text)
            ids += eval(result.group(1))
            # next page
            query_dict['s'] += 44
            parameter = urllib.urlencode(query_dict)
            url = 'https://s.taobao.com/search?' + parameter
            try:
                text = urllib2.urlopen(url).read()
                count += 1
            except:
                text = None
        return ids

    def getPictures(self, the_id):
        parameter = urllib.urlencode({'id' : the_id})
        detail_url = 'https://detail.tmall.com/item.htm?' + parameter
        print detail_url
        text = urllib2.urlopen(detail_url).read()
        soup = BeautifulSoup(text)
        gallery = soup.find(id = 'J_UlThumb').find_all('img')
        urls = map(lambda x : x[x.attrs.keys()[0]], gallery)
        pat = re.compile('.*?(jpg|png|jpeh)')
        for i in range(len(urls)):
            result = pat.search(urls[i])
            if result:
                urls[i] = result.group(0)
        return urls

    def getComments(self, the_id, page_num = 1):
        comments = []
        try:
            parameter = urllib.urlencode({'auctionNumId' : the_id,
                                          'currentPageNum' : page_num,
                                          'pageSize' : 20})
            comment_url = 'https://rate.taobao.com/feedRateList.htm?' + parameter
            text = urllib2.urlopen(comment_url).read()
            pat = re.compile('\s*\((.*)\)\s+')
            result = pat.search(text)
            if result:
                data = json.loads(result.group(1).decode('gb2312', 'ignore'))
                maxPage = min(int(math.ceil(data['total'] / 20.0)), 5)
                comments = data['comments']
                if maxPage > 1 and page_num == 1:
                    for i in range(2, maxPage + 1):
                        comments += self.getComments(the_id, i)
        except:
            return []
            print result.group(1).decode('gb2312', 'ignore')
        return comments

if __name__ == '__main__':
    taobao = TaobaoCrawler(max_page = 1)
    #print taobao.getPictures('527480658619')
    #cmts = taobao.getComments('43930014708')
    #print len(cmts)
    taobao.crawl(u'睡衣')
