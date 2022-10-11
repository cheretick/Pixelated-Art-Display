from asyncio.windows_events import NULL
import cv2 as cv
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import pickle

PIXEL_SIZE = 15
# set width and height to NULL to automatically set resolution
width = NULL
height = NULL
capture = cv.VideoCapture(0)


if width == NULL or height == NULL:
    # opens resolutions.data and adds them to resolutions list (up to 1080p)
    resolutions = []
    with open('./resolutions.data', 'rb') as fileHandle:
        resolutions = pickle.load(fileHandle)

    # tries each common resolution. this will set the resolution to the highest available resolution
    resolutionsMap = {}
    for i in range(len(resolutions)):
        capture.set(cv.CAP_PROP_FRAME_WIDTH, resolutions[i][0])
        capture.set(cv.CAP_PROP_FRAME_HEIGHT, resolutions[i][1])
        currentWidth = capture.get(cv.CAP_PROP_FRAME_WIDTH)
        currentHeight = capture.get(cv.CAP_PROP_FRAME_HEIGHT)
        resolutionsMap[str(currentWidth)+"x"+str(currentHeight)] = "OK"
    print("Possible resolutions: " + str(resolutionsMap))
else:
    # set manual webcam dimensions
    capture.set(cv.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    print("-Custom resolution is being used-")
    

# get webcam dimensions
width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)

# get background image
background = cv.imread('generatedImages\generatedImage2.jpg')
background = cv.resize(background, (int(width), int(height)))

segmentor = SelfiSegmentation()

def pixelate(pixelSize, frame):
    height = int(frame.shape[0])
    width = int(frame.shape[1])
    newHeight = height//pixelSize
    newWidth = width//pixelSize
    frameTemp = cv.resize(frame, (newWidth, newHeight), interpolation=cv.INTER_LINEAR)
    # maybe try different interpolation modes, later
    frame = cv.resize(frameTemp, (width, height), interpolation=cv.INTER_NEAREST)
    return frame

print(" Width: " + str(width) + "\tHeight: " + str(height))

# makes the preview fullscreen
cv.namedWindow("Pixelate", cv.WINDOW_NORMAL)
cv.setWindowProperty("Pixelate", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

while(True):
    isTrue, frame = capture.read()

    # changes colorspace to grayscale
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # reverts back to BGR because segmentor needs 3 color channels
    frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR) 

    # removes background
    camWithBG = segmentor.removeBG(frame, background, threshold=0.9)

    # pixelates image
    camWithBG = pixelate(PIXEL_SIZE, camWithBG)

    # mirrors the frame
    camWithBG = cv.flip(camWithBG, 1)

    cv.imshow('Pixelate', camWithBG)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()