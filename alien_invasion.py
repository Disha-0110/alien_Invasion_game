import sys
import pygame
from time import sleep
from settings import Settings
from ship import Ship
from arsenal import Arsenal 
from alien_fleet import AleinFleet
from game_stats import GameStats
from button import Button
from hud import HUD

class AlienInvasion:

    def __init__(self):
        pygame.init()
        self.settings = Settings()
        #required for difficulty reset
        self.settings.initialize_dynamic_settings()
        # screen setup
        self.screen = pygame.display.set_mode(
            (self.settings.screen_w,self.settings.screen_h)
            ) 
        pygame.display.set_caption(self.settings.name)
        #Background image
        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, (self.settings.screen_w, self.settings.screen_h))

        #add GameStats and HUD
        self.game_stats = GameStats(self)
        self.HUD = HUD(self)
        self.running = True
        self.clock = pygame.time.Clock()

        #laser sound setup
        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.50)
        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)
        #game objects
        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AleinFleet(self)
        self.alien_fleet.create_fleet()

        #play button
        self.play_button = Button(self, "Play")
        #game starts inactive
        self.game_active = False

    def run_game(self):
        #main game loop
        while self.running:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)

                
    def _check_collisions(self):
        '''handle all collision logic'''
    #ship collides with alien reset 
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()
            
    # Alein reaches left edge, it resets
        if self.alien_fleet.check_fleet_behind_ship():
            self._check_game_status()

            
    
        # bullets vs aliens
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(500)
        #update stats + HUD when bullet hits
            self.game_stats.update(collisions)
            self.HUD.update_scores()

        # if all aliens destroyed, reset fleet
        if self.alien_fleet.checked_destroyed_status():
            self._reset_level()
            self.settings.increase_difficulty()
            #level progression
            self.game_stats.update_level()
            self.HUD.update_level()

    def _check_game_status(self):
        #Handle lives and reset or end game
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            #game becomes inactive, button shows
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _reset_level(self):
        #reset bullets and aliens, but keep ship and settings
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()
        self.ship._center_ship()

    def restart_game(self):
        '''reset everything for a new game'''
        self.settings.initialize_dynamic_settings()
        self.game_stats.reset_stats()
        #refresh HUD visuals
        self.HUD.update_scores()
        self.HUD.update_level()
        #reset positions
        self._reset_level()
        self.ship._center_ship()
        self.game_active = True
        pygame.mouse.set_visible(False)

    #called when clicking play button
    def _update_screen(self):
        '''draw background, ship, aliens, HUD and button when needed'''
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.HUD.draw()

        #draw play button if game inactive
        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)
        pygame.display.flip()


    def _check_events(self):
        '''handle keyboard input, clicking, and quitting'''
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                #save scores on quit
                self.game_stats.save_scores()
                #self.running = False
                pygame.quit()
                sys.exit()
            #movement onl works when game is active    
            elif event.type == pygame.KEYDOWN and self.game_active:
                self._check_keydown_events(event)
            #clicking play button
            elif event.type == pygame.KEYUP and self.game_active:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()

    def _check_button_clicked(self):
        '''Start the game if play button was pressed'''
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self.restart_game()
            
    def _check_keydown_events(self, event):
        '''handle sideways ship movement and bullet firing'''
        if event.key ==pygame.K_UP:
            self.ship.move_up()
        elif event.key ==pygame.K_DOWN:
            self.ship.move_down()
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                self.laser_sound.play()
                self.laser_sound.fadeout(200)
                
        elif event.key == pygame.K_q:
            self.game_stats.save_scores
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()