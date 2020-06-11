import cv2
import time
import copy
import os.path
start_time = time.time()

def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
	dim = None
	(h, w) = image.shape[:2]

	if width is None and height is None:
		return image
	if width is None:
		r = height / float(h)
		dim = (int(w * r), height)
	else:
		r = width / float(w)
		dim = (width, int(h * r))

	return cv2.resize(image, dim, interpolation=inter)


def cropped(frame):
	height, width = frame.shape[:2]
	#print(height,width)
	start_row, start_col = int(height * .8), int(width * 0)
	end_row, end_col = int(height*1), int(width*1)
	#print(start_row, start_col)
	cropped = frame[start_row:end_row , start_col:end_col]
	return cropped



#for count, filename in enumerate(os.listdir("review")): 

N = 5000
n = 1
for i in range(1,N):
	frame = cv2.imread('./live/'+str(i)+'.jpg',cv2.IMREAD_UNCHANGED)
	if frame is not None:
		frame = ResizeWithAspectRatio(frame, width=500)
		frame = cropped(frame)
		cv2.imwrite('./LT/'+str(n)+'.jpg',frame)
		n = n + 1

print("--- %s seconds ---" % (time.time() - start_time))