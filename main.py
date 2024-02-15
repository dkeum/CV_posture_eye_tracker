from utils.text_onScreen import TextonScreen
import threading 
import cv2


class SharedResources():
    def __init__(self):
        # body posture message
        self.message_to_display1 = "Thumbs Up to Start"
        self.message_to_display2 = ""
        self.message_to_display3 = "Blink per min: 0"
        self.lock = threading.Lock()
        self.updated_event = threading.Event()
        self.app_exit = False
        self.has_started = False
        self.start_button =  False

        self.webcam_num = 0

        # number tuning
        self.eye_threshold = 50 # deals with opening/closing eye 
        self.shoulder_threshold = 0 # deals with posture positions
        self.camera_on = False # while detecting if there's 
        self.mood_prediction = False # Paid feature?
        self.timer_interval = 20 
        self.cap = cv2.VideoCapture(self.webcam_num)
    
    def change_cap(self,num):
        self.webcam_num = num
        self.cap = cv2.VideoCapture(num)

    def reset_default_value(self):
        self.message_to_display1 = "Thumbs Up to Start"
        self.message_to_display2 = ""
        self.message_to_display3 = "Blink per min: 0"
        self.start_button =  False

        # self.webcam_num = 0
        self.app_exit = True
        self.has_started = False




    
if __name__ == "__main__":

    sharedResources = SharedResources() # how the modules communicate with each other
    textOnScreen = TextonScreen(sharedResources=sharedResources)
    textOnScreen.main()


