import pygame 
from .buttons import button
from .slider import Slider
from .dropDownMenu import DropDown
from .checkbox import Checkbox
import cv2
import numpy as np




class Menu:
    def __init__(self, app, bg="gray") -> None:
        self.app = app
        self.bg = bg

        button1 = button(position=(600, 400), size=(100, 50), clr=(220, 220, 220), cngclr=(255, 0, 0), func=self.fn1, text='Start')
        button2 = button((750, 400), (100, 50), (220, 220, 220), (255, 0, 0), self.fn2, 'Settings')

        self.buttons = [button1, button2]

        self.button2 = button((1100, 640), (150, 60), (220, 220, 220), (255, 0, 0), self.fn3, 'Back to Menu')

        # Mood 
        self.mood_button_x = 1000
        self.mood_button_y = 130
        self.button3 = button((self.mood_button_x, self.mood_button_y), (150, 60), (220, 220, 220), (255, 0, 0), self.fn3, 'On')
        self.button4 = button((self.mood_button_x+180, self.mood_button_y), (150, 60), (220, 220, 220), (255, 0, 0), self.fn3, 'Off')

        # Camera 
        self.camera_button_x = 1000
        self.camera_button_y = 250
        self.button5 = button((self.camera_button_x, self.camera_button_y), (150, 60), (220, 220, 220), (255, 0, 0), self.fn3, 'On')
        self.button6 = button((self.camera_button_x+180, self.camera_button_y), (150, 60), (220, 220, 220), (255, 0, 0), self.fn3, 'Off')
    
        self.slider_x = 1100
        self.slider_y = 450
        self.sliders = [
            Slider((self.slider_x,self.slider_y), (300,40), 0.5, 0, 100),
            Slider((self.slider_x,self.slider_y+100), (300,40), 0.5, 0, 100),
        ]

        COLOR_INACTIVE = (100, 80, 255)
        COLOR_ACTIVE = (100, 200, 255)
        COLOR_LIST_INACTIVE = (255, 100, 100)
        COLOR_LIST_ACTIVE = (255, 150, 150)

        self.dropDown = DropDown(
            [COLOR_INACTIVE, COLOR_ACTIVE],
            [COLOR_LIST_INACTIVE, COLOR_LIST_ACTIVE],
            600, 200, 200, 50, 
            pygame.font.SysFont(None, 30), 
            "Select Webcam", [])

        self.check_button_x = 550
        self.check_button_y = 500
        self.boxes = []
        checkbox_button1 = Checkbox(self.app.screen, self.check_button_x, self.check_button_y, 0, caption='10 mins')
        checkbox_button2 = Checkbox(self.app.screen, self.check_button_x, self.check_button_y+50, 0, caption='20 mins (Default)')
        checkbox_button3 = Checkbox(self.app.screen, self.check_button_x, self.check_button_y+100, 0, caption='30 mins')
        self.boxes.append(checkbox_button1)
        self.boxes.append(checkbox_button2)
        self.boxes.append(checkbox_button3)


    def start_screen(self):
        self.app.screen.fill("black")

        top_text_width = 500
        top_text_height = 200

        title_color = (255,0,0)
        font = pygame.font.SysFont("Segoe Print", 50)
        txt_surf = font.render("Posture Plus", True, title_color)
        self.app.screen.blit(txt_surf, (top_text_width,top_text_height)) 


        for button in self.buttons:
            button.draw(self.app.screen)


    def setting_page(self, cap):

        webcam_ischecked = False
        mouse_pos = pygame.mouse.get_pos()
        mouse = pygame.mouse.get_pressed()

        self.app.screen.fill("black")

        # Video Capture

        if cap != None:
            if not webcam_ischecked:
                video_list = self.check_camera_options(cap)
                self.dropDown.options = video_list
                webcam_ischecked = True

            _ , frame = cap.read()
            frame = cv2.resize(frame, (500, 500))
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB format
            frame = np.rot90(frame)  # Rotate the frame if needed
            frame = pygame.surfarray.make_surface(frame)
            self.app.screen.blit(frame, (20, 150))

        # sliders to adjust sensitiivty 

        title_color = (255,255,255)
        font = pygame.font.SysFont("Segoe Print", 50)
        txt_surf = font.render("Settings Page", True, title_color)
        self.app.screen.blit(txt_surf, (20,20)) 


        font = pygame.font.SysFont("Segoe Print", 30)
        txt_surf = font.render("Detection Thresholds", True, title_color)
        self.app.screen.blit(txt_surf, (940,320)) 

        txt_surf = font.render("Eye", True, title_color)
        self.app.screen.blit(txt_surf, (self.slider_x-150,self.slider_y-70)) 

        txt_surf = font.render("Shoulder", True, title_color)
        self.app.screen.blit(txt_surf, (self.slider_x-150,self.slider_y+30)) 

        for slider in self.sliders:
            if slider.container_rect.collidepoint(mouse_pos):
                if mouse[0]:
                    slider.grabbed = True
            if not mouse[0]:
                slider.grabbed = False
            if slider.button_rect.collidepoint(mouse_pos):  
                slider.hover()
            if slider.grabbed:
                slider.move_slider(mouse_pos)
                slider.hover()
            else:
                slider.hovered = False
            slider.render(self.app)
            slider.display_value(self.app)

        ################### buttons #####################################

        # back to menu
        self.button2.draw(self.app.screen)

        # Mood prediction
  
        txt_surf = font.render("Mood Prediction", True, title_color)
        self.app.screen.blit(txt_surf, (self.mood_button_x-50, self.mood_button_y-100)) 

        
        self.button3.draw(self.app.screen)
        self.button4.draw(self.app.screen)


        # Camera on/off    

        txt_surf = font.render("Camera", True, title_color)
        self.app.screen.blit(txt_surf, (self.camera_button_x, self.camera_button_y-80)) 
        self.button5.draw(self.app.screen)
        self.button6.draw(self.app.screen)

        txt_surf = font.render("Timer Interval", True, title_color)
        self.app.screen.blit(txt_surf, (self.check_button_x, self.check_button_y-70)) 
        for checkbox in self.boxes:
            checkbox.render_checkbox() 

        ################### buttons #####################################



        ################### drop down Menu ###########################
        # controls the video capture desired 
        self.dropDown.draw(self.app.screen)

        ################### drop down Menu ###########################

    # callback functions 
    def fn1(self):
        self.app.sharedResources.app_exit = False
        self.app.sharedResources.start_button = True
        return "main_page"
    def fn2(self):
        self.app.sharedResources.start_button = False
        return "setting_page"
    def fn3(self):
        self.app.sharedResources.start_button = False
        return "start_page"
    
    # check camera options 

    def check_camera_options(self,cap):
        index = 1
        arr = ["webcam 1"]
        while True:
            cap = cv2.VideoCapture(index)
            if not cap.read()[0]:
                break
            else:
                arr.append( "webcam " + str(index+1))
            cap.release()
            index += 1
        return arr

