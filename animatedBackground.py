from turtle import width
import cv2 as cv
import numpy as np
import random as rand
import time

# use a common factor of height and width for pixel size to fit evenly
# https://www.calculatorsoup.com/calculators/math/commonfactors.php
PIXEL_SIZE = 15
HEIGHT = 1080
WIDTH = 1920

PIXEL_HEIGHT = HEIGHT//PIXEL_SIZE
PIXEL_WIDTH = WIDTH//PIXEL_SIZE

rand.seed(0)

pixelArray = [[[0 for k in range(3)] for j in range(PIXEL_WIDTH)] for i in range(PIXEL_HEIGHT)]

def Rainbow():
    for i in range(PIXEL_HEIGHT):
        for j in range(PIXEL_WIDTH):
            for k in range(3):
                pixelArray[i][j] = (int(rand.random()*255), int(rand.random()*255), int(rand.random()*255))

def UTColors():
    # OpenCV uses (blue, green, red)
    colors = [
        (74,36,0),      # Oxford Blue
        (101,50,0),     # Dark Midnight Blue
        (137,68,0),     # Midnight Blue
        (57,177,212),   # American Gold
        (12,135,185),   # Dark Goldenrod
        (22,103,154),   # Golden Brown
        (79,79,79),     # DarkGrey
        (105,105,105),  # DimGrey
        (128,128,128)   # Grey
        ]

    for i in range(PIXEL_HEIGHT):
        for j in range(PIXEL_WIDTH):
                pixelArray[i][j] = (colors[rand.randint(0,len(colors)-1)])

def UTGradient():
    # OpenCV uses (blue, green, red)
    gradientWeight = 0.7
    colors = [
        (74,36,0),      # Oxford Blue           
        (101,50,0),     # Dark Midnight Blue    
        (137,68,0),     # Midnight Blue     

        #(79,79,79),     # DarkGrey              
        #(105,105,105),  # DimGrey               
        #(128,128,128),  # Grey

        (57,177,212),   # American Gold         
        (12,135,185),   # Dark Goldenrod        
        (22,103,154),   # Golden Brown          
        ]

    # sorts colors by brightness
    colors = sorted(colors, key=sum, reverse=True)

    for i in range(PIXEL_HEIGHT):
        for j in range(PIXEL_WIDTH):
            iGradientOffset = i / PIXEL_HEIGHT * gradientWeight
            jGradientOffset = j / PIXEL_WIDTH * gradientWeight
            randomNumber = rand.random()
            randomSelection = int((randomNumber + iGradientOffset + jGradientOffset)/(1 + gradientWeight*2) * (len(colors)))
            #print(str(i) + " " + str(j) + ":\t" + str(randomNumber) + " " + str(iGradientOffset) + " " + str(jGradientOffset) 
            #    + " = " + str((randomNumber + iGradientOffset + jGradientOffset)/(1 + gradientWeight*2)) + "\t\t\t==== " + str(randomSelection))
            pixelArray[i][j] = (colors[randomSelection])

print("Pixel dimensions: " + str(PIXEL_WIDTH) + ", " + str(PIXEL_HEIGHT))
image = np.zeros((HEIGHT, WIDTH, 3), dtype='uint8')


while True:
    UTGradient()

    # apply pixel array to image
    for i in range(PIXEL_HEIGHT):
        for j in range(PIXEL_WIDTH):
            #print(pixelArray[i][j])
            image[i*PIXEL_SIZE:(i*PIXEL_SIZE)+PIXEL_SIZE, j*PIXEL_SIZE:(j*PIXEL_SIZE)+PIXEL_SIZE] = pixelArray[i][j]
    
    cv.putText(image, "Press 'D' to quit", (int(0.01*WIDTH), int(0.04*HEIGHT)), cv.FONT_HERSHEY_TRIPLEX, 1, (255,255,255), thickness=2)
    cv.imshow("Animated Background", image)

    time.sleep(0.05) # slows down the animation by adding 50ms second delay between frame generation

    if cv.waitKey(20) & 0xFF==ord('d'): # press 'D' to end
        break

cv.destroyAllWindows()