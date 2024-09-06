# 物体跟踪
import cv2
tracker = cv2.TrackerCSRT_create()
tracking = False
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    if cv2.waitKey(1) == ord('a'):
        tracking = True
        roi = cv2.selectROI('Tracking', frame, False)
        tracker.init(frame, roi)
    if tracking:
        success,box = tracker.update(frame)
        if success:
            x,y,w,h = box
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(frame,"tracking",(x,y-10),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255),5)
    cv2.imshow('Tracking', frame)
    cv2.waitKey(1)
cap.release()
cv2.destroyAllWindows()
