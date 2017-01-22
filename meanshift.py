# Author: Alec
# Jan 17, 2017

import sys, os, pdb, numpy
import numpy as np
import cv2
import pymeanshift as pms
from PIL import Image


# SUMMARY: saves 3 pictures: clustering results on picture with human/background and
#	final segmented human 

# PARAM bgImg: numpy array of background
# PARAM humImg: numpy array of human in front of background

# PARAM spatial_rad: [meanshift] search magnitude 
# PARAM range_rad: [meanshift] colour treshold to classify as part of cluster
# PARAM density: [meanshift] min num. of points that comprises a cluster

# PARAM hueThreshold: [segmentation] tolerance to match clusters based on colour
# PARAM spatialThreshold: [segmentation] tolerance to match clusters based on avg X/Y coords

# RETURN (cluster_human, cluster_background, seg_human) tuple of numpy arrays

def segmentImage(bgImg, humImg, spatial_rad, range_rad, density, hueThresh, spatialThresh):

	# perform mean shift clustering on both images
	(seg_bg, labels_bg, regions_bg) = pms.segment(bgImg, spatial_rad, range_rad, density)
	(seg_hum, labels_hum, regions_hum) = pms.segment(humImg, spatial_rad, range_rad, density)

	# display num clusters found
	print('regions_bg: ' + str(regions_bg))
	print('regions_hum: ' + str(regions_hum))

	# analyze clusters for colour
	bg_label_avg = calcAverage(bgImg, labels_bg)
	hum_label_avg = calcAverage(humImg, labels_hum)

	segmented_labels = []
	for ind_bg, bg_avg_tuple in enumerate(bg_label_avg):
		for ind_hum, hum_avg_tuple in enumerate(hum_label_avg):
			if abs(bg_avg_tuple[0] - hum_avg_tuple[0]) <= hueThresh and \
				abs(bg_avg_tuple[1] - hum_avg_tuple[1]) <= hueThresh and \
				abs(bg_avg_tuple[2] - hum_avg_tuple[2]) <= hueThresh and \
				abs(bg_avg_tuple[3] - hum_avg_tuple[3]) <= spatialThresh and \
				abs(bg_avg_tuple[4] - hum_avg_tuple[4]) <= spatialThresh:

				segmented_labels.append(ind_hum)

	# segment background clusters from human image
	for row in range(0, labels_bg.shape[0]):
		for column in range(0, labels_bg.shape[1]):
			if labels_hum[row][column] in segmented_labels:
				humImg[row][column][0] = 255 # white out
				humImg[row][column][1] = 255 # all channels
				humImg[row][column][2] = 255 

	return (seg_hum, seg_bg, humImg)


# SUMMARY: given a label, go to original image and calculate average RBG, x and y coord 
#	of pixels in that cluster
# PARAM img: original image read from cv2
# PARAM labels: obtained from pms.segment()
# RETURNS: (avgR, avgG, avgB, avgX, avgY)
def calcAverage(img, labels):
	avgColours = []
	for label in numpy.unique(labels):
		avgHue_R = 0
		avgHue_G = 0
		avgHue_B = 0
		avgX = 0
		avgY = 0
		coords = numpy.where(labels == label)

		for ind in range(0, coords[0].size-1):
			x = coords[0][ind]
			y = coords[1][ind]
			numPixelsInCluster = coords[0].size
			avgHue_R += img[x][y][0] 
			avgHue_G += img[x][y][1]
			avgHue_B += img[x][y][2]
			avgX += x
			avgY += y

		avgHue_R /= numPixelsInCluster
		avgHue_G /= numPixelsInCluster
		avgHue_B /= numPixelsInCluster
		avgX /= numPixelsInCluster
		avgY /= numPixelsInCluster
		avgColours.append((avgHue_R, avgHue_G, avgHue_B, avgX, avgY))

	return avgColours


# Boilerplate
##########################################################

if __name__ == "__main__":
	if (len(sys.argv) != 6):
		raise Exception("Invalid number of params")

	bgImg_Path = sys.argv[1]
	humImg_Path = sys.argv[2]
	spatial_rad = int(sys.argv[3])
	range_rad = int(sys.argv[4])
	density = int(sys.argv[5])

	bgImg = cv2.imread(bgImg_Path)
	humImg = cv2.imread(humImg_Path)

	# resize to 500px wide, keep original aspect ratio
	ratio = 500.0 / bgImg.shape[1]
	dimension = (500, int(bgImg.shape[0] * ratio))
	bgImg = cv2.resize(bgImg, dimension, interpolation = cv2.INTER_AREA)
	humImg = cv2.resize(humImg, dimension, interpolation = cv2.INTER_AREA)

	segmentImage(bgImg, humImg, spatial_rad, range_rad, density)
