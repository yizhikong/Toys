# -*- coding: cp936 -*-
import re
import json
import math
import os, sys
import urllib, urllib2
import thread, threading
from bs4 import BeautifulSoup

class TaobaoCrawler:
    
    def __init__(self, max_search_page=5, max_comment_page=5, max_thread=25):
        self.MAX_SEARCH_PAGE = max_search_page
        self.MAX_COMMENT_PAGE = max_comment_page
        self.MAX_THREAD = max_thread
        print 'use function crawl to download'

    # crawl the pictures and comments for goods
    # first get lot of items(id) according query_word by searching page to page
    # then get and save each item's infomation according item id
    def crawl(self, query_word):
        if not os.path.exists(query_word):
            os.mkdir(query_word)
        # get item ids by search function.
        detail_ids = self.search(query_word)
        thread_num = 0
        # spilit all ids to serveral batches according MAX_THREAD
        while thread_num < len(detail_ids):
            batch = detail_ids[thread_num : thread_num + self.MAX_THREAD]
            threads = []
            for the_id in batch:
                # get the folder name for this item
                folder = query_word + '/' + the_id
                # use one thread to crawl and get one item(id)
                t = threading.Thread(target = self.__saveById,
                                         args = (the_id, folder))
                t.start()
                threads.append(t)
            for th in threads:
                th.join(30)
            thread_num += self.MAX_THREAD
        print 'Finish'

    # crawl and save one item
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

    # search item ids according query_word
    def search(self, query_word):
        query_dict = {'q' : query_word.encode('gb2312'), 's' : 0}
        parameter = urllib.urlencode(query_dict)
        # construct the search page url
        url = 'https://s.taobao.com/search?' + parameter
        ids = []
        text = urllib2.urlopen(url).read()
        count = 0
        # search MAX_PAGE pages
        while text and count < self.MAX_SEARCH_PAGE:
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

    # get pictures of one item according its detail page(according id)
    def getPictures(self, the_id):
        parameter = urllib.urlencode({'id' : the_id})
        # construct detail page url
        detail_url = 'https://detail.tmall.com/item.htm?' + parameter
        print detail_url
        text = urllib2.urlopen(detail_url).read()
        soup = BeautifulSoup(text)
        # the pictures are in this place. You can find it by analyzing the html
        gallery = soup.find(id = 'J_UlThumb').find_all('img')
        urls = map(lambda x : x[x.attrs.keys()[0]], gallery)
        pat = re.compile('.*?(jpg|png|jpeh)')
        for i in range(len(urls)):
            result = pat.search(urls[i])
            if result:
                urls[i] = result.group(0)
        return urls

    # get comments of one item according a feedRayeList url(according id)
    def getComments(self, the_id, page_num = 1):
        comments = []
        try:
            parameter = urllib.urlencode({'auctionNumId' : the_id,
                                          'currentPageNum' : page_num,
                                          'pageSize' : 20})
            # construct feedRateList url
            # get this url by analyzing the request when we get comments by browser
            comment_url = 'https://rate.taobao.com/feedRateList.htm?' + parameter
            text = urllib2.urlopen(comment_url).read()
            pat = re.compile('\s*\((.*)\)\s+')
            result = pat.search(text)
            if result:
                data = json.loads(result.group(1).decode('gb2312', 'ignore'))
                # count how many comments page it has
                # limit the page with MAX_COMMENT_PAGE
                maxPage = min(int(math.ceil(data['total'] / 20.0)),
                              self.MAX_COMMENT_PAGE)
                comments = data['comments']
                # get the comments from following page when current page is the first page
                if maxPage > 1 and page_num == 1:
                    for i in range(2, maxPage + 1):
                        comments += self.getComments(the_id, i)
        except:
            return []
            print result.group(1).decode('gb2312', 'ignore')
        return comments

if __name__ == '__main__':
    taobao = TaobaoCrawler(max_search_page = 2)
    #print taobao.getPictures('527480658619')
    #cmts = taobao.getComments('43930014708')
    #print len(cmts)
    taobao.crawl(u'睡衣')
