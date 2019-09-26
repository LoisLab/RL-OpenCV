import numpy as np
import argparse
import cv2

ap = argparse.ArgumentParser()
ap.add_argument('-i', '--image', help='path to image')
args = vars(ap.parse_args())

image = cv2.imread(args['image'])

boundaries = [
	([0x2c, 0xbd, 0xfa], [0x2c, 0xbd, 0xfa]),
	([0x3d, 0x48, 0xe8], [0x3d, 0x48, 0xe8]),
	([25, 146, 190], [62, 174, 250]),
	([103, 86, 65], [145, 133, 128])
]

for (lower, upper) in boundaries:
	# create NumPy arrays from the boundaries
	lower = np.array(lower, dtype = "uint8")
	upper = np.array(upper, dtype = "uint8")

	# find the colors within the specified boundaries and apply
	# the mask
	mask = cv2.inRange(image, lower, upper)
	output = cv2.bitwise_and(image, image, mask = mask)

	# show the images
	cv2.imshow("images", np.hstack([image, output]))
	cv2.waitKey(0)
