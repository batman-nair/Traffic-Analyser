import cv2
import numpy as np

def diff_density(image1, image2, x=0, y=0, w=-1, h=-1):
#Gives how diff image1 is from image2 in a ROI (x,y,width,height)
	if(image1 is None or image2 is None):
		print("Input not compatible", image1, image2)
		exit()
	roi1 = image1[y:y+h, x:x+w]
	roi2 = image2[y:y+h, x:x+w]
	diff_array = cv2.absdiff(roi1, roi2)
	# print(np.sum(diff_array/float(w*h)))
	return np.sum(diff_array/float(w*h))