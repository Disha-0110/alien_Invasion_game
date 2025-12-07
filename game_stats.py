
import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class GameStats:
    '''Track statistics for the Alien Invasion game.'''

    def __init__(self, game: 'AlienInvasion'):
        '''Initialize statistics and load saved high socre.'''
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        #load saved high scores
        self.init_saved_scores()
        #reset starts for a new game
        self.reset_stats()
    
    def init_saved_scores(self):
        '''load high score from file if available 
        otherwise initialize file with default value'''
        self.path = self.settings.scores_file
        if self.path.exists() and self.path.stat.__sizeof__() > 0:
            contents = self.path.read_text()
            scores = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)

        else:
            self.hi_score = 0
            self.save_scores()
            
    def save_scores(self):
        '''save high score to file.'''
        scores = {'hi_score': self.hi_score}
        contents = json.dumps(scores, indent=4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f'File Note Found: {e}')

    def reset_stats(self):
        '''reset statistics that change during the game'''
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1

    def update(self,collisions):
        '''update game statistics after alien collisions'''
        self._update_score(collisions)
        self._update_max_score()
        self._update_hi_score()

    def _update_score(self, collisions):
        '''Increase the score based on number of aliens destroyed'''
        for alien in collisions.values():
            self.score += self.settings.alien_points
    
    def _update_max_score(self):
        '''track the highest score'''
        if self.score > self.max_score:
            self.max_score = self.score

    def _update_hi_score(self):
        '''update and save the all time high score'''
        if self.score > self.hi_score:
            self.hi_score = self.score

    def update_level(self):
        '''increase level afetr clearing a wave of alien'''
        self.level += 1
        print(self.level)