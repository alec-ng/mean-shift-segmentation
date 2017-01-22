from meanshift import segmentImage

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

	(cluster_human, cluster_background, seg_human) = 
		segmentImage(bgImg, humImg, spatial_rad, range_rad, density)

	# save results
	cv2.imwrite("result/cluster_human.jpg", cluster_human)
	cv2.imwrite("result/cluster_background.jpg", cluster_background)
	cv2.imwrite("result/result.jpg", seg_human)