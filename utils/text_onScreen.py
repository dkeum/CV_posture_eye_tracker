import pygame
import sys
import os
import win32gui
import win32con
import cv2
import numpy as np

class TextonScreen():
    def __init__(self, x=0, y=0):
        # Initialize Pygame
        pygame.init()

        # screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        # os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

        # Set up the display
        self.width, self.height = 300, 150
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)  # Hide window frame ,pygame.NOFRAME
        self.hwnd = pygame.display.get_wm_info()["window"]

        pygame.display.set_caption("Text Display")
        self.set_always_on_top()

        # Create a font object
        self.font = pygame.font.Font(None, 36)

        self.text_position = (10, 10)  # top left

        self.clock = pygame.time.Clock()
        self.frame_rate = 10  # Set your desired frame rate here
        self.is_initialized = False

    def set_always_on_top(self):
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 300, 150, 0x0001)

    def update_display(self, text, position, color=(255, 255, 255)):
        pygame.draw.rect(self.screen, (0, 0, 0), (0, position[1], 300, 50))
        text_surface = self.font.render(text, True, color)
        self.screen.blit(text_surface, position)

    def main(self, sharedData=None, cap =None):
        # Main game loop
        APPMOUSEFOCUS = 1
        APPINPUTFOCUS = 2
        APPACTIVE     = 4
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    if sharedData != None:
                        sharedData.app_exit = True
                    pygame.quit()
                    sys.exit()
                # if e.type == pygame.ACTIVEEVENT:
                #     print("ACTIVEEVENT:", e.state, e.gain)
                #     if e.state & APPMOUSEFOCUS == APPMOUSEFOCUS:
                #         print ('mouse focus ' + ('gained' if e.gain else 'lost'))
                #     if e.state & APPINPUTFOCUS == APPINPUTFOCUS:
                #         print ('input focus ' + ('gained' if e.gain else 'lost'))
                #     if e.state & APPACTIVE == APPACTIVE:
                #         print('app is ' + ('visibile' if e.gain else 'iconified'))

            if cap != None and sharedData.has_started== False:
                
                _ , frame = cap.read()
                height, width, _ = frame.shape
                screen_width = 300 + width
                screen_height = height
                self.screen = pygame.display.set_mode((screen_width, screen_height))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB format
                frame = np.rot90(frame)  # Rotate the frame if needed
                frame = pygame.surfarray.make_surface(frame)
                self.screen.blit(frame, (300, 0))
            else: 
                if self.is_initialized == False:
                    self.screen = pygame.display.set_mode((self.width, self.height))
                    self.hwnd = pygame.display.get_wm_info()["window"]
                    self.set_always_on_top()
                    self.is_initialized = True


            if sharedData is not None:
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

            pygame.display.flip()
            self.clock.tick(self.frame_rate)


if __name__ == "__main__":
    text = TextonScreen()
    cap = cv2.VideoCapture(0)
    text.main(cap=cap)



