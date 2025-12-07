import pygame
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from alien import Alien


class AleinFleet:
    #Fleet that lives on the RIGHT side and moves toward the rocket on the LEFT

    def __init__(self, game: 'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()

        # fleet moves UP/DOWN (1 = down, -1 = up)
        self.fleet_direction = self.settings.fleet_direction
        # when bouncing off top/bottom, move LEFT by this much
        self.fleet_drop_speed = self.settings.fleet_drop_speed

    def create_fleet(self):
        #Create a grid of aliens on the RIGHT half of the screen
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        # simple grid in right half: cols go left from near right edge
        cols = 6
        rows = 9

        # start a bit away from the right edge
        x_start = screen_w - alien_w * 2

        # spread vertically from some margin
        y_margin = alien_h
        for row in range(rows):
            for col in range(cols):
                x = x_start - col * alien_w * 2
                y = y_margin + row * alien_h * 2
                self._create_alien(x, y)

    def _create_alien(self, current_x: int, current_y: int):
        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        #If any alien hits TOP or BOTTOM, move fleet LEFT and reverse direction
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break
        
    def _drop_alien_fleet(self):
        #Move whole fleet LEFT when bouncing off top/bottom
        for alien in self.fleet:
            alien.x -= self.fleet_drop_speed

    def update_fleet(self):
        self._check_fleet_edges()
        self.fleet.update()

    def draw(self):
        alien: Alien
        for alien in self.fleet:
            alien.draw_alien()

    def check_collisions(self, other_group):
        #Return collisions between aliens and bullets (delete both)
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)
    
    def check_fleet_behind_ship(self) -> bool:
        #Return True if any alien reaches the LEFT edge (behind the rocket)
        for alien in self.fleet:
            if alien.rect.left <= 0:
                return True
        return False
    
    def checked_destroyed_status(self) -> bool:
        #Return True if the whole fleet is gone
        return not self.fleet