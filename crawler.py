# -*- coding: cp936 -*-
import urllib2
import urllib
import re
from bs4 import BeautifulSoup
import json
import os
import thread

class TaobaoCrawler:
    def __init__(self, max_page=5):
        self.MAX_PAGE = max_page
        print 'use function crawl to download'

    def crawl(self, query_word):
        if not os.path.exists(query_word):
            os.mkdir(query_word)
        detail_ids = self.search(query_word)
        print len(detail_ids)
        for the_id in detail_ids:
            print 'crawling ' + the_id
            # create a folder for this item
            folder = query_word + '/' + the_id
            try:
                self.__saveById(the_id, folder)
            except:
                print 'crawl ' + the_id + ' failed'

    def __saveById(self, the_id, folder):
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
        
    def search(self, query_word):
        parameter = urllib.urlencode({'q' : query_word.encode('gb2312')})
        url = 'https://s.taobao.com/search?' + parameter
        ids = []
        text = urllib2.urlopen(url).read()
        count = 0
        while text and count < self.MAX_PAGE:
            #pat = re.compile('g_page_config\s?=\s?({.*})')
            pat = re.compile('"allNids":(\[.*?\])')
            result = pat.search(text)
            ids += eval(result.group(1))
            soup = BeautifulSoup(text)
            all_a = soup.find_all('a')
            print len(all_a)
            for a in all_a:
                print a['href']
            f = open('page.txt', 'w')
            f.write(str(soup.find_all('script')))
            f.close()
            # next page
            next_page = soup.find(attrs={'class':'item next'}).find('a')
            try:
                ['href']
                text = urllib2.urlopen(next_page).read()
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
        parameter = urllib.urlencode({'auctionNumId' : the_id,
                                      'currentPageNum' : page_num,
                                      'pageSize' : 20})
        comment_url = 'https://rate.taobao.com/feedRateList.htm?' + parameter
        text = urllib2.urlopen(comment_url).read()
        pat = re.compile('\s*\((.*)\)\s+')
        result = pat.search(text)
        data = json.loads(result.group(1).decode('gb2312', 'ignore'))
        maxPage = min(data['total'] / 20, 5)
        comments = data['comments']
        if maxPage > 1 and page_num == 1:
            for i in range(2, maxPage + 1):
                comments += self.getComments(the_id, i)
        return comments

if __name__ == '__main__':
    taobao = TaobaoCrawler()
    #print taobao.getPictures('17380454793')
    taobao.crawl(u'睡衣')
