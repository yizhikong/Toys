import urllib2
import urllib
from xml.etree import ElementTree

api_key = ''

def getTags():
    dayHotTagUrl = 'https://api.flickr.com/services/rest?method=flickr.tags.getHotList&api_key=%s&period=day&count=200' % (api_key)
    xml = ElementTree.fromstring(urllib2.urlopen(dayHotTagUrl).read())
    tags = [item.text for item in xml.getchildren()[0].getchildren()]
    weekHotTagUrl = 'https://api.flickr.com/services/rest?method=flickr.tags.getHotList&api_key=%s&period=week&count=200' % (api_key)
    xml = ElementTree.fromstring(urllib2.urlopen(weekHotTagUrl).read())
    tags += [item.text for item in xml.getchildren()[0].getchildren()]
    print len(tags)
    tags = list(set(tags))
    print len(tags)
    relateBaseUrl = 'https://api.flickr.com/services/rest?method=flickr.tags.getRelated&api_key=%s&tag=%s'
    # get 5000 tags
    for tag in tags:
        print len(tags)
        relateUrl = relateBaseUrl % (api_key, tag)
        try:
            xml = ElementTree.fromstring(urllib2.urlopen(relateUrl).read())
        except:
            pass
        relateTags = [item.text for item in xml.getchildren()[0].getchildren()]
        #print relateTags
        for rt in relateTags:
            if rt not in tags:
                tags.append(rt)
        if len(tags) > 5000:
            break
    # find tags which has more than 15k pictures
    goodTags = []
    for tag in tags:
        print tag + " has photos : "
        num = getTagPhotoNum(tag)
        print "\t" + num.strip()
        if (int)(num) > 15000:
            goodTags.append(tag)
    f = open('tags5000.txt', 'w')
    for tag in goodTags:
        try:
            f.write(tag + '\n')
        except:
            pass
    f.close()

# save photo as 'photoId_commentNums.jpg'
def extractOne(photoMsg, fileOp, imgPath):
    user_id, farm_id, server_id, photo_id, photo_secret = photoMsg
    imgUrl = 'http://farm%s.static.flickr.com/%s/%s_%s.jpg' % (farm_id, server_id, photo_id, photo_secret)
    cmtUrl = 'https://api.flickr.com/services/rest?offset=0&limit=50&sort=date-posted-desc&method=' +\
             'flickr.photos.comments.getList&api_key=%s&photo_id=%s' % (api_key, photo_id)
    xml = ElementTree.fromstring(urllib2.urlopen(cmtUrl).read())
    comments = xml.getchildren()[0].getchildren()
    savePath = imgPath +  photo_id + '_' + str(len(comments)) + '.jpg'
    urllib.urlretrieve(imgUrl, savePath)
    # can filt comments here
    for comment in comments:
        print photo_id + ' ' + comment.attrib['author'] + ' ' + comment.text
        try:
            fileOp.write(photo_id + ' ' + comment.attrib['author'] + ' ' + comment.text)
        except:
            print 'comment has invalid char'
        fileOp.write('\n')

def getTagPhotoNum(tagName):
    tagUrl = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=%s&tags=%s' % (api_key, tagName)
    xml = ElementTree.fromstring(urllib2.urlopen(tagUrl).read())
    return xml.getchildren()[0].attrib["total"]

# get photo message(id, owner and so on) by tag
def getPhotosMsgByTag(tagName):
    tagUrl = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=%s&tags=%s' % (api_key, tagName)
    xml = ElementTree.fromstring(urllib2.urlopen(tagUrl).read())
    photosXml = xml.getchildren()[0].getchildren()
    photos = []
    for photo in photosXml:
        attrib = photo.attrib
        photos.append((attrib['owner'], attrib['farm'], attrib['server'], attrib['id'], attrib['secret']))
    return photos

if __name__ == '__main__':
    # just take one tag for example, you can take all the tags to download lots of photos
    #getTags()
    print getTagPhotoNum("springtraining")
    '''
    tagName = 'puppy'
    f = open('D:/comment.txt', 'w')
    for photo in getPhotosMsgByTag(tagName):
        # multiple thread can set here
        extractOne(photo, f, 'D:/photos/')
    f.close()
    '''
