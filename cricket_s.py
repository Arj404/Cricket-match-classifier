import cv2
import time
import copy
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



def video_capture(url,f):
	cap = cv2.VideoCapture(url)
	count = 0
	f_list = []
	height = 0
	width = 0
	while cap.isOpened():
		ret,frame = cap.read()
		if ret == True:
			#print(frame.shape)
			#if(count==2):
				#cv2.imwrite('kang.jpg',frame)

			if(count%f==0):
				r_frame = ResizeWithAspectRatio(frame, height=1000)
				f_list.append(r_frame)
			count = count + 1
			if cv2.waitKey(10) & 0xFF == ord('q'):
				break
		else:
			break
	cap.release()
	return f_list


def video_generate(f_list,name,fps):
	(he, wi) = f_list[0].shape[:2]
	out = cv2.VideoWriter(name,0,fps, (wi,he))
	for i in range(len(f_list)):
		out.write(f_list[i])
	out.release()


def pre_process(f_list):
	p_list = []
	for i in f_list:
		#g_image = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
		height, width = i.shape[:2]
		start_row, start_col = int(height * .8), int(width * 0)
		end_row, end_col = int(height*1), int(width*1)
		cropped = i[start_row:end_row , start_col:end_col]
		p_list.append(cropped)
	return p_list


def live_detection(f_list):
	image_template1 = cv2.imread('image.png')
	image_template1 = cv2.cvtColor(image_template1, cv2.COLOR_BGR2GRAY)
	#image_template2 = cv2.imread('image2.png')
	#image_template2 = cv2.cvtColor(image_template2, cv2.COLOR_BGR2GRAY)
	x_list = []
	c1=0
	c2=0
	for frame in f_list:
		height, width = frame.shape[:2]
		im = copy.copy(frame)
		top_left_x,top_left_y = int(height * .8), int(width * 0)
		bottom_right_x,bottom_right_y = int(height*1), int(width*1)

		cv2.rectangle(frame, (top_left_y,top_left_x), (bottom_right_y,bottom_right_x), (127,50,127), 3)
		cropped = frame[top_left_x:bottom_right_x , top_left_y:bottom_right_y]

		image1 = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
		orb1 = cv2.ORB_create(1000, 1.2, 8, 15, 0,2)
		#orb2 = cv2.ORB_create(1000, 1.2, 8, 15, 0,2)
		kp1, des1 = orb1.detectAndCompute(image1, None)
		kp2, des2 = orb1.detectAndCompute(image_template1, None)
		#kp3, des3 = orb2.detectAndCompute(image1, None)
		#kp4, des4 = orb2.detectAndCompute(image_template2, None)
		bf1 = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
		#bf2 = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
		matches1 = bf1.match(des1,des2)
		matches1 = sorted(matches1, key=lambda val: val.distance)
		matches1 = len(matches1)

		#matches2 = bf2.match(des3,des4)
		#matches2 = sorted(matches2, key=lambda val: val.distance)
		#matches2 = len(matches2)
		
		output_string = str(matches1)
		cv2.putText(frame, output_string, (20,20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
		threshold1 = 200
		#threshold2 = 65
		if matches1 > threshold1:
			cv2.putText(frame,'L',(140,20), cv2.FONT_HERSHEY_COMPLEX, 2 ,(255,0,0), 2)
			cv2.imwrite('./live/image5L'+str(c1)+'.jpg',im)
			c1=c1+1
		else:
			cv2.putText(frame,'R',(140,20), cv2.FONT_HERSHEY_COMPLEX, 2 ,(0,0,255), 2)
			cv2.imwrite('./review/image5R'+str(c2)+'.jpg',im)
			c2=c2+1
		x_list.append(frame)
	return x_list


v_url = './Video6.mp4'
f_list = []
p_list = []
f_list= video_capture(v_url,5)
print(f_list[0].shape)
#p_list = pre_process(frame_list)


p_list = live_detection(f_list)

#video_generate(p_list,'pre.avi',10)

cv2.destroyAllWindows()
print("--- %s seconds ---" % (time.time() - start_time))