import sys
from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        # Create a new bullet and add it to the bullets group.
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)   
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
            ship.moving_right = False  
    elif event.key == pygame.K_LEFT:
            ship.moving_left = False


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
            #mouse_x, mouse_y = pygame.mouse.get_pos()
            #check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y)    
        
def check_play_button(ai_settings, screen, stats, play_button, ship, aliens, bullets, mouse_x, mouse_y):
        button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
        if button_clicked and not stats.game_active:
            pygame.mouse.set_visible(False)     
        
        if play_button.rect.collidepoint(mouse_x, mouse_y):
            stats.reset_stats()
            stats.game_active = True
        # Empty the list of aliens and bullets.
        aliens.empty()
        bullets.empty() 
         # Create a new fleet and center the ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
 
#Start a new game when the player clicks Play."""
    #button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    #if button_clicked and not stats.game_active:
       # Hide the mouse cursor.
        #pygame.mouse.set_visible(False) 
        #
        # stats.reset_stats()
  

def update_bullets(ai_settings, screen, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets):
 #Respond to bullet-alien collisions."""
 # Remove any bullets and aliens that have collided.    
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if len(aliens) == 0:
 #Destroy existing bullets and create new fleet.
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
#Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height -
                        (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
 #reate a full fleet of aliens,Create an alien and find the number of aliens in a row.
 # Spacing between each alien is equal to one alien width.
    alien = Alien(ai_settings, screen)
    #alien_width = alien.rect.width
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
        alien.rect.height)
 #create fleet of aliens
    for row_number in range(number_rows):
 # Create the first row of aliens.
        for alien_number in range(number_aliens_x):
 # Create an alien and place it in the row.
            #alien = Alien(ai_settings, screen)
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings, aliens):
    #Respond appropriately if any aliens have reached an edge."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    #Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
 #Respond to ship being hit by alien."""..Decrement ships_left.
    
    if stats.ships_left > 0:
       stats.ships_left -= 1
    # Empty the list of aliens and bullets.
       aliens.empty()
       bullets.empty()
    # Create a new fleet and center the ship.
       create_fleet(ai_settings, screen, ship, aliens)
       ship.center_ship()
      # pygame.mouse.set_visible(True)
    # Pause.
       sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
#Check if any aliens have reached the bottom of the screen."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
 # Treat this the same as if the ship got hit.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break 


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):     
    check_fleet_edges(ai_settings, aliens)   
    aliens.update()
    # Look for alien-ship collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
        print("Ship hit!!!")
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def update_screen(ai_settings, screen, stats, ship, aliens, bullets, play_button):
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color) 
    for bullet in bullets:
        bullet.draw_bullet()

    # Draw the play button if the game is inactive.
    if not stats.game_active:
        play_button.draw_button()

    ship.blitme()
    aliens.draw(screen)  
    pygame.display.flip()
