from PIL import Image, ImageGrab
from numpy import *
import random
import math

# the yield version of view_as_window function, lazy 
def view_as_window(img, patch_size):
    height, width = img.shape
    pWidth = patch_size[0]
    pHeight = patch_size[1]
    for i in range(width - pWidth + 1):
        for j in range(height - pHeight + 1):
            # the RGB[i][j] is the left-top pixel of the patch
            domain = img[j:(j+pHeight), i:(i+pWidth)]
            yield domain

# size is the size of patch
def getDarkChannel(r, g, b, size):
    height, width = r.shape
    # get the min pixel among r, g and b
    min_rgb = zeros((height, width), dtype = "double")
    for h in range(height):
        for w in range(width):
            min_rgb[h][w] = min(r[h][w], g[h][w], b[h][w])
    # min filter
    img = minFilter(min_rgb, size)
    return img

def getA(r, g, b, darkChannel):
    height, width = darkChannel.shape
    length = height * width
    sortedPixel = darkChannel.copy().reshape(1, length)
    # sort the pixel in darkChannel
    sortedPixel.sort()
    # find the tenth high pixel
    tenthMax = sortedPixel[0][int(length - length * 0.001)]
    # the 0.1% pixel were selected, now find them out
    # and find the pixel with highest intensity
    maxIntensity = 0
    max_h = 0
    max_w = 0
    for h in range(height):
        for w in range(width):
            if darkChannel[h][w] > tenthMax:
                # saving the time, ignore the 1/3
                intensity = r[h][w] + g[h][w] + b[h][w]
                if intensity > maxIntensity:
                    maxIntensity = intensity
                    max_h = h
                    max_w = w
    # adjust A to avoid terrible sky
    r_A = min(r[max_h][max_w], 220)
    g_A = min(g[max_h][max_w], 220)
    b_A = min(b[max_h][max_w], 220)
    A = (r_A, g_A, b_A)
    return A

def getT(r, g, b, A, size):
    # original T
    t = 1 - 0.95 * getDarkChannel(r/A[0], g/A[1], b/A[2], size)
    # get the gray image of the image to be the guide image
    guideImg = getGrayChannel(r, g, b)
    # guide filter
    t_img = guidefilter(guideImg / 255, t, (41, 41), 0.0001)
    return t_img

def guidefilter(I, p, size, eps):
    # these four filt can be done with multithread but i am lazy..
    meanI = arithmeticfilter(I, size)
    meanp = arithmeticfilter(p, size)
    corrI = arithmeticfilter(I * I, size)
    corrIp = arithmeticfilter(I * p, size)
    varI = corrI - meanI * meanI
    covIp = corrIp - meanI * meanp
    # eps is a regularization parameter penalizing large a
    a = covIp / (varI + eps)
    b = meanp - a * meanI
    meana = arithmeticfilter(a, size)
    meanb = arithmeticfilter(b, size)
    # the guide model
    q = meana * I + meanb
    return q

def minFilter(input_img, size):
    height, width = input_img.shape
    pW = size[0] / 2
    pH = size[1] / 2
    newWidth = width + pW * 2
    newHeight = height + pH * 2
    # padding
    # 0 will lead to white border
    # img = zeros((newHeight, newWidth), dtype = "double")
    img = array([255.0] * newHeight * newWidth).reshape(newHeight, newWidth)
    # center part
    img[pH:(pH + height), pW:(pW + width)] = input_img.copy()
    w = 0
    h = 0
    # min filter
    for domain in view_as_window(img, size):
        # get the minimun number of the domain
        input_img[h][w] = domain.min()
        h += 1
        if h == height:
            h = 0
            w += 1
    return input_img

def arithmeticfilter(input_img, size):
    height, width = input_img.shape
    pW = size[0] / 2
    pH = size[1] / 2
    newWidth = width + pW * 2
    newHeight = height + pH * 2
    # padding
    img = zeros((newHeight, newWidth), dtype = "double")
    returnImg = zeros((height, width), dtype = "double")
    # center part
    img[pH:(pH + height), pW:(pW + width)] = input_img.copy()
    # top and bottom mirror copy
    for h in range(pH):
        img[h, pW:(width+pW)] = input_img[pH-h].copy()
        img[(height+pH +h), pW:(width+pW)] = input_img[height-1-h].copy()
    # left and right mirror copy
    for w in range(pW):
        img[pH:(height+pH), w] = input_img[:, pW - w].copy()
        img[pH:(height+pH), width+pW+w] = input_img[:, width-1-w].copy()
    w = 0
    h = 0
    # arithmetic mean filter
    coefficient = 1.0 / (size[0] * size[1])
    for domain in view_as_window(img, size):
        returnImg[h][w] = domain.sum()
        h += 1
        if h == height:
            h = 0
            w += 1
    returnImg *= coefficient
    return returnImg

# get a gray image from a color image
def getGrayChannel(r, g, b):
    height, width = r.shape
    img = zeros((height, width), dtype = "double")
    for h in range(height):
        for w in range(width):
            img[h][w] = r[h][w] * 0.299 + g[h][w] * 0.587 + b[h][w] * 0.114
    return img

# the major function
def dehaze(r, g, b, size):
    height, width = r.shape
    darkChannel = getDarkChannel(r, g, b, size)
    A = getA(r, g, b, darkChannel)
    print A
    t = getT(r, g, b, A, size)
    print 'get T matrix'
    Jr = zeros((height, width), dtype="double")
    Jg = zeros((height, width), dtype="double")
    Jb = zeros((height, width), dtype="double")
    for h in range(height):
        for w in range(width):
            # avoid small t
            t_value = max(t[h][w], 0.1)
            Jr[h][w] = (r[h][w] - A[0]) / t_value + A[0]
            Jg[h][w] = (g[h][w] - A[1]) / t_value + A[1]
            Jb[h][w] = (b[h][w]  - A[2]) / t_value + A[2]
    saveName = raw_input("save file as : ")
    saveRGB(Jr, Jg, Jb, saveName)

# for image with r g b
def loadRGB(fileName):
    img = Image.open(fileName)
    width, height = img.size
    rgb = img.split()
    r_ = rgb[0].getdata()
    g_ = rgb[1].getdata()
    b_ = rgb[2].getdata()
    r = array(list(r_), dtype="double").reshape(height, width)
    g = array(list(g_), dtype="double").reshape(height, width)
    b = array(list(b_), dtype="double").reshape(height, width)
    return (r, g, b)

# for image with r g b 
def saveRGB(r, g, b, fileName):
    height, width = r.shape
    newImg = Image.new('RGB', (width, height))
    for i in range(width):
        for j in range(height):
            rgbTuple = (int(r[j][i]), int(g[j][i]), int(b[j][i]))
            newImg.putpixel((i,j), rgbTuple)
    if "png" not in fileName:
        fileName += ".png"
    newImg.save(fileName)

# for gray image
def saveImg(matrix, fileName):
    height, width = matrix.shape
    newImg = Image.new('L', (width, height))
    for i in range(width):
        for j in range(height):
            value = matrix[j][i]
            if value < 0:
                value = 0
            if value > 255:
                value = 255
            try :
                newImg.putpixel((i,j), value)
            except Exception:
                newImg.putpixel((i,j), 0)
    #newImg.show()
    if "png" not in fileName:
        fileName += ".png"
    newImg.save(fileName)

if __name__ == "__main__":
    while True:
        fileName = raw_input("input image name : ")
        r, g, b = loadRGB(fileName)
        size = (15, 15)
        dehaze(r, g, b, size)
