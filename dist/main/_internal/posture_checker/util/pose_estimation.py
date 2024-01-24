import cv2
import mediapipe as mp
import time
import math


class poseDetector():
    def __init__(self, mode=False,model_complexity=1,smooth=True,detectionConf=0.5,trackingConf=0.5):
        self.mode=mode
        self.model_complexity=model_complexity
        self.smooth=smooth
        self.detectionConf=detectionConf
        self.trackingConf=trackingConf

        self.mpDraw= mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(static_image_mode=self.mode,model_complexity=self.model_complexity,smooth_landmarks=self.smooth,min_detection_confidence=self.detectionConf,min_tracking_confidence=self.trackingConf)

    def findPose(self,img,draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img
            
    def findPosition(self, img,draw=True):
        self.lmList=[]
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                self.lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),10,(255,0,255),cv2.FILLED)
        return self.lmList
    
    def findAngle(self, img, p1,p2,p3, draw=True):
        x1,y1 = self.lmList[p1][1:]
        x2,y2 = self.lmList[p2][1:]
        x3,y3 = self.lmList[p3][1:]

        #Calculate angle
        angle = math.degrees(math.atan2(y3-y2,x3-x2)- math.atan2(y1-y2,x1-x2))

        if angle < 0:
            angle+= 360

        # draw
        if draw:
            cv2.line(img, (x1,y1),(x2,y2), (255,255,255), 3)
            cv2.line(img, (x2,y2),(x3,y3), (255,255,255), 3)

            cv2.circle(img, (x1,y1),5,(0,0,255), cv2.FILLED)
            cv2.circle(img, (x2,y2),5,(0,0,255), cv2.FILLED)
            cv2.circle(img, (x3,y3),5,(0,0,255), cv2.FILLED)

            cv2.circle(img, (x1,y1),10,(0,0,255), 2)
            cv2.circle(img, (x2,y2),10,(0,0,255), 2)
            cv2.circle(img, (x3,y3),10,(0,0,255), 2)
            cv2.putText(img, str(int(angle)), (x2-50,y2+50),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)
        return img , angle
    
    def calculateShoulderPosture(self, img):
        # take the landmarks 
        # left shoulder = 12 
        # right shoulder = 11 
        # right ear = 7 , left ear = 8 

        img, angle = self.findAngle(img,7,11,2,draw=False)
        
        x1,y1 =  self.lmList[11][1:] # get the left should point coord
        x2,y2 =  self.lmList[7][1:] # get the left should point coord

        left_distance = self.findDistance(x1,y1,x2,y2)

        x1,y1 =  self.lmList[12][1:] # get the left should point coord
        x2,y2 =  self.lmList[8][1:] # get the left should point coord

        right_distance = self.findDistance(x1,y1,x2,y2)

        return img, angle, left_distance,right_distance

    
    def findDistance(self,x1, y1, x2, y2):
        dist = math.sqrt((x2-x1)**2+(y2-y1)**2)
        return dist
    def sendWarning(x):
        pass
    
    




