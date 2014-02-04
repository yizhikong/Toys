# cheat in QQ game "DuiDuiPeng", but it dosen't work well(To slow).
import autopy
import time
import Image
import ImageGrab
#all = [[],[],[],[],[],[],[],[]]
def flect(picHash):
    if picHash > 15000386789431278592:
        return 'chicken'
    if abs(picHash - 4070829687239942417) < 829687239942417:
        return 'dog'
    if abs(picHash - 10249979888794476929) < 979888794476929:
        return 'monkey'
    if abs(picHash - 8710159644527196208) < 159644527196208:
        return 'cat'
    if abs(picHash - 9230197187512038617) < 1971875120386:
        return 'ox'
    if abs(picHash - 432693552648189798) < 93552648189798:
        return 'frog'
    return 'panda'
def cut(all):
    left, top = 551, 159
    size = 48
    #count = 0
    for i in range(8):
        for j in range(8):
            #room = (left, top, left+size, top+size)
            room = (left+8, top+8, left+size-8, top+size-8)
            img = ImageGrab.grab(room)
            picHash = gethash(img)
            all[i].append(flect(picHash))
            #name = repr(count) + '.png'
            #img.save(name)
            #count += 1
            left += size
        top += size
        left = 551
def gethash(img):
    img = img.resize((8, 8), Image.ANTIALIAS).convert('L')
    avg = reduce(lambda x, y: x + y, img.getdata()) / 64.
    return reduce(lambda x, (y, z): x | (z << y),
                  enumerate(map(lambda i: 0 if i < avg else 1, img.getdata())),
                  0)
def find(all):
    for i in range(8):
        for j in range(8):
            if j+1 < 8 and all[i][j] == all[i][j+1]:
                #left-left
                if j-2 > 0 and all[i][j-2] == all[i][j]:
                    #move from (i,j-2) to (i,j-1)
                    move(i, j-2, i, j-1)
                    return True
                #left-up
                if i-1 > 0 and j-1 > 0 and all[i-1][j-1] == all[i][j]:
                    move(i-1, j-1, i, j-1)
                    return True
                #left-down
                if i+1 < 8 and j-1 > 0 and all[i+1][j-1] == all[i][j]:
                    move(i+1, j-1, i, j-1)
                    return True
                #right-right
                if j+3 < 8 and all[i][j+3] == all[i][j]:
                    move(i, j+3, i, j+2)
                    return True
                #right-up
                if j+2 < 8 and i-1 > 0 and all[i-1][j+2] == all[i][j]:
                    move(i-1, j+2, i, j+2)
                    return True
                #right-down
                if j+2 < 8 and i+1 < 8 and all[i+1][j+2] == all[i][j]:
                    move(i+1, j+2, i, j+2)
                    return True:
            if i+1 < 8 and all[i][j] == all[i+1][j]:
                #up-up
                if i-2 > 0 and all[i-2][j] == all[i][j]:
                    move(i-2, j, i-1, j)
                    return True
                #up-left
                if i-1 > 0 and j-1 > 0 and all[i-1][j-1] == all[i][j]:
                    move(i-1, j-1, i-1, j)
                    return True
                #up-right
                if i-1 > 0 and j+1 < 8 and all[i-1][j+1] == all[i][j]:
                    move(i-1, j+1, i-1, j)
                    return True
                #down-down
                if i+3 < 8 and all[i+3][j] == all[i][j]:
                    move(i+3, j, i+2, j)
                    return True
                #down-left
                if i+2 < 8 and j-1 > 0 and all[i+2][j-1] == all[i][j]:
                    move(i+2, j-1, i+2, j)
                    return True
                #down-right
                if i+2 <8 and j+1 < 8 and all[i+2][j+1] == all[i][j]:
                    move(i+2, j+1, i+2, j)
                    return True
    return false
def move(orx, ory, tax, tay):
    left, top = 551, 159
    size = 48
    ory = top + ory * size + size / 2
    orx = left + orx * size + size / 2
    tay = top + tay * size + size / 2
    tax = left + tax * size + size / 2
    autopy.mouse.move(orx, ory)
    autopy.mouse.toggle(True)
    autopy.mouse.smooth_move(tax, tay)
    autopy.mouse.toggle(False)
    
time.sleep(3)
print 'begin'
t = 1
while t > 0:
    all = [[],[],[],[],[],[],[],[]]
    cut(all)
    find(all)
    t -= 1
print 'over'
'''
autopy.mouse.move(575,183)
autopy.mouse.toggle(True)
autopy.mouse.smooth_move(621,183)
time.sleep(0.1)
autopy.mouse.toggle(False)
'''
