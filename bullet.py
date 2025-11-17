import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):
    def __init__(self,game: 'AlienInvasion'):
        super().__init__()
        
        self.screen = game.screen
        self.settings = game.settings
        ship = game.ship

        image = pygame.image.load(self.settings.bullet_file)
        image = pygame.transform.scale(image,
            (self.settings.bullet_w, self.settings.bullet_h)
            )
        self.image = pygame.transform.rotate(image, -90)

        self.rect = self.image.get_rect()
        self.rect.midleft = ship.rect.midright
        self.x = float(self.rect.x)

    def update(self):
        self.x -= self.settings.bullet_speed
        self.rect.x = self.x

    def draw_bullet(self):
        self.screen.blit(self.image, self.rect)