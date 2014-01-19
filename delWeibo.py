#delete weibo by weibo API
# -*- coding: cp936 -*-
#encoding=utf8
from weibo import APIClient
import webbrowser
import sys
import urllib
import urllib2
APP_KEY = 'your APP_KEY'
APP_SECRET = 'your APP_SECRET'
CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'
client = APIClient(app_key = APP_KEY, app_secret = APP_SECRET, \
                   redirect_uri = CALLBACK_URL)
url = client.get_authorize_url() 
webbrowser.open_new(url)  # get the code from the open web
code = raw_input('code : ')
client = APIClient(app_key = APP_KEY, app_secret = APP_SECRET, \
                   redirect_uri = CALLBACK_URL)
r = client.request_access_token(code)
access_token = r.access_token
expires_in = r.expires_in
client.set_access_token(access_token, expires_in)
weiboList = client.statuses.user_timeline.ids.get(uid = 'your weibo uid', \
                                                  feature = 1).statuses
#I save the weibo in weibo.txt before delete it
f = open('weibo.txt', 'a')
reload(sys)
sys.setdefaultencoding('utf-8')
count = 1
while len(weiboList) != 0:
    print 'in run ' + repr(count)
    for weiboId in weiboList:
        currentWeibo = client.statuses.show.get(id = weiboId)
        f.write(currentWeibo.text)
        f.write('\n')
        f.write(currentWeibo.created_at)
        f.write('\n\n')
        client.statuses.destroy.post(id = weiboId)
    weiboList = client.statuses.user_timeline.ids.get(uid = 'your weibo uid', \
                                                      feature = 1).statuses
    count = count + 1
f.close()
