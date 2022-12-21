import cv2
import pickle
import cvzone
import numpy as np
import pyzbar.pyzbar as pyzbar
 
cap = cv2.VideoCapture('park3.webm')

cam  = cv2.VideoCapture(0)
 
with open('CarPos', 'rb') as f:
    posList = pickle.load(f)
    
posList.sort(key = lambda item: item[1])

x = False
 
width, height = 42, 92


def detectActivity(imgPro, prevFrame):
    global move_hist
    frame_diff_all = cv2.absdiff(imgPro, prevFrame)
    imgMedian = cv2.medianBlur(frame_diff_all, 5)
    kernel = np.ones((3, 3), np.uint8)
    frame_diff_all = cv2.dilate(imgMedian, kernel, iterations=1)

    id = 0
    
    for pos in posList:
        id+=1
        x, y = pos
      
        frame_diff = frame_diff_all[y:y + height, x:x + width]

        count = cv2.countNonZero(frame_diff)

        if count < 250:
            color = (0, 255, 0)
            thickness = 5
    
        else:
            color = (0, 0, 255)
            thickness = 2
            move_hist.add(str(id))
            if str(id) not in allowed:
                cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)

        if len(move_hist.difference(allowed)) > 0:
            
            move_hist = move_hist.difference(allowed)
            cvzone.putTextRect(img, f'Possible Theft detected at space ID {", ".join(move_hist)}', (25, 50), scale=2,
                                thickness=2, colorR=(0,0,200))

        # cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
  
        cvzone.putTextRect(img, " id: "+ str(id), (x, y + height - 3), scale=0.75,
                           thickness=1, offset=0, colorR=(0,0,0))
 

   
img = cv2.imread('first_frame.jpg')
prevGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
prevBlur = cv2.GaussianBlur(prevGray, (3, 3), 1)
prevCanny = cv2.Canny(prevBlur, 100, 100)

move_hist = set()
allowed = set()

reference = prevCanny.copy()
frame_count = 0
last_frame_count = -50
while True:
    frame_count += 1
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        print("-------------------start-------------------")
        move_hist = set()
        prevCanny = reference.copy()
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frame_count = 0
        last_frame_count = -50

    next, cam_img = cam.read()
    cam_img = cv2.resize(cam_img, (int(cam_img.shape[1] * 0.5), int(cam_img.shape[0] * 0.5)), interpolation=cv2.INTER_CUBIC) 
    

    if (frame_count - last_frame_count) > 50:
        decodedObjects = pyzbar.decode(cam_img)
        for obj in decodedObjects:
            last_frame_count = frame_count
            identity = str(obj.data).strip("b'")
            if identity not in allowed:
                allowed.add(identity)
            else:
                allowed.remove(identity)
    else:
        cvzone.putTextRect(cam_img, f'Successfully scanned for id: {identity}', (25, 50), scale=1,
                            thickness=1, colorR=(0,200,0))
    
    cv2.imshow("image", cam_img)
      
    success, img = cap.read()
    img = cv2.resize(img, (int(img.shape[1]*1.5), int(img.shape[0]*1.5)), interpolation=cv2.INTER_CUBIC)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgCanny = cv2.Canny(imgGray, 100, 100)

    detectActivity(imgCanny, prevCanny)

    prevCanny = imgCanny.copy()
    cv2.imshow("Image", img)

    if cv2.waitKey(5) & 0xFF==ord('d'):
        x=True
        break 