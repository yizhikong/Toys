# -*- coding: cp936 -*-
#  download pictures from tieba by using re
import urllib
import urllib2
import re
import threading
import sys

# get all possible comic pages from the root(guide) page
# the key of dic is file_num, the value of dic is comic page url of that file
def getComicUrls(root_url):
    urls = []
    response = urllib2.urlopen(root_url)
    link_pattern = re.compile('>(http://tieba.baidu.com/(f\?kz|p).*?)</a>')
    for line in response:
        result = link_pattern.findall(line)
        if len(result) > 0:
            for res in result:
                urls.append(res[0])
                sys.stdout.write("\rget %d urls..." % len(urls))
    print "\nfilting the urls:"
    dic = filtUrl(urls)
    return dic

# get valid comic pages from urls by judging whether the title contains (file) number
# the key of dic is file_num, the value of dic is comic page url of that file
def filtUrl(urls):
    page_urls_dic = {}
    count = 1
    for url in urls:
        sys.stdout.write("\ranalyzing " + url + "... " +\
                         "[%d/%d]     " % (count, len(urls)))
        count += 1
        response = urllib2.urlopen(url)
        # find the title and quick the loop quickly
        title_pattern = re.compile('<title>.*?</title>')
        for line in response:
            result = title_pattern.search(line)
            if result:
                break
        # check whether the title contain numbers(file_num)
        file_pattern = re.compile('[0-9]+')
        result = file_pattern.search(result.group(0))
        if result:
            # the url refers to some file
            file_num = result.group(0)
            page_urls_dic[int(file_num)] = url
    print "\ntotally " + repr(len(page_urls_dic)) + " valid urls are found"
    return page_urls_dic

# get all the pictures from a comic page
def getPicUrls(page_url):
    pic_urls = []
    pic_pattern = [re.compile('src="(http://hiphotos.baidu.com/.*?)"'), \
               re.compile('<img.*?BDE_Image.*?src="(http://imgsrc.baidu.com/.*?)"')]
    response = urllib2.urlopen(page_url)
    # try to use pattern to find picture's url
    results = pic_pattern[0].findall(response.read())
    for res in results:
        pic_urls.append(res)
    # the pictures' url is not in pattern1, try pattern2
    if len(pic_urls) == 0:
        response = urllib2.urlopen(page_url)
        results = pic_pattern[1].findall(response.read())
        for res in results:
            pic_urls.append(res)
    return pic_urls

# down a file by file_num
def downFile(pages_dic, file_num):
    try:
        file_num = int(file_num)
        url = pages_dic[file_num]
    except ValueError:
        print "wrong file_num"
        return
    except KeyError:
        print "sorry, no such file was searched:("
        return
    pages = getPicUrls(url)
    print "downloading images..."
    for i in range(len(pages)):
        filename = "FILE_" + str(file_num) + "_" + str(i) + ".jpg"
        t = threading.Thread(target = urllib.urlretrieve, \
                             args = (pages[i], filename))
        t.start()

if __name__ == "__main__":
    print "running..."
    root_url = 'http://tieba.baidu.com/p/3383251367'
    pages_dic = getComicUrls(root_url)
    print "\nanalyze over"
    while True:
        file_num = raw_input("download file : ")
        downFile(pages_dic, file_num)
