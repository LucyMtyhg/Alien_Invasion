from time import sleep
import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
import games_functions as gf

def run_game():
    # Initialize game and create a screen object.
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, 
    ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")  

    #Make the Play button.
    play_button = Button(ai_settings, screen, "Play")
  
    # Create an instance to store game statistics.
    stats = GameStats(ai_settings)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    #alien =  Alien(ai_settings, screen)
    #created an empty group called aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)
    #make the instance of the alien


    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
        
        gf.update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button)

run_game()


#pip 22.2.2 from C:\Users\Lucia\AppData\Local\Programs\Python\Python310\lib\site-packages\pip (python 3.10)


