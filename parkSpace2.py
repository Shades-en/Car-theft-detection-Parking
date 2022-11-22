
import cv2
import pickle
import cvzone
import numpy as np
 
# Video feed
# cap = cv2.VideoCapture('carPark.mp4')
cap = cv2.VideoCapture('park3.webm')
 
with open('CarPos', 'rb') as f:
    posList = pickle.load(f)
   
print(posList)
 
width, height = 42, 92
 
 
def checkParkingSpace(imgPro, prevFrame):
    spaceCounter = 0

    frame_diff_all = cv2.absdiff(imgPro, prevFrame)
    imgMedian = cv2.medianBlur(frame_diff_all, 5)
    kernel = np.ones((3, 3), np.uint8)
    frame_diff_all = cv2.dilate(imgMedian, kernel, iterations=1)

    
    # imgMedian2 = cv2.blur(imgPro, (11, 11))
    imgMedian2 = cv2.GaussianBlur(imgPro, (15, 15), 0)
    # imgMedian2 = imgPro
    kernel2 = np.ones((5,5), np.uint8)
    imgMedian_test = cv2.dilate(imgMedian2, kernel2, iterations=1)
   
    cv2.imshow("frame_diff_all", imgMedian_test)
    id = 0
    for pos in posList:
        id+=1
        x, y = pos
 
        # imgDilate = imgDilate[y:y + height, x:x + width]
      
        imgMedian2 = imgMedian_test[y:y + height, x:x + width]
        frame_diff = frame_diff_all[y:y + height, x:x + width]
        # print(imgMedian2.shape)

        countArea = cv2.countNonZero(imgMedian2)

        count = cv2.countNonZero(frame_diff)
  
        
        # if countArea < 3500:
        #     color = (0, 255, 0)
        #     thickness = 5
        #     spaceCounter += 1
            
        # else:
        #     color = (0, 0, 255)
        #     thickness = 2
        #     # print("movement detected for"+ str(id)+ " " + str(countArea))

        if count < 250:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
            
        else:
            color = (0, 0, 255)
            thickness = 2
            print("movement detected for"+ str(id)+ " " + str(count))

        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), color, thickness)
        # cvzone.putTextRect(img, str(countArea)+ " id: "+ str(id), (x, y + height - 3), scale=0.5,
        #                    thickness=1, offset=0, colorR=color)
        cvzone.putTextRect(img, str(count)+ " id: "+ str(id), (x, y + height - 3), scale=0.5,
                           thickness=1, offset=0, colorR=color)
 
    # cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
    #                        thickness=5, offset=20, colorR=(0,200,0))

img = cv2.imread('first_frame.jpg')
prevGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
prevBlur = cv2.GaussianBlur(prevGray, (1, 1), 1)
prevCanny = cv2.Canny(prevBlur, 100, 100)
# prevMedian = cv2.medianBlur(prevCanny, 3)
# prevThreshold = cv2.adaptiveThreshold(prevBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                          cv2.THRESH_BINARY_INV, 25, 16)
# prevMedian = cv2.medianBlur(prevThreshold, 5)
# kernel = np.ones((3, 3), np.uint8)
# prevDilate = cv2.dilate(prevMedian, kernel, iterations=1)
reference = prevCanny.copy()
print(cap)
while True:
    
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        print("-------------------start-------------------")
        # prevCanny = cv2.Canny(prevBlur, 300, 300)
        prevCanny = reference.copy()
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
      
    success, img = cap.read()
    img = cv2.resize(img, (int(img.shape[1]*1.5), int(img.shape[0]*1.5)), interpolation=cv2.INTER_CUBIC)
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (1, 1), 1)
    imgCanny = cv2.Canny(imgBlur, 100, 100)

    # imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                                      cv2.THRESH_BINARY_INV, 25, 16)
    # imgMedian = cv2.medianBlur(imgThreshold, 5)
    # kernel = np.ones((3, 3), np.uint8)
    # imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
 
    checkParkingSpace(imgCanny, prevCanny)
   
    # prevDilate = imgDilate.copy()

    prevCanny = imgCanny.copy()
    cv2.imshow("Image", img)
    # cv2.imshow("Image", imgCanny)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThres", imgMedian)
    if cv2.waitKey(5) & 0xFF==ord('d'):
        break 