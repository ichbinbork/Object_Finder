import cv2
import numpy as np

hsv = None # Initialize hsv
lower = [] # lower bound of the color we want to detect
upper = [] # upper bound of the color we want to detect

cv2.namedWindow("Trackbar") # Create a window for the trackbars
def nothing(x):
	pass

def findcolor(event, x, y, flags, param): # This function is used to find the color we want to detect
	global lower, upper, hsv # Global variables
	if event == cv2.EVENT_LBUTTONDOWN: # If left mouse button is clicked trackbars will be created
		lower = [] # lower bound of the color we want to detect
		upper = [] # upper bound of the color we want to detect
		pixel = hsv[y, x] # Get the pixel at the position x, y
		upper.append([(pixel[0]+30), pixel[1]+30, pixel[2]+30]) # Add the upper bound of the color we want to detect
		lower.append([(pixel[0]-30), pixel[1]-30, pixel[2]-30]) # Add the lower bound of the color we want to detect
		cv2.createTrackbar('Low Hue','Trackbar', int(lower[0][0]), 360, nothing) # Create a trackbar for the lower Hue bound of the color we want to detect
		cv2.createTrackbar('High Hue','Trackbar', int(upper[0][0]), 360, nothing) # Create a trackbar for the upper Hue bound of the color we want to detect

		cv2.createTrackbar('Low Saturation','Trackbar', int(lower[0][1]), 255, nothing) # Create a trackbar for the lower Saturation bound of the color we want to detect
		cv2.createTrackbar('High Saturation','Trackbar', int(upper[0][1]), 255, nothing) # Create a trackbar for the upper Saturation bound of the color we want to detect

		cv2.createTrackbar('Low Value','Trackbar', int(lower[0][2]), 255, nothing) # Create a trackbar for the lower Value bound of the color we want to detect
		cv2.createTrackbar('High Value','Trackbar', int(upper[0][2]), 255, nothing) # Create a trackbar for the upper Value bound of the color we want to detect


cv2.namedWindow("Detection") # Create a window for the image

cv2.setMouseCallback("Detection", findcolor) # Set the mouse callback for the window x


cap = cv2.VideoCapture(0) # Initialize the camera or video file

track = np.zeros((300,500)) # Create a black image for the trackbars
while True:
	_, frame = cap.read() # Read the frame
	blur = cv2.GaussianBlur(frame, (5,5), 0) # Blur the frame

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert the frame to HSV

	if len(lower) != 0:

		lh = cv2.getTrackbarPos('Low Hue', 'Trackbar') # Get the lower Hue bound from the trackbar
		hh = cv2.getTrackbarPos('High Hue', 'Trackbar') # Get the upper Hue bound from the trackbar

		ls = cv2.getTrackbarPos('Low Saturation', 'Trackbar') # Get the lower Saturation bound from the trackbar
		hs = cv2.getTrackbarPos('High Saturation', 'Trackbar') # Get the upper Saturation bound from the trackbar

		lv = cv2.getTrackbarPos('Low Value', 'Trackbar')# Get the lower Value bound from the trackbar
		hv = cv2.getTrackbarPos('High Value', 'Trackbar')# Get the upper Value bound from the trackbar

		mask = cv2.inRange(hsv, np.array([lh, ls, lv]), np.array([hh, hs, hv])) # Create a mask according to the hsv threshold values
		cv2.imshow("Masked", mask) # Show the mask
		contors, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # Find the contours of the object we want to detect

		if contors: # If contors exist 
			contors = max(contors, key=cv2.contourArea) # Get the largest contour

			x,y,w,h = cv2.boundingRect(contors) # Get the bounding rectangle of the object
			cv2.rectangle(frame, (x,y), (x+w,y+h), (0,119,255), 2) # Draw a rectangle around the object
			cv2.putText(frame, "Object", (x, y - 5),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2) # Put text on the frame
															# (x, y - 5) is the position of the text
															# cv2.FONT_HERSHEY_SIMPLEX is the font of the text
															# 0.5 is the size of the text
															# (255,255,255) is the color of the text
															# 2 is the thickness of the text
	#cv2.imshow("HSV_FORMAT", hsv)
	cv2.imshow("Detection", frame)
	cv2.imshow("Trackbar", track)

	if cv2.waitKey(10) == ord('q'): # If q is pressed exit the program
		cap.release()
		cv2.destroyAllWindows()
		break