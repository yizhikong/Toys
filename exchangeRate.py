# -*- coding:utf-8-*-
# maybe you should open SMTP service(in your email setting) first
import smtplib
from email.mime.text import MIMEText
import os
import time
import re
import urllib2

def getStatus():
    url = 'http://www.baidu.com/s?ie=utf-8&f=3&rsv_bp=1&rsv_idx=1&tn=baidu&wd=%E6%96%B0%E5%8A%A0%E5%9D%A1%E5%B8%81%E5%AF%B9%E4%BA%BA%E6%B0%91%E5%B8%81%E6%B1%87%E7%8E%87&oq=%E6%96%B0%E5%8A%A0%E5%9D%A1%E5%B8%81%E5%AF%B9%E4%BA%BA%E6%B0%91%E5%B8%81%E6%B1%87%E7%8E%87&rsv_pq=b5e65990000008e0&rsv_t=0ed4ZSC49cgXDovgyufVAYl8P6vAWI6xMdWU0LAWhf0M2vLd82Cb3n6IKTQ&rqlang=cn&rsv_enter=0&prefixsug=%E6%96%B0%E5%8A%A0%E5%9D%A1%E5%B8%81%E5%AF%B9%E4%BA%BA%E6%B0%91%E5%B8%81%E6%B1%87%E7%8E%87&rsp=0'
    html = urllib2.urlopen(url).read()
    pat = re.compile('<div>(1.*?=.*?)</div>.*?<div>(1.*?=.*?)</div>')
    result = pat.search(html)
    if result:
        return result.group(1) + ' \r\n' + result.group(2) +\
               ' \r\n' + getRefreshTime(html)
    return None

def getRefreshTime(html):
    pat = re.compile('<div class="c-gap-top op_exrate_tip".*?>(.*?)<')
    result = pat.search(html)
    if result:
        return result.group(1)
    return ''

def sendEmail(fromUser, password, toUser, title, content):
	parse = fromUser.split('@')
	mailHost = 'smtp.' + parse[1]
	#mailPostFix = parse[1]
	msg = MIMEText(content, _subtype = 'plain', _charset = 'gb2312')
	msg['Subject'] = title
	msg['From'] = fromUser
	msg['to'] = toUser
	server = smtplib.SMTP()
	server.connect(mailHost)
	server.login(fromUser, password)
	#print mailHost
	server.sendmail(fromUser, toUser, msg.as_string())
	server.close()

if __name__ == '__main__':
    # set the imformation
    from_user = 'sendEmail@xx.com'
    password = 'sendPassword'
    email_title = 'Realtime Exchange Rate'
    to_user = 'receiveEmail@xx.com'
    # begin monitor
    status = ''
    while False:
        current  = getStatus()
        if current != status:
            sendEmail(from_user, password, to_user, 
                      email_title, current.decode('utf8', 'ignore'))
            status = current
            print status
        else:
            print 'no update'
        time.sleep(60)
