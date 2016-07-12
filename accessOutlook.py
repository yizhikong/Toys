import win32com.client as win32
import datetime
import time
import re

# Save my conversation with yiyi in skype by accessing the mails in outlook.
# I have tried to do this with C# but the requirements are real troublesome. A terrible try
# love python

def getConversationWith(selectName, mailbox):
    mails = mailbox.Items
    conversation = []
    mail = mails.GetFirst()
    while mail:
        try:
            subject = mail.Subject
            time = mail.ReceivedTime
            body = mail.Body
            sender = mail.SenderName
            receiver = mail.To
            if subject == 'Conversation with ' + selectName or sender == selectName or receiver == selectName:
                conversation.append({'subject':subject, 'time':time, 'sender':sender, 'body':body})
        except:
            pass
        mail = mails.GetNext()
    conversation = sorted(conversation, key=lambda x : x['time'])
    return conversation

if __name__ == '__main__':
    # I save lots of conversation in this special folder 'yiyi'
    SPECIAL_FOLDERNAME = 'yiyi'
    # I want to get the conversation with yiyi
    WITH_WHO = 'yiyi'

    conversation = []
    # get conversation from special folder
    outlook = win32.gencache.EnsureDispatch('Outlook.Application')
    namespace = outlook.GetNamespace('MAPI')
    folders = namespace.Folders.GetFirst().Folders
    folder = folders.GetFirst()
    while folder:
        if folder.Name == SPECIAL_FOLDERNAME:
            mailbox = folder
        folder = folders.GetNext()
    conversation += getConversationWith(WITH_WHO, mailbox)
    # get conversation from default folder
    mailbox = namespace.GetDefaultFolder(win32.constants.olFolderInbox)
    conversation += getConversationWith(WITH_WHO, mailbox)

    # sort by conversation time
    conversation = sorted(conversation, key=lambda x : x['time'])
    f = open('conversation.txt', 'w')
    for i in range(len(conversation) - 1):
        if conversation[i]['body'] in conversation[i + 1]['body']:
            continue
        f.write(str(conversation[i]['time']) + '\n')
        f.write(conversation[i]['body'].encode('utf8'))
        f.write('\n\n')
    f.write(str(conversation[-1]['time']) + '\n')
    f.write(conversation[-1]['body'].encode('utf8'))
    f.write('\n\n')
    f.close()
