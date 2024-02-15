import cv2
import mediapipe as mp
import time
import numpy as np

class FaceMesh():
    def __init__(self, staticMode=False, maxFaces=2, minDectConf=0.5, minTrackConf=0.5):
        self.staticMode = staticMode
        self.maxFaces = maxFaces
        self.minDectConf = minDectConf
        self.minTrackConf = minTrackConf
        self.mpDraw = mp.solutions.drawing_utils
        self.mpFaceMesh = mp.solutions.face_mesh
        self.faceMesh = self.mpFaceMesh.FaceMesh(max_num_faces=self.maxFaces)
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)

        self.faces = []
        self.eye_closed_count_val = 0  # Rename to avoid conflict with the method name

        self.blink_per_min = 60 # controls the rate of detection

        self.is_eyeClosed= False

        self.eye_threshold = 0
    
    def findFaceMesh(self, img, draw=True):
        self.imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceMesh.process(self.imgRGB)
        self.faces = []

        temp = [386, 374, 159, 145]
        if self.results.multi_face_landmarks:
            for faceLms in self.results.multi_face_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        img, faceLms, self.mpFaceMesh.FACEMESH_TESSELATION, landmark_drawing_spec=self.drawSpec
                    )
                face = []
                for id, lm in enumerate(faceLms.landmark):
                    ih, iw, ic = img.shape
                    x, y = int(lm.x * iw), int(lm.y * ih)

                    if id in temp and draw==True:
                        cv2.circle(img, (x, y), 3, (0, 255, 0), -1)  # Draw a filled green circle
                        # cv2.putText(img, str(id), (x,y), cv2.FONT_HERSHEY_COMPLEX,0.3,(0,255,0),3)
                    face.append([x, y])
                self.faces.append(face)
        return img, self.faces

    def count_eye_closed(self):  # Rename the method to avoid conflict
        
        if len(self.faces) != 0:
        
            # good ref: https://github.com/google/mediapipe/issues/1909
            # vertical distance
            x1, y1 = self.faces[0][386]  # topRight_peak_eye
            x2, y2 = self.faces[0][374]  # botVertexRight_peak_eye
            x3, y3 = self.faces[0][159]  # topLeft_peak_eye
            x4, y4 = self.faces[0][145]  # botVertexLeft_peak_eye

            # horizontal distance
            x5, y5 = self.faces[0][263]  # LeftL_x,y 
            x6, y6 = self.faces[0][362]  # LeftR_x,y
            x7, y7 = self.faces[0][133]  # RightL_x,y
            x8, y8 = self.faces[0][33]  # RightR_x,y



            distance_right_eye_V = self.euclidean_distance(x1, y1, x2, y2)
            distance_left_eye_V = self.euclidean_distance(x3, y3, x4, y4)

            distance_right_eye_H = self.euclidean_distance(x5, y5, x6, y6)
            distance_left_eye_H = self.euclidean_distance(x7, y7, x8, y8)

            if distance_right_eye_V != 0 and distance_left_eye_V !=0:
                reRatio = distance_right_eye_H/distance_right_eye_V
                leRatio = distance_left_eye_H/distance_left_eye_V
                ratio = (reRatio+leRatio)/2
            
                eye_threshold = np.interp(self.eye_threshold, [0,100], [-2,2])
                if ratio > 4.4+eye_threshold: 
                    self.is_eyeClosed = True
                    # print("eye is down")
                else:
                    if ratio < 3.5+eye_threshold and self.is_eyeClosed:
                        self.eye_closed_count_val += 1
                        # print("total blinks: " + str(self.eye_closed_count_val))
                        self.is_eyeClosed = False

    def mouth_closed(self):
         if len(self.faces) != 0:
        
            # good ref: https://github.com/google/mediapipe/issues/1909
            # vertical distance
            x1, y1 = self.faces[0][61]  # RightSide End
            x2, y2 = self.faces[0][91]  # LeftSide End
            
            x3, y3 = self.faces[0][37]  # right of middle top
            x4, y4 = self.faces[0][84]  # right of middle bot

        
            x5, y5 = self.faces[0][0]  # middle top 
            x6, y6 = self.faces[0][17 ]  # middle bot

            x7, y7 = self.faces[0][267]  # left of middle top
            x8, y8 = self.faces[0][314]  # left of middle bot


            # mouth open ratio
            horizontal_distance= self.euclidean_distance(x1, y1, x2, y2)
            right_of_middle = self.euclidean_distance(x3, y3, x4, y4)

            middle = self.euclidean_distance(x5, y5, x6, y6)
            left_of_middle = self.euclidean_distance(x7, y7, x8, y8)

            return (right_of_middle+middle+left_of_middle)/(3*horizontal_distance)

    def neck_leaning_forward(self):
        # here we use the NLR Ratio
        # https://iopscience.iop.org/article/10.1088/1742-6596/2325/1/012057/pdf
        if len(self.faces) != 0:
        
            x1, y1 = self.faces[0][8]  # top of nose
            x2, y2 = self.faces[0][4]  # bottome of nose

            vertical_distance= self.euclidean_distance(x1, y1, x2, y2)

            return vertical_distance

    def euclidean_distance(self, x1, y1, x2, y2):
        return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    def main(self, cap, shared_resource=None):
        next_check_time = time.time() + self.blink_per_min # 10 seconds
        
        while not shared_resource.app_exit:
            self.eye_threshold = shared_resource.eye_threshold
            success, img = cap.read()
            img, faces = self.findFaceMesh(img, draw=False)
            if len(faces) != 0:
                self.count_eye_closed()  # Adjusted method name
                
                current_time = time.time()
                if current_time > next_check_time:
                    next_check_time = current_time + self.blink_per_min # check again in another 10 seconds
                    
                    # put a message
                    if shared_resource is not None:
                        print("Blink per min: " + str(self.eye_closed_count_val))
                        shared_resource.message_to_display3 = "Blink per min: " + str(self.eye_closed_count_val)
                    
                    self.eye_closed_count_val = 0

            cv2.waitKey(5)

        

if __name__ == "__main__":
    detector = FaceMesh()
    cap = cv2.VideoCapture(0)
    detector.main(cap)
