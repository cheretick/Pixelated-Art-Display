import cv2 as cv
import numpy as np

PIXEL_SIZE = 15
APPLY_PIXELATE = True
APPLY_DIFFERENCE = True

capture = cv.VideoCapture(1) # try cv.VideoCapture(0) if you aren't getting input
print("Capture Input--\theight: " + str(capture.get(4)) + "\twidth: " 
    + str(capture.get(3)) + "\tframerate: " + str(capture.get(5)))

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
    prompt = np.zeros(shape=[int(capture.get(4)), int(capture.get(3)), 3], dtype=np.uint8)
    cv.putText(prompt, "Welcome!", (60, 60), cv.FONT_HERSHEY_TRIPLEX, 1, (0,255,180))
    cv.putText(prompt, "Would you like to take a new background image?", (20, 90), cv.FONT_HERSHEY_TRIPLEX, 0.6, (0,255,180))
    cv.putText(prompt, "Press 'Y' for \"Yes\" or 'N' for \"No\"", (40, 115), cv.FONT_HERSHEY_TRIPLEX, 0.6, (0,255,180))
    cv.putText(prompt, "Instructions:", (20, 250), cv.FONT_HERSHEY_TRIPLEX, 0.6, (0,255,180))
    cv.putText(prompt, "When ready, press 'K' to to take background reference image", (30, 270), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0,255,180))
    cv.putText(prompt, "Make sure nobody is in the frame", (30, 290), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0,0,255))
    cv.putText(prompt, "Camera must be still after image is taken", (30, 310), cv.FONT_HERSHEY_TRIPLEX, 0.5, (0,0,255))
    cv.imshow("preview", prompt)
    if cv.waitKey(20) & 0xFF==ord('y'):
        while True:
            isTrue, image = capture.read()    
            cv.imshow("preview", image)
            # press 'K' to take a new background image or press 'Q' to skip
            if cv.waitKey(20) & 0xFF==ord('k'):
                cv.imwrite('./background.jpg', image)
                break
            if cv.waitKey(20) & 0xFF==ord('q'):
                break
    if cv.waitKey(20) & 0xFF==ord('n'):
        break           

while True:
    # captures a frame
    isTrue, frame = capture.read()
    if APPLY_DIFFERENCE:
        # grabs background image
        background = cv.imread('./background.jpg')
        
        # applies the difference between the image and the video feed
        frame = cv.absdiff(background, frame)
    
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