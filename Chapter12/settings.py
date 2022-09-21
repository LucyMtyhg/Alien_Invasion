class Settings():

   def __init__(self):
      # Screen settings
      self.screen_width = 800
      self.screen_height = 500
      self.bg_color = (2, 230, 230)

      #Ship settings
      self.ship_speed_factor = 0.4
      self.ship_limit = 3

      # Bullet settings
      self.bullet_speed_factor = 1
      self.bullet_width = 3
      self.bullet_height = 15
      self.bullet_color = 60, 60, 60

      # Alien settings
      self.alien_speed_factor = 0.1
      self.fleet_drop_speed = 10

      # fleet_direction of 1 represents right; -1 represents left.
      self.fleet_direction = 1
