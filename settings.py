from pathlib import Path 

class Settings:

    def __init__(self):
        #window title shown at the top of the screen
        self.name: str = 'Alien Invasion'

        #Width and height of the game screen (in pixels)
        self.screen_w = 1200
        self.screen_h = 800

        #Frames per seconds- how fast game refreshes
        self.FPS = 60

        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'Starbasesnow.png'
        self.ship_file =  Path.cwd() / 'Assets' / 'images' / 'ship2(no bg).png'

        #ship widht and height
        self.ship_w = 40
        self.ship_h = 60

        # how ship moves when press UP and DOWN
        self.ship_speed = 20
        self.starting_ship_count = 3 #for lives

        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'laserBlast.png'  
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'laser.mp3' 
        self.impact_sound = Path.cwd() / 'Assets' / 'sound' / 'impactSound.mp3'
        
        #how fast the bullet travels across the screen
        self.bullet_speed = 9
        self.bullet_w = 50
        self.bullet_h = 25
        
        #max number of bullets allowed on screen at the same time
        self.bullet_amount = 8 

        #Fleet settings
        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'enemy_4.png'
        self.alien_w = 40
        self.alien_h = 40

        #fleet moves up and down
        self.fleet_speed = 2
        self.fleet_direction = 1
        self.fleet_drop_speed = 40