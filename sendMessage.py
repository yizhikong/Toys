#use other's api to send [FeiXin] message (delayed)
#-*- coding=utf-8 -*-
import urllib2
import time
import re
phone, password = raw_input("your phone and password : ").split(' ')
msg = raw_input("what do you want to send : ")
receive = raw_input("sent to : ")
url = 'http://quanapi.sinaapp.com/fetion.php?u='
delay = raw_input("delay(s) : ")
time.sleep(int(delay))
urllib2.urlopen(url + phone + '&p=' + password + '&to=' + receive + '&m=' + msg + repr(i))
