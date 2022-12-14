import cv2 as cv
import numpy as np
import random

DEMO_MODE = False
PIXEL_SIZE = 5
videoNumber = 1
previousVideo = videoNumber
width = 640
height = 360
counter = random.randint(100,1000)
if DEMO_MODE:
    counter = 0
capture = cv.VideoCapture(2)
foregroundFeed = cv.createBackgroundSubtractorMOG2(history=500, varThreshold= 45, detectShadows=False) # defaults: 500, 16, True
video = cv.VideoCapture("G:\\School\\2022 FALL\\ENGT 4050\\Pixelated-Art-Display\\videos\\" + str(videoNumber) + ".mp4")

# set manual webcam dimensions
capture.set(cv.CAP_PROP_FRAME_WIDTH, width)
capture.set(cv.CAP_PROP_FRAME_HEIGHT, height)
    
# get webcam dimensions
width = capture.get(cv.CAP_PROP_FRAME_WIDTH)
height = capture.get(cv.CAP_PROP_FRAME_HEIGHT)

# get background image
background = cv.imread('generatedImages\generatedImage2.jpg')
background = cv.resize(background, (int(width), int(height)))

def pixelate(pixelSize, frame):
    height = int(frame.shape[0])
    width = int(frame.shape[1])
    newHeight = height//pixelSize
    newWidth = width//pixelSize
    frameTemp = cv.resize(frame, (newWidth, newHeight), interpolation=cv.INTER_NEAREST)
    frame = cv.resize(frameTemp, (width, height), interpolation=cv.INTER_NEAREST)
    return frame

print(" Width: " + str(width) + "\tHeight: " + str(height))

# makes the preview fullscreen
cv.namedWindow("Pixelate", cv.WINDOW_NORMAL)
cv.setWindowProperty("Pixelate", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

# foreground color
grey = np.zeros(background.shape, np.uint8)
grey.fill(25)

# morphology fill size
kernel = np.ones((PIXEL_SIZE, PIXEL_SIZE), np.uint8)

# for plaque
plaque = cv.imread("backgroundWithPlaque.jpg")
plaque = cv.resize(plaque, (int(width), int(height)))
plaqueCounter = 1

while(True):
    if (counter > 0): # use webcam for input
        retCam, frame = capture.read()
        frame = foregroundFeed.apply(frame)  # apply the background removal algorithm
        mask = cv.inRange(frame, 0, 125)
        mask = pixelate(PIXEL_SIZE, mask)
        invMask = cv.bitwise_not(mask)
        foregroundOnly = cv.bitwise_and(grey, grey, mask = invMask)
        backgroundOnly = cv.bitwise_and(background, background, mask = mask)
        counter -= 1
        if counter == 50:
            if (random.randint(1,4) == 1): 
                background = plaque
            else:
                background = cv.imread('generatedImages\generatedImage2.jpg')
                background = cv.resize(background, (int(width), int(height)))
    else: # use prerecorded video as input
        retVideo, frame = video.read()
        if retVideo: 
            mask = cv.inRange(frame, (0,0,0), (245,245,245))
            mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel, iterations=4)
            mask = pixelate(PIXEL_SIZE, mask)
            invMask = cv.bitwise_not(mask)
            foregroundOnly = cv.bitwise_and(grey, grey, mask = mask)
            backgroundOnly = cv.bitwise_and(background, background, mask = invMask)
        else: # when video is over
            while videoNumber == previousVideo:
                videoNumber = random.randint(1,12)
            previousVideo = videoNumber
            video = cv.VideoCapture("G:\\School\\2022 FALL\\ENGT 4050\\Pixelated-Art-Display\\videos\\" + str(videoNumber) + ".mp4")
            if not DEMO_MODE:
                counter = random.randint(100,1000)
            if DEMO_MODE:
                if (random.randint(1,6) == 1) or (plaqueCounter == 0): 
                    background = plaque
                    plaqueCounter -= 1
                else:
                    background = cv.imread('generatedImages\generatedImage2.jpg')
                    background = cv.resize(background, (int(width), int(height)))
                    plaqueCounter = 1
    
    # combines foreground and background
    camWithBG = cv.add(foregroundOnly, backgroundOnly)

    # mirrors the frame
    camWithBG = cv.flip(camWithBG, 1)

    cv.imshow('Pixelate', camWithBG)

    if cv.waitKey(10) & 0xFF == ord('d'):
        DEMO_MODE = True
        print("Demo Mode: ON")
    if cv.waitKey(10) & 0xFF == ord('f'):
        DEMO_MODE = False
        print("Demo Mode: OFF")
    if cv.waitKey(10) & 0xFF == ord('q'):
        break

capture.release()
cv.destroyAllWindows()