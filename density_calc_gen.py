import cv2
import numpy as np 
from diff_density import diff_density
import time
import sys

#DIFFERENT TRAFFIC DENSITY DATA
TRAFFIC = ["EMPTY", "V LIGHT", "LIGHT", "MODERATE", "HIGH", "V HIGH"]
TRAFFIC_TIME = [0.0, 2.0, 3.0, 4.0, 5.0, 6.0]
TRAFFIC_COLOR = [(240,240,240), (0,255,0), (0,128,0), (0,69,255), (0,0,128), (0,0,255)]

#Frame rate of input traffic video is 10, please change for different source
MAX_FPS = 10
#Space separation for each view window
VIEW_MARGIN = 20
WINDOW_TITLE_HEIGHT = 70

# This is to generalize all lanes as they will have different 
# source, bg, roi and traffic
lanes = []
# To add a lane
# lanes.append([SOURCE, BG, X, Y, WIDTH, HEIGHT, TRAFFIC_INDEX, THRESH_RANGES]) 
SRC, BG, X, Y, W, H, TI, TR= range(8)

path = "traffic_video/"
lanes.append([path+"1.avi", 
	path+"1_bg.png",
	450, 0, 100, 540, 0,
	(3, 24, 29, 34, 38)])
lanes.append([path+"2.avi", 
	path+"2_bg.png",
	450, 0, 100, 540, 0,
	(3, 24, 29, 34, 38)])
lanes.append([path+"3.avi", 
	path+"3_bg.png",
	450, 0, 100, 540, 0,
	(3, 24, 29, 34, 38)])
lanes.append([path+"4.avi", 
	path+"4_bg.png",
	450, 0, 100, 540, 0,
	(3, 24, 29, 34, 38)])

no_of_lanes = len(lanes)

#Which lane has green light and corresponding timer
green = 0
timer = 2.0

cam = []
f = []
bg = []
gray = []

#Initializing cam reader lists
for n in range(no_of_lanes):
	cam.append( cv2.VideoCapture(lanes[n][SRC]) )
	ret, frame = cam[n].read()
	if(ret is False):
		print("Video could not be loaded")
		exit()
	f.append( frame )
	gray.append( cv2.cvtColor(f[n], cv2.COLOR_BGR2GRAY))
	bg.append( cv2.imread(lanes[n][BG], 0) )

#For FPS management
max_frame_period = 1.0/MAX_FPS
delay = 0
timet = time.time()
#initializing vars
init_time =timet
final_time =timet

valid = True
while(valid):

	init_time = final_time

	for i in range(no_of_lanes):

		_, f[i] = cam[i].read()
		if f[i] is None:
			print("No video input")
			valid = False
			break

		gray[i] = cv2.cvtColor(f[i], cv2.COLOR_BGR2GRAY)

		d = diff_density(gray[i], bg[i], lanes[i][X], lanes[i][Y], lanes[i][W], lanes[i][H])

		#Calculate traffic index based on d comparing with thresholds
		lanes[i][TI] = 0
		for t in lanes[i][TR]:
			if(d > t):
				lanes[i][TI]+=1

		#Add appropriate traffic message to screen
		if(green == i):
			cv2.putText(f[i], str(round(timer,2)), (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,255), 4)
		else:
			cv2.putText(f[i], TRAFFIC[lanes[i][TI]], (0,50), cv2.FONT_HERSHEY_SIMPLEX, 1, TRAFFIC_COLOR[lanes[i][TI]], 3)

		res = cv2.resize(f[i], None, fx=0.5, fy=0.5, interpolation = cv2.INTER_CUBIC)

		h, w = res.shape[:2]
		cv2.imshow("Lane: " + str(i+1), res)
		cv2.moveWindow("Lane: " + str(i+1), int(i%2)*(w+VIEW_MARGIN), int(i/2)*(h+VIEW_MARGIN+WINDOW_TITLE_HEIGHT))

	k = cv2.waitKey(1)
	if k&255 == 27:
		break

	timet = time.time()
	final_time = timet
	frame_period = final_time - init_time
	extra_time = max_frame_period - frame_period
	delay -= extra_time

	#Creating a delay to stay in MAX_FPS range
	if(delay<0):
		time.sleep((-delay))
		delay=0.0

	timet = time.time()
	final_time = timet
	actual_frame_period = final_time - init_time

	timer = timer - actual_frame_period
	if(timer <= 0.0):
		#Green light to next lane
		green = (green+1)%no_of_lanes
		timer = TRAFFIC_TIME[lanes[green][TI]]

	sys.stdout.write("FPS ")
	sys.stdout.write(str(1/actual_frame_period))
	sys.stdout.write('\r')
	sys.stdout.flush()

#Releasing all vars
for i in range(no_of_lanes):
	cam[i].release()

cv2.destroyAllWindows()