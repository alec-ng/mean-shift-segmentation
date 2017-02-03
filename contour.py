import cv2, pdb
import numpy as np

def overlayContour(origImg, segImg):
	# binarize
	segImg[segImg != 255] = 0

	canny = cv2.Canny(segImg, 100, 200)

	im2, contours, hierarchy = cv2.findContours(canny.copy(), \
		cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

	cv2.drawContours(origImg, contours, -1, (0, 0, 255), 1)

	return origImg