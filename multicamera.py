#Program Name: multicamera.py
#Author: Victoria Koretsky
#Description: Displays three webcam feeds simultaneously
#Saves pictures and videos when corresponding buttons are pressed
#To run "python multicamera.py <-filename->"
#

#IMPORTS
import cv2 as cv
import pygame
import math
import numpy as np
import sys
from pygame import gfxdraw


#Function: circleCheck
#inputs: pose (tuple x,y), center (tuple x,y), radius (int)
#outputs: binary True/False if the x,y pose is contained in the circle of given center and radius
def circleCheck(pose,center,radius):
    
    x = pose[0]
    y = pose[1]
    
    cenx = center[0]
    ceny = center[1]
    
    sqx = (x - cenx)**2
    sqy = (y - ceny)**2
    
    if math.sqrt(sqx+sqy) < radius:
        return True
    else:
        return False

#MAIN FUNCTION
def main(argv):
        
    pygame.init()
    
    #DEFINING VARIABLES

    #setting logo
    logo = pygame.image.load("logo.png")
    pygame.display.set_icon(logo)
    
    #video click (for video file title)
    videoclick1 = 0
    videoclick2 = 0
    videoclick3 = 0
    
    #picture click (for picture file title)
    pictureclick1 = 0
    pictureclick2 = 0
    pictureclick3 = 0
    
    #colors
    red = (255,23,0)
    green = (23,255,0)
    grey = (175,175,220)
    
    #circle colors
    circle1 = green
    circle2 = green
    circle3 = green
    circle4 = green
    
    #creating rectangle button sizes
    rectbutton1 = pygame.Rect(260, 525, 30, 30)
    rectbutton2 = pygame.Rect(900, 525, 30, 30)
    rectbutton3 = pygame.Rect(1540, 525, 30, 30)
    rectbutton4 = pygame.Rect(900, 665, 40, 40)
    
    #video width and height
    vw = 640
    vh = 480
    
    #circle widths and heights
    cw1 = 380
    cw2 = 1020
    cw3 =  1660
    ch = 540
    bigcw = 1020
    bigch = 680
    
    #webcam feeds
    cap1 = cv.VideoCapture(0)
    cap2 = cv.VideoCapture(1)
    cap3 = cv.VideoCapture(2)
    
    #frames per second
    fps = 30.0

    #define fourcc (codec), compresses video
    fourcc = cv.VideoWriter_fourcc('m','p','4','v')
    
    #creating flags for recording
    feed1 = False
    feed2 = False
    feed3 = False
    file1 = cv.VideoWriter('temp1.mp4',fourcc, fps, (vw,vh))
    file2 = cv.VideoWriter('temp2.mp4',fourcc, fps, (vw,vh))
    file3 = cv.VideoWriter('temp3.mp4',fourcc, fps, (vw,vh))

    #creating pygame screen and name
    screen = pygame.display.set_mode((1920, 960))
    pygame.display.set_caption("Camera")
    
    #WHILE LOOP
    while True:
    
        #defining variables from camera read for surface display
        rcor1, frame1 = cap1.read()
        rcor2, frame2 = cap2.read()
        rcor3, frame3 = cap3.read()
        
        #defining pic variable for recordings
        pic1 = frame1
        pic2 = frame2
        pic3 = frame3
        
        #changing frame colors so they are compatible with the code
        frame1 = cv.cvtColor(frame1, cv.COLOR_BGR2RGB)
        frame2 = cv.cvtColor(frame2, cv.COLOR_BGR2RGB)
        frame3 = cv.cvtColor(frame3, cv.COLOR_BGR2RGB)
        
        #rotating the frames 90 degrees
        frame1 = np.rot90(frame1)
        frame2 = np.rot90(frame2)
        frame3 = np.rot90(frame3)
        
        #defining the frames as pygame surfaces
        frame1 = pygame.surfarray.make_surface(frame1)
        frame2 = pygame.surfarray.make_surface(frame2)
        frame3 = pygame.surfarray.make_surface(frame3)        
        
        #displaying the frames on window
        screen.blit(frame1, (0,0))
        screen.blit(frame2, (vw,0))
        screen.blit(frame3, ((vw*2),0))
        pygame.display.update()
        
        #defining feeds if true (saving recordings)
        if feed1 == True:               #webcam 1
            pic1 = cv.flip(pic1,1)
            #write flipped frame
            file1.write(pic1)
            pygame.display.update()
            
        if feed2 == True:               #webcam 2
            pic2 = cv.flip(pic2,1)
            #write flipped frame
            file2.write(pic2)
            pygame.display.update()
            
        if feed3 == True:               #webcam 3
            pic3 = cv.flip(pic3,1)
            #write flipped frame
            file3.write(pic3)
            pygame.display.update()
            
        #drawing and displaying circle buttons
        #draw circle button first with anti-aliased outline using gfxdraw – then fill in circle with gfx draw
        #MUST DO THIS EVERY TIME YOU DRAW A CIRCLE IN THIS ORDER
        pygame.gfxdraw.aacircle(screen, cw1, ch, 20, circle1)           #circle 1
        pygame.gfxdraw.filled_circle(screen, cw1, ch, 20, circle1)      #circle 1
        
        pygame.gfxdraw.aacircle(screen, cw2, ch, 20, circle2)           #circle 2 
        pygame.gfxdraw.filled_circle(screen, cw2, ch, 20, circle2)      #circle 2
        
        pygame.gfxdraw.aacircle(screen, cw3, ch, 20, circle3)           #circle 3
        pygame.gfxdraw.filled_circle(screen, cw3, ch, 20, circle3)      #circle 3
        
        pygame.gfxdraw.aacircle(screen, bigcw, bigch, 30, circle4)      #circle 4
        pygame.gfxdraw.filled_circle(screen, bigcw, bigch, 30, circle4) #circle 4
        
        #drawing and displaying rectangle buttons
        pygame.draw.rect(screen, grey, rectbutton1)     #rectangle 1
        pygame.draw.rect(screen, grey, rectbutton2)     #rectangle 2
        pygame.draw.rect(screen, grey, rectbutton3)     #rectangle 3
        pygame.draw.rect(screen, grey, rectbutton4)     #rectangle 4
        pygame.display.update()
        
        #CHECKING CLICKS
        for event in pygame.event.get():
            #checking coordinates of click and whether it is on the button
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                #FIRST WEBCAM
                #start feed 1 recording after pressing the circle1 button
                if ((circleCheck(mouse_pos, (cw1, ch), 20) == True) and (circle1 == green)):
                    videoclick1 += 1
                    feed1 = True
                    circle1 = red
                    print('started recording [webcam 1]!')
                    #releasing previous file1
                    file1.release()
                    #creating new file name
                    imname1 = sys.argv[1]+'_f1_{}.mp4'.format(videoclick1)
                    #saving video
                    file1 = cv.VideoWriter(imname1,fourcc, fps, (vw,vh))
                
                #stopping feed 1 recording after pressing the circle1 button
                elif ((circleCheck(mouse_pos, (cw1, ch), 20) == True) and (circle1 == red)):
                    feed1 = False
                    circle1 = green
                    circle4 = green
                    print('stopped recording [webcam 1]!')
                    #releasing file
                    file1.release()
                
                #taking a feed 1 picture after pressing the rect1 button
                if rectbutton1.collidepoint(mouse_pos):
                    pictureclick1 += 1
                    #creating file name
                    img1 = sys.argv[1]+'_f1_{}.png'.format(pictureclick1)
                    #saving picture
                    cv.imwrite(img1,pic1)
                    print('picture taken [webcam 1]!')
                    
                #SECOND WEBCAM
                #starting feed 2 recording after pressing the circle2 button
                if ((circleCheck(mouse_pos, (cw2, ch), 20) == True) and (circle2 == green)):
                    videoclick2 += 1
                    feed2 = True
                    circle2 = red
                    print('started recording [webcam 2]!')
                    #releasing previous file2
                    file2.release()
                    #creating new file name
                    imname2 = sys.argv[1]+'_f2_{}.mp4'.format(videoclick2)
                    #saving video
                    file2 = cv.VideoWriter(imname2,fourcc, fps, (vw,vh))
                
                #stopping feed 2 recording after pressing the circle2 button
                elif ((circleCheck(mouse_pos, (cw2, ch), 20) == True) and (circle2 == red)):
                    feed2 = False
                    circle2 = green
                    circle4 = green
                    print('stopped recording [webcam 2]!')
                    #releasing file2
                    file2.release()
                
                #taking a feed 2 picture after pressing the rect2 button
                if rectbutton2.collidepoint(mouse_pos):
                    pictureclick2 += 1
                    #creating file name
                    img2 = sys.argv[1]+'_f2_{}.png'.format(pictureclick2)
                    #saving picture
                    cv.imwrite(img2,pic2)
                    print('picture taken [webcam 2]!')

                #THIRD WEBCAM
                #starting feed 3 recording after pressing the circle3 button
                if ((circleCheck(mouse_pos, (cw3, ch), 20) == True) and (circle3 == green)):
                    videoclick3 += 1
                    feed3 = True
                    circle3 = red
                    print('started recording [webcam 3]!')
                    #releasing previous file3
                    file3.release()
                    #creating new file name
                    imname3 = sys.argv[1]+'_f3_{}.mp4'.format(videoclick3)
                    #saving video
                    file3 = cv.VideoWriter(imname3,fourcc, fps, (vw,vh))
                
                #stopping feed 3 recording after pressing the circle3 button                
                elif ((circleCheck(mouse_pos, (cw3, ch), 20) == True) and (circle3 == red)):
                    feed3 = False
                    circle3 = green
                    circle4 = green
                    print('stopped recording [webcam 3]!')
                    #releasing file3
                    file3.release()
                
                #taking a feed 3 picture after pressing the rect3 button                
                if rectbutton3.collidepoint(mouse_pos):
                    pictureclick3 += 1
                    #creating file name
                    img3 = sys.argv[1]+'_f3_{}.png'.format(pictureclick3)
                    #saving picture
                    cv.imwrite(img3,pic3)
                    print('picture taken [webcam 3]!')
                    
                #ALL WEBCAMS (BIG BUTTONS)
                #starting all three recordings if circle 4 is pressed
                #stopping and starting any cameras that are already recording
                if ((circleCheck(mouse_pos, (bigcw, bigch), 30) == True) and (circle4 == green)):
                    videoclick1 += 1
                    videoclick2 += 1
                    videoclick3 += 1
                    file1.release()
                    file2.release()
                    file3.release()
                    #creating all file names
                    imname1 = sys.argv[1]+'_f1_{}.mp4'.format(videoclick1)
                    imname2 = sys.argv[1]+'_f2_{}.mp4'.format(videoclick2)
                    imname3 = sys.argv[1]+'_f3_{}.mp4'.format(videoclick3)
                    #saving all videos
                    file1 = cv.VideoWriter(imname1,fourcc, fps, (vw,vh))
                    file2 = cv.VideoWriter(imname2,fourcc, fps, (vw,vh))
                    file3 = cv.VideoWriter(imname3,fourcc, fps, (vw,vh))
                    feed1 = True
                    feed2 = True
                    feed3 = True
                    circle1 = red
                    circle2 = red
                    circle3 = red
                    circle4 = red
                    print('all videos recording!')
                
                #stopping all three webcam recordings
                elif ((circleCheck(mouse_pos, (bigcw, bigch), 30) == True) and (circle4 == red)):
                    feed1 = False
                    feed2 = False
                    feed3 = False
                    circle1 = green
                    circle2 = green
                    circle3 = green
                    circle4 = green
                    #releasing all files
                    file1.release()
                    file2.release()
                    file3.release()
                    print('all videos stopped!')
                
                #taking a picture with all webcams
                if rectbutton4.collidepoint(mouse_pos):
                    pictureclick1 += 1
                    pictureclick2 += 1
                    pictureclick3 += 1
                    #creating all file names
                    img1 = sys.argv[1]+'_f1_{}.png'.format(pictureclick1)
                    img2 = sys.argv[1]+'_f2_{}.png'.format(pictureclick2)
                    img3 = sys.argv[1]+'_f3_{}.png'.format(pictureclick3)
                    #saving all images
                    cv.imwrite(img1,pic1)
                    cv.imwrite(img2,pic2)
                    cv.imwrite(img3,pic3)
                    print('all pictures taken!')
                    
            #QUITTING
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    pygame.quit()
    sys.exit()


main(sys.argv)    