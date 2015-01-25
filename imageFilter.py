import time
from PIL import Image, ImageGrab
from numpy import *
# flags = 1 for DFT, flags = -1 for IDFT
def dft2d(input_img, flags):
    row, col = input_img.shape
    img = input_img.copy()
    maxSide = max(col, row)
    # column vector
    x = array(range(maxSide)).reshape(maxSide, 1)
    # row vector
    y = array(range(maxSide)).reshape(1, maxSide)
    # get a matrix
    uxvy = dot(x, y) * 2 * pi
    # evy means e ** (2 * pi * v * y / N)
    evy = (uxvy[:col, :col].copy()) / col
    evy = cos(evy) - flags * sin(evy) * 1j
    # eux means e ** (2 * pi * u * x / M)
    eux = (uxvy[:row, :row].copy()) / row
    eux = cos(eux) - flags * sin(eux) * 1j
    # separability of the 2-D DFT
    F_x_v = dot(img, evy)
    F_u_v = dot(eux, F_x_v)
    # if it is IDFT, multiple 1 / MN
    if flags == -1:
        constNum = 1.0 / (row * col)
        F_u_v *= constNum
    return F_u_v

# flags = 1 for DFT, flags = -1 for IDFT
# 1D fft, recursion version
def fft1d(f, flags):
    M = f.shape[0]
    K = M / 2
    F = array([0j] * M)
    if M == 1:
        F[0] = f[0]
        return F
    # get the even list and odd list
    f_even = f[0:M:2]
    f_odd = f[1:M:2]
    # recursion
    F_even = fft1d(f_even, flags)
    F_odd = fft1d(f_odd, flags)
    # combine
    for u in range(K):
        temp = 2 * pi * u / M
        mul = F_odd[u] * complex(cos(temp), -flags * sin(temp))
        F[u] = F_even[u] + mul
        F[u + K] = F_even[u] - mul
    return F

# flags = 1 for DFT, flags = -1 for IDFT
def fft2d(pImg, flags):
    # pImg's size should be 2**n
    P, Q = pImg.shape
    temp = array([0j] * P * Q).reshape(P, Q)
    # for each row
    for i in range(P):
        temp[i] = fft1d(pImg[i], flags)
    # for each column
    for j in range(Q):
        temp[0:P, j] = fft1d(temp[0:P, j], flags)
    # if it is IDFT, multiple 1 / MN
    if flags == -1:
        temp = temp / (P * Q)
    return temp

# filt in fequency
def filter2d_freq(input_img, filt):
    M, N = input_img.shape
    m, n = filt.shape
    # pad the image and filter
    pImg = padImg(input_img, M+m-1, N+n-1)
    pFilter = padFilter(filt, M+m-1, N+n-1)
    # do DFT
    F = dft2d(pImg, 1)
    H = dft2d(pFilter, 1)
    # point multiple
    G = H * F
    # center
    G = center(G)
    # get the left-top part
    g = ((dft2d(G, -1).real))[:M, :N]
    return g

'''
    ----------------------------------------------
    the above part contains the two function of homework
    ----------------------------------------------
'''

# multip (-1) ** (x + y)
def center(input_img):
    newMatrix = input_img.copy()
    row, col = input_img.shape
    for x in range(row):
        for y in range(col):
            newMatrix[x][y] = input_img[x][y] * (-1) ** (x + y)
    return newMatrix

# make the filter in the center
def padFilter(filt, P, Q):
    size = filt.shape[0]
    up = ((P - size) + 1) / 2
    down = P - size - up
    left = ((Q - size) + 1) / 2
    right = Q - size - left
    padUp = zeros((up , size))
    padDown = zeros((down, size))
    filt = vstack((padUp, filt, padDown))
    padLeft = zeros((P, left))
    padRight = zeros((P, right))
    filt = hstack((padLeft, filt, padRight))
    return filt

# make the image in the left-top
# finally I found that this function can be done in 3 line of code
# so stupid I am
def padImg(img, P, Q):
    row, col = img.shape
    right = Q - col
    down = P - row
    padRight = zeros((row, right))
    img = hstack((img, padRight))
    padDown = zeros((down, Q))
    img = vstack((img, padDown))
    return img

# service for the menu
def showSpectrum(input_img, version):
    # do DFT(user select 1)
    if version == 1:
        F = dft2d(center(input_img), 1)
    # do FFT(user select 3)
    if version == 3:
        cImg = center(input_img)
        row, col = cImg.shape
        P = 1
        Q = 1
        while (P < row):
            P *= 2
        while (Q < col):
            Q *= 2
        pImg = padImg(cImg, P, Q)
        F = fft2d(pImg, 1)
    # make it look normal
    spectrum = log(abs(F) + 1)
    height, width = spectrum.shape
    # scale
    maxNum = spectrum.max()
    minNum = spectrum.min()
    delta = maxNum-minNum
    newImg = Image.new('L', (width, height))
    for i in range(width):
        for j in range(height):
            newImg.putpixel((i,j), (spectrum[j][i] - minNum) * 255 / delta)
    newImg.show()
    #newImg.save("19_spectrum.png")

# service for the menu
# do DFT and then IDFT, the result picture will be extramely similar to the
# original picture
def dft_idft(input_img):
    real = dft2d(dft2d(input_img, 1),-1).real
    height, width = real.shape
    newImg = Image.new('L', (width, height))
    for i in range(width):
        for j in range(height):
            newImg.putpixel((i,j), real[j][i])
    newImg.show()
    #newImg.save("19_dft_idft.png")

# service for the menu
# do FFT and then IFFT, the result picture will be extramely similar to the
# original picture
def fft_ifft(input_img):
    row, col = input_img.shape
    P = 1
    Q = 1
    while (P < row):
        P *= 2
    while (Q < col):
        Q *= 2
    pImg = padImg(matrix, P, Q)
    real = fft2d(fft2d(pImg, 1),-1)[:row, :col].real
    height, width = real.shape
    newImg = Image.new('L', (width, height))
    for i in range(width):
        for j in range(height):
            newImg.putpixel((i,j), real[j][i])
    newImg.show()
    #newImg.save("19_fft_ifft.png")

# service for the menu
def filtInFreq(input_img, filt):
    g = filter2d_freq(matrix, filt)
    filt_Img = Image.new('L', (width, height))
    for i in range(width):
        for j in range(height):
            value = g[j][i]
            if value < 0:
                value = 0
            if value > 255:
                value = 255
            filt_Img.putpixel((i,j), value)
    filt_Img.show()
    #filt_Img.save("19_averaging.png")
    #filt_Img.save("19_laplacian.png")
