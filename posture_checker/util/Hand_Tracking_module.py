import cv2
import mediapipe as mp
import time
import os 
import sys

bundle_dir = getattr(sys,'_MEIPASS',os.path.abspath(os.path.dirname(__file__)))

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode



class handDetector():
    def __init__(self, mode=False,maxHands=2, model_complexity=1, detectionConf=0.5, trackConf=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.model_complexity=model_complexity
        self.detectionConf = detectionConf
        self.trackConf = trackConf
        self.results = None

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.model_complexity, self.detectionConf,self.trackConf) 
        self.mpDraw = mp.solutions.drawing_utils
        # model_path=r'C:\Users\16047\Desktop\python_project\personal_project\posture_checker\util\gesture_recognizer.task'
        # model_path='./gesture_recognizer.task'
        model_path  = os.path.abspath(os.path.join(bundle_dir,'gesture_recognizer.task'))
        self.options = GestureRecognizerOptions(
        base_options=BaseOptions(model_asset_buffer=open(model_path,'rb').read()),
        running_mode=VisionRunningMode.LIVE_STREAM,
        result_callback=self.print_result)
        
    

        self.fingerTipsId = [4,8,12,16,20]
    
    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # print(results)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img
    
    def findPosition(self,img, handNo=0, draw=True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h,w,c = img.shape
                cx,cy = int(lm.x*w), int(lm.y*h)
                self.lmList.append([id,cx,cy])
                if draw:
                    cv2.circle(img,(cx,cy),5,(255,0,255), cv2.FILLED)
        return self.lmList
    
    def FingersUp(self): 
        fingers=[]
        
        if self.lmList[self.fingerTipsId[0]][1] < self.lmList[self.fingerTipsId[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # fingers     
        for id in range(1,5):
            if self.lmList[self.fingerTipsId[id]][2] < self.lmList[self.fingerTipsId[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        return fingers

    ''' 
     - take in the videoCapture "cap" as input. 
     - Used a thread function
    '''
    def ThumbUp(self ,cap, shared_data=None, textOnScreen= None): 
        timestamp = 0
        isFound = False
        with GestureRecognizer.create_from_options(self.options) as recognizer:
            while not isFound and not textOnScreen.app_exit:
                success, img = cap.read()
                timestamp+=1
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
                recognizer.recognize_async(mp_image, timestamp)
                if self.results is not None and self.results != []: 
                    # print(self.results[0][0].category_name)
                    if self.results[0][0].category_name == 'Thumb_Up':
                        # threading condiiton
                        if shared_data != None: 
                            isFound= True
                            # print("thumb is up in the hand detector")
                            shared_data.value = True
                            shared_data.updated_event.set()
                            time.sleep(1)
                        return True
                cv2.waitKey(100)            
    
    # Create a image segmenter instance with the live stream mode:
    def print_result(self, result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
        # cv2.imshow('Show', output_image.numpy_view())
        # imright = output_image.numpy_view()
        self.results = result.gestures
        # print(result.gestures)
        # cv2.imwrite('somefile.jpg', imright)
         
    def main(self):
        pTime = 0 
        cTime = 0
        timestamp = 0
        cap = cv2.VideoCapture(0)
        self.ThumbUp(cap)
        
        

        # with GestureRecognizer.create_from_options(self.options) as recognizer:
        #     while True:
        #         success, img = cap.read()

        #         if not success:
        #             print("Ignoring empty frame")
        #             break
        #         timestamp+=1
        #         mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
        #         recognizer.recognize_async(mp_image, timestamp)

        #         if self.results is not None and self.results != []: 
        #             print(self.results[0][0].category_name)
                

        #         # img = self.findHands(img)
        #         # myList = self.findPosition(img)
        #         # if len(myList) != 0:
        #             # print(myList[4])
        #             # pass

        #         cTime = time.time()
        #         fps = 1/(cTime-pTime)
        #         pTime=cTime

        #         cv2.putText(img, str(int(fps)), (10,70), cv2.FONT_HERSHEY_COMPLEX,3,(255,0,255),3)
        #         cv2.imshow("image",img)
        #         cv2.waitKey(5)



if __name__ == "__main__":
    body_module = handDetector()
    body_module.main()
