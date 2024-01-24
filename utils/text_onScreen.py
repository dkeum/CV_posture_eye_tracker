import pygame
import sys
import os
import queue
import win32gui
import win32con


class TextonScreen():

    def __init__(self, x=0, y=0, text="Thumbs Up to Start"):
        # Initialize Pygame
        pygame.init()

        screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

        # Set up the display
        width, height = 300, 200
        self.screen = pygame.display.set_mode((width, height), pygame.NOFRAME)  # Hide window frame
        self.hwnd = pygame.display.get_wm_info()["window"]

        pygame.display.set_caption("Text Display")
        self.set_always_on_top()

        # Create a font object
        self.font = pygame.font.Font(None, 36)

        # Create a text surface
        self.text_surface = self.font.render(text, True, (255, 255, 255))

        self.text_position = (10, 10)  # top left

        self.clock = pygame.time.Clock()
        self.frame_rate = 10  # Set your desired frame rate here

    def set_always_on_top(self):
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, 0, 0, 300, 200,
                            0x0001)

    def main(self, sharedData=None):

        # Main game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if sharedData is not None:
                text = sharedData.message_to_display1
                if text != "":
                    pygame.draw.rect(self.screen, (0, 0, 0), (0, 0, 300, 50))
                    if text == "good posture detected":
                        font_color = (0, 255, 0)
                    elif text == "bad posture detected":
                        font_color = (255, 0, 0)
                    else:
                        font_color = (255, 255, 255)
                    self.text_surface = self.font.render(text, True, font_color)

                text2 = sharedData.message_to_display2
                if text2 != "":
                    pygame.draw.rect(self.screen, (0, 0, 0), (0, 50, 300, 50))
                    if text2 == "5 min break":
                        font_color = (255, 0, 0)
                    else:
                        font_color = (255, 255, 255)
                    self.text_surface2 = self.font.render(text2, True, font_color)
                    text2_position = (self.text_position[0], self.text_position[1] + 50)
                    self.screen.blit(self.text_surface2, text2_position)

                text3 = sharedData.message_to_display3
                if text3 != "":
                    pygame.draw.rect(self.screen, (0, 0, 0), (0, 100, 300, 150))
                    if int(text3[14:]) <= 8 and int(text3[14:]) != 0:
                        font_color = (255, 0, 0)
                    else:
                        font_color = (0, 255, 0)
                    self.text_surface3 = self.font.render(text3, True, font_color)
                    text3_position = (self.text_position[0], self.text_position[1] + 100)
                    self.screen.blit(self.text_surface3, text3_position)

            self.screen.blit(self.text_surface, self.text_position)
            pygame.display.flip()

            self.clock.tick(self.frame_rate)


if __name__ == "__main__":
    text = TextonScreen()
    text.main()
