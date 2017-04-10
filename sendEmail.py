# -*- coding:utf-8-*-
# maybe you should open SMTP service(in your email setting) first
import smtplib
from email.mime.text import MIMEText
import os
import time
import re

def getStatus():
    info = os.popen('nvidia-smi').read()
    pat = re.compile('(\d+)MiB.*?\d+MiB')
    used_of_gpus = pat.findall(info)
    hasFree = False
    for used_of_gpu in used_of_gpus:
        if int(used_of_gpu) < 1000:
            hasFree = True
    return hasFree, info

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
    hasFree = False
    while True:
        status, info = getStatus()
        if status != hasFree:
            hasFree = status
            title = 'GPUs are busy again!'
            if hasFree == True:
                title = 'Free GPU is avaliable now!'
            sendEmail('sendEmail@xx.com', 'sendPassword', 'receiveEmail@xx.com',
                      title, info)
            print 'send ' + title
        time.sleep(600)
