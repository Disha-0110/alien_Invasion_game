import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal


#handles image loading, movement , bullet firing, and drawing the ship of the screen.
class Ship:


    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal'):
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        original = pygame.image.load(self.settings.ship_file)
        original = pygame.transform.scale(original,
            (self.settings.ship_w, self.settings.ship_h)
            )
        self.image = pygame.transform.rotate(original, -90)

        self.rect = self.image.get_rect()
        self._center_ship()
        self.arsenal = arsenal 

    def _center_ship(self):
        #reset the ship to the left-center position
        self.rect.midleft = self.boundaries.midleft
        self.y = float(self.rect.y)
        

    def move_up(self):
        #move ship one step up when UP is pressed
        step = self.settings.ship_speed
        if self.rect.top - step >= 0:
            self.rect.y -= step  
        

    def move_down(self):
        #move ship one step up when DOWN is pressed
        step = self.settings.ship_speed
        if self.rect.bottom + step <= self.boundaries.bottom:
            self.rect.y += step
        

    def update(self):
        self.arsenal.update_arsenal()

    def draw(self):
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)
    def fire(self):
        return self.arsenal.fire_bullet()
    
    def check_collisions(self, other_group):
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False