import cv2 as cv
import pickle
import numpy as np
import random

PIXEL_SIZE = 10
# set width and height to 'None' to automatically set resolution
# the webcam driver will likely select the closest available resolution when using a custom value
width = 1280
height = 720
capture = cv.VideoCapture(1)
foregroundFeed = cv.createBackgroundSubtractorMOG2(history=500, varThreshold= 60, detectShadows=False) # defaults: 500, 16, True
video = cv.VideoCapture("G:\\School\\2022 FALL\\ENGT 4050\\videos\\edited\\test.mp4")


if width == None or height == None:
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

grey = np.zeros(background.shape, np.uint8)
grey.fill(25)

kernel = np.ones((PIXEL_SIZE, PIXEL_SIZE), np.uint8)

#out = cv.VideoWriter('videos\example.mp4', cv.VideoWriter_fourcc(*'MP4V'), 29.97, (int(width),int(height)))

counter = 100

while(True):
    if (counter > 0):
        retCam, frame = capture.read()
        frame = foregroundFeed.apply(frame)  # apply the background removal algorithm
        mask = cv.inRange(frame, 0, 125)
        mask = pixelate(PIXEL_SIZE, mask)
        invMask = cv.bitwise_not(mask)
        foregroundOnly = cv.bitwise_and(grey, grey, mask = invMask)
        backgroundOnly = cv.bitwise_and(background, background, mask = mask)
        counter -= 1
        if counter == 0: # load next video
            video = cv.VideoCapture("G:\\School\\2022 FALL\\ENGT 4050\\videos\\edited\\test.mp4")
    else:
        retVideo, frame = video.read()  # uses video as input
        foregroundOnly = cv.bitwise_and(grey, grey, mask = mask)
        backgroundOnly = cv.bitwise_and(background, background, mask = invMask)

        # use for prerecorded videos
        if retVideo:
            mask = cv.inRange(frame, (0,0,0), (245,245,245))
            mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel, iterations=4)
            mask = pixelate(PIXEL_SIZE, mask)
            invMask = cv.bitwise_not(mask)
        else:
            print("not retVideo")
            counter = random.randint(100,1000)
    
    camWithBG = cv.add(foregroundOnly, backgroundOnly)

    # mirrors the frame
    camWithBG = cv.flip(camWithBG, 1)

    cv.imshow('Pixelate', camWithBG)
    #cv.imshow('video', videoCap)
    #cv.imshow('frame', frame)
    #cv.imshow('mask', mask)
    #cv.imshow('foreground', foregroundOnly)
    #cv.imshow('background', backgroundOnly)

    #out.write(camWithBG)
    
    if cv.waitKey(30) & 0xFF == ord('q'):
        break


capture.release()
#out.release()
cv.destroyAllWindows()