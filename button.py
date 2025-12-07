import pygame.font
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Button:
    '''a class to create and manage buttons'''
    def __init__(self, game: 'AlienInvasion', msg):
        '''initialize button attributes'''
        self.game = game
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings = game.settings
        #font setup from setting
        self.font = pygame.font.Font(self.settings.font_file, self.settings.button_font_size)
        #build the button's rect and center it
        self.rect = pygame.Rect(0,0,self.settings.button_w, self.settings.button_h)
        self.rect.center = self.boundaries.center
        #prepare message to render once
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        '''convert message text into a rendered image'''
        self.msg_image = self.font.render(msg, True, self.settings.text_color, None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        '''draw button and text to screen'''
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        

    def check_clicked(self, mouse_pos):
        '''returns true if button is clicked'''
        return self.rect.collidepoint(mouse_pos)