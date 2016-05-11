# -*- coding: utf-8 -*-
import urllib
import urllib2
import re
import langid

def getToken():
    data = urllib.urlencode({'client_id':'yzkk',
                             'client_secret':'',
                             'grant_type':'client_credentials',
                             'scope':'http://api.microsofttranslator.com'})
    url = 'https://datamarket.accesscontrol.windows.net/v2/OAuth2-13'
    request = urllib2.Request(url, data = data)
    response = eval(urllib2.urlopen(request).read())
    return response["access_token"]

def detect(token, text):
    url = 'http://api.microsofttranslator.com/v2/Http.svc/Detect?'
    url += urllib.urlencode({'text':text})
    headers = {'Authorization' : 'Bearer ' + token}
    request = urllib2.Request(url, headers = headers)
    response = urllib2.urlopen(request)
    pat = re.compile('>(.*?)<')
    result = pat.search(response.read())
    if result:
        return result.group(1)
    else:
        return ''

if __name__ == '__main__':
    f = open('comment.txt')
    output = open('result.txt', 'w')
    patterns = [("<.*?>|\(.*?\)|\[.*?\]|[^\w',!?\.]+?", ' '), ("(('[^s])|_)", ' '),
                (',+', ' , '), ('\.+', ' . '),
                ('\s{2,}', ' '), ('(?<=\w)!', ' !'),
                ('!(?=\w)', '! '), ('(?<=\w)\?', ' ?'),
                ('\?(?=\w)', '? ')]
    lines = f.readlines()
    print lines
    for line in lines:
        line = line.strip()           
        position = line.find('\t')
        owner = line[:position]
        comment = line[position + 1:]
        suspicionFlag = False
        try:
            if langid.classify(comment)[0] != 'en':
                print '=======langid suspicion ' + comment
                # langid maybe wrong, should combine with bing
                suspicionFlag = True
        except:
            # invalid char will cause exception in langid
            token = getToken()
            if detect(token, comment) != 'en':
                print '=======langid throw exception, bing find ' + comment
                continue
        if suspicionFlag:
            token = getToken()
            if detect(token, comment) != 'en':
                print '=======both langid bing find ' + comment
                # both langid and bing say it is not 'en', ignore it
                continue
        for pattern in patterns:
            comment = re.sub(pattern[0], pattern[1], comment)
        print comment
        if len(comment) < 3:
            continue
        output.write(owner + '\t' + comment.lower() + '\n')
    f.close()
    output.close()
