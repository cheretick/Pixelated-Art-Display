import cv2 as cv
import pickle
import numpy as np

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
    frameTemp = cv.resize(frame, (newWidth, newHeight), interpolation=cv.INTER_LINEAR)
    # maybe try different interpolation modes, later
    frame = cv.resize(frameTemp, (width, height), interpolation=cv.INTER_NEAREST)
    return frame

print(" Width: " + str(width) + "\tHeight: " + str(height))

# makes the preview fullscreen
cv.namedWindow("Pixelate", cv.WINDOW_NORMAL)
#cv.setWindowProperty("Pixelate", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

#low = np.array([0,0,0])
#high = np.array([25,25,25])
grey = np.zeros(background.shape, np.uint8)
grey.fill(25)

out = cv.VideoWriter('videos\example.mp4', cv.VideoWriter_fourcc(*'MP4V'), 29.97, (int(width),int(height)))

while(True):
    isTrue, frame = capture.read()
    isTrue, videoCap = video.read()  # uses video as input

    videoCap = cv.resize(videoCap,(int(width),int(height)),fx=0,fy=0, interpolation = cv.INTER_CUBIC)
    frame = videoCap #inserts video into frame instead of webcam

    #frame = foregroundFeed.apply(frame)  # apply the background removal algorithm
    mask = cv.inRange(frame, (0,0,0), (245,245,245))
    mask = pixelate(PIXEL_SIZE, mask)
    invMask = cv.bitwise_not(mask)
    #frame = cv.cvtColor(frame, cv.COLOR_GRAY2BGR) #matches color channel for bitwise_and
    #frame = cv.bitwise_not(frame) #inverts colors

    # pixelates image
    #frame = pixelate(PIXEL_SIZE, frame)

    # normal mask layers
    #foregroundOnly = cv.bitwise_and(grey, grey, mask = invMask)
    #backgroundOnly = cv.bitwise_and(background, background, mask = mask)

    # reverse mask layers
    foregroundOnly = cv.bitwise_and(grey, grey, mask = mask)
    backgroundOnly = cv.bitwise_and(background, background, mask = invMask)

    #camWithBG = cv.bitwise_and(background, background, mask=mask)
    camWithBG = cv.add(foregroundOnly, backgroundOnly)

    # mirrors the frame
    camWithBG = cv.flip(camWithBG, 1)

    cv.imshow('Pixelate', camWithBG)
    #cv.imshow('video', videoCap)
    #cv.imshow('frame', frame)
    #cv.imshow('mask', mask)
    #cv.imshow('foreground', foregroundOnly)
    #cv.imshow('background', backgroundOnly)

    out.write(camWithBG)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

print("done!")
capture.release()
out.release()
cv.destroyAllWindows()