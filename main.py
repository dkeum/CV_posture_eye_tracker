import threading 
import os 
from utils.text_onScreen import TextonScreen
from posture_checker.posture_checker import PostureChecker
from time_on_computer.time_on_computer import TimeTrack
import cv2
from eye_tracker.tiredness_checker import FaceMesh

class SharedResources():
    def __init__(self):
        # body posture message
        self.message_to_display1 = "Thumbs Up to Start"
        self.message_to_display2 = ""
        self.message_to_display3 = "Blink per min: 0"
        self.lock = threading.Lock()
        self.updated_event = threading.Event()
    



if __name__ == "__main__":

    textOnScreen = TextonScreen()
    posture_checker = PostureChecker()
    sharedResources = SharedResources() # how the modules communicate with each other
    TimeonComputer = TimeTrack()
    eye_track = FaceMesh()

    cap = cv2.VideoCapture(0)
    
    thread1 = threading.Thread(target=posture_checker.main, args=(cap, sharedResources))
    thread3 = threading.Thread(target=TimeonComputer.main, args=(sharedResources,))  
    thread4 = threading.Thread(target=eye_track.main, args=(cap, sharedResources,))  
 

    thread1.start()
    thread3.start()
    thread4.start()

    TextonScreen().main(sharedResources)

    thread1.join()
    thread3.join()
    thread4.join()

