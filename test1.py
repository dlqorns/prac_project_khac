import mediapipe as mp
import cv2 as cv

videoFile = 'WIN_20230608_13_11_31_Pro.mp4' 
cap = cv.VideoCapture(videoFile) #load as a VideoCapture class

while(cap.isOpened()): #Check Video is Available
	ret, frame = cap.read() #read by frame (ret=TRUE/FALSE)

	if ret:
		cv.imshow('jeongIN', frame)
		if cv.waitKey(10) & 0xFF == ord('a'): #wait 10ms until user input
			break
	else:
		print("ret is false")
		break

cap.release() #release memory
cv.destroyAllWindows() #destroy All Window