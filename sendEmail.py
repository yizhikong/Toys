# maybe you should open SMTP service(in your email setting) first
import smtplib
from email.mime.text import MIMEText
def sendEmail(fromUser, password, toUser, title, content):
    parse = toUser.split('@')
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
    server.sendmail(formUser, toUser, msg.as_string())
    server.close()

sendEmail('xxxxx@qq.com', 'mypassword', 'xxxxx@qq.com', 'My first eamil', 'Hello world!')
