import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AleinFleet


class Alien(Sprite):
    #Alien for the horizontal-style game.

    #Moves UP/DOWN together with the fleet, and the whole fleet drifts LEFT.
    

    def __init__(self, fleet: 'AleinFleet', x: float, y: float):
        super().__init__()
        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = self.screen.get_rect()
        self.settings = fleet.game.settings

        # Load and scale alien image
        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(
            self.image,
            (self.settings.alien_w, self.settings.alien_h)
        )
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
        # Store as floats for smooth movement
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        #Move the alien UP/DOWN according to the fleet direction
        temp_speed = self.settings.fleet_speed
        self.y += temp_speed * self.fleet.fleet_direction
        self.rect.y = int(self.y)
        self.rect.x = int(self.x)

    def check_edges(self) -> bool:
        #Return True if alien hits TOP or BOTTOM of the screen
        return (
            self.rect.top <= self.boundaries.top or
            self.rect.bottom >= self.boundaries.bottom
        )

    def draw_alien(self):
        self.screen.blit(self.image, self.rect)