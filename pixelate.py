import cv2 as cv

PIXEL_SIZE = 15
APPLY_BACKGROUND_SUBTRACTOR = True
APPLY_PIXELATE = True

capture = cv.VideoCapture(0) # try cv.VideoCapture(0) if you aren't getting input
print("Capture Input--\theight: " + str(capture.get(4)) + "\twidth: " 
    + str(capture.get(3)) + "\tframerate: " + str(capture.get(5)))

foregroundFeed = cv.createBackgroundSubtractorMOG2()

def pixelate(pixelSize, frame):
    height = int(frame.shape[0])
    width = int(frame.shape[1])
    newHeight = height//pixelSize
    newWidth = width//pixelSize
    frameTemp = cv.resize(frame, (newWidth, newHeight), interpolation=cv.INTER_LINEAR)
    # maybe try different interpolation modes, later
    frame = cv.resize(frameTemp, (width, height), interpolation=cv.INTER_NEAREST)
    return frame

# makes the preview fullscreen
cv.namedWindow("preview", cv.WINDOW_NORMAL)
cv.setWindowProperty("preview", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)

while True:
    # captures a frame
    isTrue, frame = capture.read()
    
    if APPLY_BACKGROUND_SUBTRACTOR:
        frame = foregroundFeed.apply(frame)
    
    # pixelates the frame
    if APPLY_PIXELATE:
        frame = pixelate(PIXEL_SIZE, frame)

    # mirrors the frame
    frame = cv.flip(frame, 1)

    cv.putText(frame, "Press 'D' to quit", (int(frame.shape[1])-200, int(frame.shape[0])-20), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0,255,180)) 
    cv.imshow("preview", frame)

    if cv.waitKey(20) & 0xFF==ord('d'): # press 'D' to end
        break

capture.release()
cv.destroyAllWindows()