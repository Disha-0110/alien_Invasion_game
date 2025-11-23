import pygame
from bullet import Bullet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    

class Arsenal:
    def __init__(self, game: 'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()

    #update bullet states
    def update_arsenal(self):
        self.arsenal.update()
        self._remove_bullets_offscreen()
    
    #remove bullets off-screen
    def _remove_bullets_offscreen(self):
        for bullet in self.arsenal.copy():
            if bullet.rect.left >= self.settings.screen_w:
                self.arsenal.remove(bullet)
                
    #draw bullets
    def draw(self):
        for bullet in self.arsenal:
            bullet.draw_bullet()

    #fire bullets
    def fire_bullet(self):
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False