import cv2 as cv

# videoPath = "carPark.mp4"
videoPath = "park3.webm"

def getFirstFrame(videofile):
    vidcap = cv.VideoCapture(videofile)
    success, image = vidcap.read()
    image = cv.resize(image, (int(image.shape[1]*1.5), int(image.shape[0]*1.5)), interpolation=cv.INTER_CUBIC)
    if success:
        cv.imwrite("first_frame.jpg", image)  # save frame as JPEG file

getFirstFrame(videoPath)

