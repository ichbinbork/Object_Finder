
import cv2
import numpy as np
	

cap = cv2.VideoCapture(0) # Our webcam or video file
while True:

	_, frame = cap.read() # Read the frame

	blur = cv2.GaussianBlur(frame, (5,5), 0) #Blur the frame for better detection

	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV) # Convert the frame to HSV

	mask = cv2.inRange(hsv, np.array([0, 0, 10]), np.array([160, 200,25])) #Create a numpy array color we want to detect
																		   # 0, 0, 10 is the lower bound and 160, 200, 25 is the upper bound these values can be changed to detect different colors
																		   # We want to detect the color from black to white
																		   # We can change the values to detect other colors
																		   # We can also use the cv2.inRange function to detect the color
	cv2.imshow("Masked Frame", mask)

	contors, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE) # Find the contours of the object we want to detect

	if contors: # If there are contours in frame below snippet will execute

		if cv2.waitKey(20) == ord('2'): # If we press 2 then program detects the object

			contors = max(contors, key=cv2.contourArea) # Find the contour with maximum area
														# cv2.contourArea is a function that returns the area of the contour
															
			x,y,w,h = cv2.boundingRect(contors) # Find the bounding rectangle of the contour

			print(x,y,w,h) # Print the bounding rectangle of the contour

			cv2.rectangle(frame, (x,y), (x+w,y+h), (0,119,255), 2) # Draw a rectangle around the contour
		    													   # 0, 119, 255 is the color of the rectangle
																   # 2 is the thickness of the rectangle
																   # We can change the values to draw other colors
			cv2.putText(frame, "Object", (x, y - 5),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2) # Put text on the frame
															# (x, y - 5) is the position of the text
															# cv2.FONT_HERSHEY_SIMPLEX is the font of the text
															# 0.5 is the size of the text
															# (255,255,255) is the color of the text
															# 2 is the thickness of the text
	cv2.imshow("HSV", hsv)
	cv2.imshow("Captured_Object", frame)
	if cv2.waitKey(10) == ord('q'): # If we press q then program quits
		cap.release()
		cv2.destroyAllWindows()

		break 