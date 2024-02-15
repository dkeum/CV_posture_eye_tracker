
import pygame 

class UI:
    @staticmethod
    def init(app):
        UI.font = pygame.font.Font(None, 30)
        UI.sfont = pygame.font.Font(None, 20)
        UI.lfont = pygame.font.Font(None, 40)
        UI.xlfont = pygame.font.Font(None, 50)
        UI.center = (app.screen.get_size()[0]//2, app.screen.get_size()[1]//2)
        UI.half_width = app.screen.get_size()[0]//2
        UI.half_height = app.screen.get_size()[1]//2

        UI.fonts = {
            'sm':UI.sfont,
            'm':UI.font,
            'l':UI.lfont,
            'xl':UI.xlfont
        }
