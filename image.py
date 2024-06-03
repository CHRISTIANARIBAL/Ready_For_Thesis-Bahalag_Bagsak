import cv2

url = 'http://192.168.0.106:8080/video'
cap = cv2.VideoCapture(url)

while True:
    ret, frame = cap.read()
    
    if frame is not None:
        height, width, _ = frame.shape
        
        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', width, height)
        
        cv2.imshow('frame', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
