# # Goal: check the posture in regular intervals and notify the user when the posture is bad
# # sound / visual
# # stick visual for now. on the top left corner a rectangle with text "bad posture"

# # primarily the camera should be in front of the person ie (facing the laptop in front of you)

# # problems
# # (1) different camera angles there are different values of angles and distances between ear to shoulder ratio to calculate
# # (2)





import cv2
from .util import pose_estimation
from .util import Hand_Tracking_module
import threading
import time
import numpy as np 



class SharedData:
    def __init__(self):
        self.value = True
        self.lock = threading.Lock()
        self.updated_event = threading.Event()


class PostureChecker(): 
     def __init__(self): 
          self.detector = pose_estimation.poseDetector()
          self.hand_detector = Hand_Tracking_module.handDetector()
          # self.bad_posture_counter = 0

     def posture_checker(self, cap, shared_data=None, TextOnScreen=None):
          found_optimal_value = False

         
          while not TextOnScreen.app_exit:
               _ , img = cap.read()
               img = self.detector.findPose(img,draw=False)
               lmList = self.detector.findPosition(img,draw=False)
               
               if len(lmList) != 0:
                    img, angle, left_distance, right_distance = self.detector.calculateShoulderPosture(img)
                    # case when a object is not passed in
                    if shared_data == None: 
                         if not found_optimal_value:
                              self.hand_detector.ThumbUp(cap)
                              print("Thumb's up confirmed")
                              img, angle, left_distance, right_distance = self.detector.calculateShoulderPosture(img)
                              good_angle, good_LD, good_RD = angle, left_distance, right_distance
                              print(good_angle, good_LD, good_RD)
                              found_optimal_value = True

                    else: 
                         if not shared_data.value or shared_data.updated_event.is_set():
                              if not found_optimal_value:
                                   good_angle, good_LD, good_RD = angle, left_distance, right_distance
                                   print("Thumb's up confirmed")
                                   if TextOnScreen != None:
                                        TextOnScreen.message_to_display1 = "Thumb's up confirmed"
                                        TextOnScreen.has_started = True
                                   print(good_angle, good_LD, good_RD)
                                   found_optimal_value = True
                    
               if found_optimal_value:
                    shoulder_threshold = 0
                    shoulder_angle_threshold = 0
                    

                    if TextOnScreen.shoulder_threshold != 0:
                         shoulder_threshold = np.interp( TextOnScreen.shoulder_threshold , [0,100], [0,35]) 
                         shoulder_angle_threshold = np.interp( TextOnScreen.shoulder_threshold , [0,100], [0,5]) 

                    if abs(good_angle - angle) > 5+shoulder_angle_threshold or abs(good_LD - left_distance) > 15+shoulder_threshold or abs(good_RD - right_distance) > 15+shoulder_threshold:
                         if TextOnScreen is not None:
                              # print("bad posture detected")
                              # TextOnScreen.update_msg1("bad posture detected")
                              TextOnScreen.message_to_display1 = "bad posture detected"
                    else:
                         if TextOnScreen is not None:
                              # print("good posture detected")
                              # TextOnScreen.update_msg1("good posture detected")
                              TextOnScreen.message_to_display1 = "good posture detected"
                         #  cv2.putText(img,"Stand up with Good Posture",(70,50),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),3)
                         #  cv2.putText(img,"If done, Put up a thumb",(70,200),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),3)

               # cv2.putText(img,str(int(fps)),(70,50),cv2.FONT_HERSHEY_COMPLEX,3,(255,0,0),3)
               # cv2.imshow("image", img)
               time.sleep(0.5)
               
        
     def main(self,cap, TextOnScreen=None):
      
          shared_data = SharedData()
          thread1= threading.Thread(target=self.posture_checker, args=(cap, shared_data,TextOnScreen ))
          thread2= threading.Thread(target=self.hand_detector.ThumbUp, args=(cap, shared_data, TextOnScreen ))

          thread1.start()
          thread2.start()
          # Wait for both threads to finish
          thread1.join()
          shared_data.updated_event.set()
          thread2.join()



if __name__ == "__main__":
    posture_checker = PostureChecker()
    cap = cv2.VideoCapture(0)
    posture_checker.main(cap)










