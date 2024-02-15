import pygame
import sys
import os
import win32gui
import win32con
import cv2
import numpy as np
from .UI import UI
from .buttons import button


from .EventHandler import EventHandler

from .menu import Menu

import threading 
from posture_checker.posture_checker import PostureChecker
from time_on_computer.time_on_computer import TimeTrack
from eye_tracker.eye_tracker import FaceMesh


class TextonScreen():
    def __init__(self, sharedResources, x=0, y=0):
        
        self.sharedResources = sharedResources
        
        # Initialize Pygame
        pygame.init()

        self.screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
        UI.init(self)
        
        # screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        # os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

        # Set up the display
        self.width, self.height = 1280, 720
        self.main_width, self.main_height = 350, 450
        # self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)  # Hide window frame ,pygame.NOFRAME
       
        self.hwnd = pygame.display.get_wm_info()["window"]

        pygame.display.set_caption("Text Display")
        self.set_always_on_top()

        # Create a font object
        self.font = pygame.font.Font(None, 36)

        self.text_position = (10, 10)  # top left


        self.clock = pygame.time.Clock()
        self.frame_rate = 10  # Set your desired frame rate here
        self.is_initialized = False
        EventHandler()
        self.menu = Menu(self)
        self.background_thread = False
        self.posture_checker = PostureChecker()
        self.TimeonComputer = TimeTrack()
        self.eye_track = FaceMesh()

        self.thread1 = threading.Thread(target=self.posture_checker.main, args=(self.sharedResources.cap, self.sharedResources))
        self.thread3 = threading.Thread(target=self.TimeonComputer.main, args=(self.sharedResources ,))  
        self.thread4 = threading.Thread(target=self.eye_track.main, args=(self.sharedResources.cap, self.sharedResources,))  

        self.main_page_UI()

    def set_always_on_top(self):
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 300, 150, 0x0001)

    def update_display(self, text, position, color=(255, 255, 255)):
        pygame.draw.rect(self.screen, (0, 0, 0), (0, position[1], 300, 50))
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def display_settings(self):
        self.screen.fill((60,25,60))
        color_light = (250,0,0)
        pygame.draw.rect(self.screen,color_light,[10,10,140,40]) 
        
        title = "Setting Page"
        self.screen.blit(title , (50,20))

    def reinitialize_posture(self):
        print("hi")
        return "main_page"
    
    def main_button_back(self):
        self.sharedResources.reset_default_value()
        self.is_initialized = False
        self.screen = pygame.display.set_mode((self.width, self.height))
        return "start_page"
    
    def main_page_UI(self):

        button_pos_x, button_pos_y = 100,300

        main_button1 = button((button_pos_x, button_pos_y), (150, 60), (220, 220, 220), (255, 0, 0), self.reinitialize_posture, 'reinitialize posture')
        main_button2 = button((button_pos_x, button_pos_y+70), (150, 60), (220, 220, 220), (255, 0, 0), self.main_button_back, 'back to menu')

        self.main_buttons = []
        self.main_buttons.append(main_button1)
        self.main_buttons.append(main_button2)

    def start_main(self): 
        
        self.screen.fill("black")
        sharedData = self.sharedResources
        cap = sharedData.cap

        if sharedData.has_started == False:        
            _ , frame = cap.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB format
            frame = np.rot90(frame)  # Rotate the frame isf needed
            frame = pygame.surfarray.make_surface(frame)
            self.screen.blit(frame, (300, 0))
        else: 
            if self.is_initialized == False:
                self.screen = pygame.display.set_mode((self.main_width, self.main_height))
                self.hwnd = pygame.display.get_wm_info()["window"]
                self.set_always_on_top()
                self.is_initialized = True

        # Check for new messages and update independently
        text1 = sharedData.message_to_display1
        if text1 != "":
            if text1 == "good posture detected":
                font_color = (0, 255, 0)
            elif text1 == "bad posture detected":
                font_color = (255, 0, 0)
            else:
                font_color = (255, 255, 255)
            self.update_display(text1, self.text_position, font_color)


        text2 = sharedData.message_to_display2
        if text2 != "":
            if text2 == "5 min break":
                font_color = (255, 0, 0)
            else:
                font_color = (255, 255, 255)
            text2_position = (self.text_position[0], self.text_position[1] + 50)
            self.update_display(text2, text2_position, font_color)

        text3 = sharedData.message_to_display3
        if text3 != "" :
            if int(text3[14:]) <= 8 and int(text3[14:]) != 0:
                font_color = (255, 0, 0)
            else:
                font_color = (0, 255, 0)
            text3_position = (self.text_position[0], self.text_position[1] + 100)
            self.update_display(text3, text3_position, font_color)
        
        for b in self.main_buttons:
            b.draw(self.screen)

    def start_background_thread(self):

        self.thread1 = threading.Thread(target=self.posture_checker.main, args=(self.sharedResources.cap, self.sharedResources))
        self.thread3 = threading.Thread(target=self.TimeonComputer.main, args=(self.sharedResources ,))  
        self.thread4 = threading.Thread(target=self.eye_track.main, args=(self.sharedResources.cap, self.sharedResources,)) 

        self.thread1.start()
        self.thread3.start()
        self.thread4.start()
 
    def end_background_thread(self):
        self.thread1.join()
        self.thread3.join()
        self.thread4.join()
       
    def main(self):
        # Main game loop
        APPMOUSEFOCUS = 1
        APPINPUTFOCUS = 2
        APPACTIVE     = 4

        current_page = "start_page"
        sharedData = self.sharedResources
        cap = sharedData.cap

        while True:

            EventHandler.run()
            for e in EventHandler.events:
                if e.type == pygame.QUIT:
                    if sharedData != None:
                        sharedData.app_exit = True
                    pygame.quit()
                    sys.exit()
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    if e.button == 1:
                        pos = pygame.mouse.get_pos()
                        for b in self.menu.buttons:
                            if b.rect.collidepoint(pos):
                                current_page = b.call_back()
                        for b in self.main_buttons:
                            if b.rect.collidepoint(pos):
                                current_page = b.call_back()

                        selected_option = self.menu.dropDown.update(event=e, pos=pos)
                        if selected_option >= 0:
                            self.menu.dropDown.main = self.menu.dropDown.options[selected_option]
                        if self.menu.button2.rect.collidepoint(pos):
                            current_page = "start_page"
                        if self.menu.button3.rect.collidepoint(pos):
                            sharedData.mood_prediction = True
                        if self.menu.button4.rect.collidepoint(pos):
                            sharedData.mood_prediction = False
                        if self.menu.button5.rect.collidepoint(pos):
                            sharedData.camera_on  = True
                        if self.menu.button6.rect.collidepoint(pos):
                            sharedData.camera_on  = False
                        if self.menu.sliders[0].button_rect.collidepoint(pos):
                            sharedData.eye_threshold= self.menu.sliders[0].get_value()
                        if self.menu.sliders[1].button_rect.collidepoint(pos):
                            sharedData.shoulder_threshold= self.menu.sliders[1].get_value()
                        for box in self.menu.boxes:
                            box.update_checkbox(e)
                            if box.checked is True:
                                if box.caption == "10 mins":
                                    sharedData.timer_interval = 10
                                elif box.caption == "20 mins (Default)":
                                    sharedData.timer_interval = 20
                                else:
                                    sharedData.timer_interval = 30
                                for b in self.menu.boxes:
                                    if b != box:
                                        b.checked = False

                        
                
                # if e.type == pygame.ACTIVEEVENT:
                #     print("ACTIVEEVENT:", e.state, e.gain)
                #     if e.state & APPMOUSEFOCUS == APPMOUSEFOCUS:
                #         print ('mouse focus ' + ('gained' if e.gain else 'lost'))
                #     if e.state & APPINPUTFOCUS == APPINPUTFOCUS:
                #         print ('input focus ' + ('gained' if e.gain else 'lost'))
                #     if e.state & APPACTIVE == APPACTIVE:
                #         print('app is ' + ('visibile' if e.gain else 'iconified'))

            if current_page == "start_page":
                if self.background_thread == True:
                    self.end_background_thread()
                    self.background_thread = False
                self.menu.start_screen()

            elif current_page == "main_page":
                if self.background_thread == False:
                    self.background_thread = True
                    self.start_background_thread()
                self.start_main()

            elif current_page =="setting_page":
                sharedData.start_button = False
                self.menu.setting_page(cap=cap)
                
            pygame.display.flip()
            self.clock.tick(self.frame_rate)





if __name__ == "__main__":
    text = TextonScreen()
    cap = cv2.VideoCapture(0)
    text.main(cap=cap)



