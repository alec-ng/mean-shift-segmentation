# Author: Alec
# Jan 17, 2017

import sys, os, pdb, numpy, math
import numpy as np
import cv2
import pymeanshift as pms
from PIL import Image

# 5 5 200 30 for oliver
# 5 13 200 30 for alec


# SUMMARY: saves 3 pictures: clustering results on picture with human/background and
#	final segmented human 

# PARAM bgImg: numpy array of background
# PARAM humImg: numpy array of human in front of background

# PARAM spatial_rad: [meanshift] search magnitude 
# PARAM range_rad: [meanshift] colour treshold to classify as part of cluster
# PARAM density: [meanshift] min num. of points that comprises a cluster

# PARAM deltEThresh: [segmentation] tolerance for delta E for 2 LAB pixels

# RETURN (cluster_human, cluster_background, seg_human) tuple of numpy arrays

def segmentImage(bgImg, humImg, spatial_rad, range_rad, density, deltEThresh):

	# perform mean shift clustering on both images
	(seg_bg, labels_bg, regions_bg) = pms.segment(bgImg, spatial_rad, range_rad, density)
	(seg_hum, labels_hum, regions_hum) = pms.segment(humImg, spatial_rad, range_rad, density)

	# display num clusters found
	print('regions_bg: ' + str(regions_bg))
	print('regions_hum: ' + str(regions_hum))

	# convert to LAB colour space
	lab_seg_bg = cv2.cvtColor(seg_bg, cv2.COLOR_BGR2LAB)
	lab_seg_hum = cv2.cvtColor(seg_hum, cv2.COLOR_BGR2LAB)

	for row in range(0, humImg.shape[0]):
		for column in range(0, humImg.shape[1]):
		
			diff = deltaE(seg_hum[row][column], seg_bg[row][column])

			if diff < deltEThresh:
				humImg[row][column][0] = 255 # white out
				humImg[row][column][1] = 255 # all channels
				humImg[row][column][2] = 255 

	return (seg_hum, seg_bg, humImg)

# calculate deltaE between two LAB pixels
# return scalar
def deltaE(p1, p2):
	l_squareDiff = (int(p1[0]) - int(p2[0]))**2
	a_squareDiff = (int(p1[1]) - int(p2[1]))**2
	b_squareDiff = (int(p1[2]) - int(p2[2]))**2

	return math.sqrt(l_squareDiff + a_squareDiff + b_squareDiff)


# Boilerplate
##########################################################

if __name__ == "__main__":
	if (len(sys.argv) != 7):
		raise Exception("Invalid number of params")

	bgImg_Path = sys.argv[1]
	humImg_Path = sys.argv[2]
	spatial_rad = int(sys.argv[3])
	range_rad = int(sys.argv[4])
	density = int(sys.argv[5])
	deltEThresh = int(sys.argv[6])

	bgImg = cv2.imread(bgImg_Path)
	humImg = cv2.imread(humImg_Path)

	# resize to 500px wide, keep original aspect ratio
	ratio = 500.0 / bgImg.shape[1]
	dimension = (500, int(bgImg.shape[0] * ratio))
	bgImg = cv2.resize(bgImg, dimension, interpolation = cv2.INTER_AREA)
	humImg = cv2.resize(humImg, dimension, interpolation = cv2.INTER_AREA)

	segmentImage(bgImg, humImg, spatial_rad, range_rad, density, deltEThresh)
