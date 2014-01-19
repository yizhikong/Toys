import urllib, urllib2, re, threading
addr = 'http://tieba.baidu.com/p/250465074?pn='
page = 7
pat = re.compile('http://hiphotos\.baidu\.com/lzmh19/pic.*?jpg')
print 'running...'
count = 0
for i in range(1, page + 1):
    addr = 'http://tieba.baidu.com/p/250309968?pn=' + repr(i)
    urlnames = []
    text = urllib2.urlopen(addr).read()
    for line in urllib2.urlopen(addr) :
        check = pat.search(line)
        if check :
            print 'downing in page ' + repr(i)
            urlnames.append(check.group(0))
    if urlnames == 0:
        print 'fail'
    for URL in urlnames:
        name = 'C:\\Users\\Administrator\\Desktop\\test\\test' + repr(count) + '.jpg'
        t = threading.Thread(target = urllib.urlretrieve, args = (URL, name))
        t.start()
        count = count + 1
print 'finish'
