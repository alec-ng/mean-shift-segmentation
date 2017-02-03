import sys, os, pdb, numpy, math
import numpy as np
import cv2
import pymeanshift as pms
from PIL import Image

def segmentImage(bgImg, humImg, spatial_rad, range_rad, density, clusterThresh, labThresh):

	# perform mean shift clustering on both images
	(seg_bg, labels_bg, regions_bg) = pms.segment(bgImg, spatial_rad, range_rad, density)
	(seg_hum, labels_hum, regions_hum) = pms.segment(humImg, spatial_rad, range_rad, density)

	# display num clusters found
	print('regions_bg: ' + str(regions_bg))
	print('regions_hum: ' + str(regions_hum))

	# convert to LAB colour space
	lab_seg_bg = cv2.cvtColor(seg_bg, cv2.COLOR_BGR2LAB)
	lab_seg_hum = cv2.cvtColor(seg_hum, cv2.COLOR_BGR2LAB)
	lab_humImg = cv2.cvtColor(humImg, cv2.COLOR_BGR2LAB)
	lab_bgImg = cv2.cvtColor(bgImg, cv2.COLOR_BGR2LAB)

	threshImg = np.empty_like(humImg)
	meanshiftImg = np.empty_like(humImg)
	threshImg[:] = humImg
	meanshiftImg[:] = humImg

	for row in range(0, humImg.shape[0]):
		for col in range(0, humImg.shape[1]):
		
			# while looking at background pixel, look at range of human pixels
			# to account for slight translation invariances
			seg_bg_pixel = seg_bg[row][col]
			lab_bgImg_pixel = lab_bgImg[row][col]

			meanshift_deltas = getOffsetDeltas(seg_hum, col, row, seg_bg_pixel)
			threshold_deltas = getOffsetDeltas(lab_humImg, col, row, lab_bgImg_pixel)

			do_seg_cluster = any(x < clusterThresh for x in meanshift_deltas)
			do_seg_thresh = any(x < labThresh for x in threshold_deltas)

			if do_seg_cluster or do_seg_thresh:
				humImg[row][col][0] = 255 # white out
				humImg[row][col][1] = 255 # all channels
				humImg[row][col][2] = 255 
			
			# save intermediate threshold photo for analysis
			if do_seg_thresh:
				threshImg[row][col][0] = 255 
				threshImg[row][col][1] = 255 
				threshImg[row][col][2] = 255 

			# save intermediate mean shift clustering photo for analysis
			if do_seg_cluster:
				meanshiftImg[row][col][0] = 255 
				meanshiftImg[row][col][1] = 255 
				meanshiftImg[row][col][2] = 255

	return (seg_hum, seg_bg, humImg, threshImg, meanshiftImg)


def getOffsetDeltas(img, col, row, pixel_compare):
	offset = 2

	low = abs(offset - row)
	if row + offset > (img.shape[0] - 1):
		high = img.shape[0] - 1
	else:
		high = row + offset

	deltas = []
	for index in range(low, high + 1):
		deltas.append(deltaE(pixel_compare, img[index][col]))

	return deltas


# calculate deltaE between two LAB pixels
# return scalar
def deltaE(p1, p2):
	l_squareDiff = (int(p1[0]) - int(p2[0]))**2
	a_squareDiff = (int(p1[1]) - int(p2[1]))**2
	b_squareDiff = (int(p1[2]) - int(p2[2]))**2

	return math.sqrt(l_squareDiff + a_squareDiff + b_squareDiff)
