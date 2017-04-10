import os
import random
import cv2
# get all the picture
filenames = os.listdir(os.path.join(os.getcwd(), 'data'))
temp = filenames[:]
data = open("data.txt", "a+")
# data = open("test.txt", "a+")
linecount = 0
# only make 1000 data(enough)
iterations = 1000
for n in range(iterations):
	# randomly take photo between looking and not looking photo
	pos = int(random.random() * (len(filenames) - 1))
	if "look" not in filenames[pos]:
		continue
	print repr(n) + " at " + repr(pos) + ' ' + filenames[pos]
	linecount += 1
	# read the photo
	img = cv2.imread('data/' + filenames[pos])
	heigh, width, depth = img.shape
	# convert the photo to numbers(pixel)
	for h in range(heigh):
		for w in range(width):
			data.write(repr(img[h][w][0]) + " ")
	# and then the label is according the filename
	label = "1"
	if "not" in filenames[pos]:
		label = "0"
	data.write(label + "\n")

	os.remove('data/' + filenames[pos])
	del filenames[pos]

data.close()
print linecount