import cv2 as cv
from tracker import *

# videoPath = "carPark.mp4"
videoPath = "park3.webm"

tracker = EuclideanDistTracker()



def getFirstFrame(videofile):
    vidcap = cv.VideoCapture(videofile)
    
    success, image = vidcap.read()
    print(int(image.shape[0]*1.15))
    #resize image
    image = cv.resize(image, (int(image.shape[1]*1.5), int(image.shape[0]*1.5)), interpolation=cv.INTER_CUBIC)
    # #crop image
    # image = image[image.shape[0] - int(image.shape[0]*0.5): , : ] 
    if success:
        cv.imwrite("first_frame.jpg", image)  # save frame as JPEG file


def getEdges(img):
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    blur = cv.GaussianBlur(gray, (11, 11), 0)
    # cv.imshow ("blur", blur)
    # canny = cv.Canny(blur, 150, 150)
    # return canny
    return blur


getFirstFrame(videoPath)

img = cv.imread("first_frame.jpg")
reference = getEdges(img)
reference = cv.Canny(reference, 110, 120)
cv.imshow("reference", reference)
contours, hierarchy = cv.findContours(reference, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# cv.drawContours(img, contours, -1, (0, 255, 0), 3)
for c in contours:
    if cv.contourArea(c) < 100:
        continue
    x, y, w, h = cv.boundingRect(c)
    cv.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv.imshow("contours", img)

# cv.imshow('Canny Edges ', reference)

cv.waitKey(0)


# capture = cv.VideoCapture(videoPath)
# frame_count = 0 
# consecutive_frame = 1
# prevFrame = None

# while True:
#     isTrue, frame = capture.read()
    
#     if isTrue:   
#         frame_count += 1
#         frame = cv.resize(frame, (1000,700), interpolation=cv.INTER_CUBIC)
#         # cv.imshow('Video', frame)
#         frame = frame[frame.shape[0] - int(frame.shape[0]*0.5): , : ]
#         orig_frame = frame.copy()
#         currentCanny = getEdges(frame)
#         cv.imshow('Canny Edges ', currentCanny)
#         if frame_count % consecutive_frame == 0 or frame_count == 1:
#             frame_diff_list = []
      
#         # frameDiff = currentCanny - reference
#         if(prevFrame is None):
#             frameDiff = cv.absdiff(currentCanny, reference)
#         else:
#             frameDiff = cv.absdiff(currentCanny, prevFrame)

#         prevFrame = currentCanny
#         cv.imshow('diff ', frameDiff)
#         frame_diff_list.append(frameDiff)
#         if len(frame_diff_list) == consecutive_frame:
#             sum_frames = sum(frame_diff_list)
#             contours, hierarchy = cv.findContours(sum_frames, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
#             detections = []
#             for contour in contours:
#                 # continue through the loop if contour area is less than 500...
#                 # ... helps in removing noise detection
#                 if cv.contourArea(contour) < 12000:
#                     continue
#                 # get the xmin, ymin, width, and height coordinates from the contours
#                 (x, y, w, h) = cv.boundingRect(contour)
#                 if w<frameDiff.shape[1]*0.2 and h<frameDiff.shape[0]*0.5:
#                     cv.rectangle(orig_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                 if w > 30 and h > 30:
#                     # cv.rectangle(orig_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#                     detections.append([x, y, w, h])
                
#             boxes_ids = tracker.update(detections)

#             # for box_id in boxes_ids:
#             #     x, y, w, h, id = box_id
#             #     if w > 30 and h > 30:
#             #         cv.rectangle(orig_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
#             #         cv.putText(orig_frame, "Movement Detected for "+str(id), (10, 20), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
#             #         print(id)
#             cv.imshow('Detected Objects', orig_frame)

#             if cv.waitKey(20) & 0xFF==ord('d'):
#                 break            
#     else:
#         break

# capture.release()
cv.destroyAllWindows()