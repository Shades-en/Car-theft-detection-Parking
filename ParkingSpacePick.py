
import cv2
import pickle
 
width, height = 42, 92
x = 32
y = 309

 
try:
    with open('CarPos', 'rb') as f:
        posList = pickle.load(f)
        
except:
    posList = []
 

def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))

    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
 
    with open('CarPos', 'wb') as f:
        pickle.dump(posList, f)
   
 
 
while True:
    img = cv2.imread('first_frame.jpg')
    x = 32
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)
    # while x < img.shape[1]:
    #     cv2.rectangle(img, (x, y), (x + width, y + height), (255, 0, 255), 2)
    #     x+= int(width*1.0476191) 
        
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    if cv2.waitKey(1) & 0xFF==ord('d'):
        break 