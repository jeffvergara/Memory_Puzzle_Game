import RPi.GPIO as GPIO
import array
import time
import subprocess
import pygame
import threading
import os
import memorypuzzle


pygame.init()

global  laser,win_laser,lose_laser


#if your variable is 3
win_laser = [6]
lose_laser = [1,2,3,4,5]

clockCodes = ["9","15"]

#the GPIO must be 3 also
laser = [14,15,18,23,24,25]

def edge(channel):

    for i in range(0,6):
        if laser[i] == channel:
            print("laser " + str(i+1) + " detected")
            for j in range (0,len(win_laser)):
                if win_laser[j] == i+1:
                    print("win")
            for j in range(0,len(lose_laser)):
                if lose_laser[j] == i+1:
                    print("lose")


def disconnected():
    print("disconnected from the server, trying to reconnect")



def hideLCD():
    os.system("sudo pkill -9 LCDtime")
    os.system("opt/vc/bin/tvservice -o")  #deactivating the HDMI

def memorypuzzle(level):

    # you must assign variable
    puzzle = memorypuzzle
    #os.system("python"+"/home/user/PycharmProjects/raspberry_try/memorypuzzle.py")
    subprocess.call(["python3","/home/user/PycharmProjects/raspberry_try/memorypuzzle.py"])   #how to call your python file
                                                                                              #on another python file



#def soundGame():

    #subprocess.call(["aplay", "/home/user/PycharmProjects/raspberry_try/mi3.wav"])


def start_game(level,clock,playercount):


    channel = win_laser
    soundObj = pygame.mixer.Sound("entertainer.wav")



    pygame.mixer.music.load("entertainer.wav")
    pygame.mixer.music.play(-1,0.0)

    soundObj.play()

    pygame.mixer.music.stop()

    print("level is: "+str(level))
    print ("time allowed: "+str(clock))
    print("player count: "+str(playercount))
    print("active threads: " + str (threading.active_count()))





    if not GPIO.input(35):
         print("under voltage")

    for i in range (0,6):

        if not (laser[i]):
            print("laser on")
        else:
            print("laser" + str (i+1)+ " not working")



    threadC = threading.Thread(target=edge, args=(channel)) #the variable must be name
    threadC.start()


def init():
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(35,GPIO.IN)

    for i in range(0,6):
        GPIO.setup(laser[i], GPIO.IN)
        GPIO.add_event_detect(laser[i],GPIO.RISING, callback=edge, bounctime=200)



init()

start_game(1,2,3)
#soundGame()
memorypuzzle(5)