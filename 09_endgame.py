"""
Platformer Game
"""
import arcade
import time
# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Proyecto Lunar"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.2
CHARACTER_BIGSCALING = 0.3
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED =10
GRAVITY = 0
PLAYER_JUMP_SPEED = 5

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
LEFT_VIEWPORT_MARGIN = 300
RIGHT_VIEWPORT_MARGIN = 300
BOTTOM_VIEWPORT_MARGIN = 250
TOP_VIEWPORT_MARGIN = 200

PLAYER_START_X = 640
PLAYER_START_Y = 940

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.coin_list = None
        self.wall_list = None
        self.foreground_list = None
        self.background_list = None
        self.dont_touch_list = None
        self.player_list = None
        # Background image will be stored in this variable
        self.background = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the luna
        self.luna = 0

        # Where is the right edge of the map?
        self.end_of_map = 0

        # Level
        self.level = 1

        #Vidas
        self.vidas = 3

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("sounds/coin1.wav")
        self.jump_sound = arcade.load_sound("sounds/jump1.wav")
        self.game_over = arcade.load_sound("sounds/gameover1.wav")

    def setup(self, level):
        """ Set up the game here. Call this function to restart the game. """

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the luna
        self.luna = 0
        self.tsluna = 0

        #Vidas
        self.vidas = 3

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.foreground_list = arcade.SpriteList()
        self.background_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        if self.level == 1:
           self.player_sprite_chico = arcade.Sprite("images/player_1/luna1.png", CHARACTER_SCALING)
           self.player_sprite_grande = arcade.Sprite("images/player_1/luna1.png", CHARACTER_BIGSCALING)
        if self.level == 2:
           self.player_sprite_chico = arcade.Sprite("images/player_1/luna2.png", CHARACTER_SCALING)
           self.player_sprite_grande = arcade.Sprite("images/player_1/luna2.png", CHARACTER_BIGSCALING)
        if self.level == 3:
           self.player_sprite_chico = arcade.Sprite("images/player_1/luna3.png", CHARACTER_SCALING)
           self.player_sprite_grande = arcade.Sprite("images/player_1/luna3.png", CHARACTER_BIGSCALING)
        self.player_sprite_chico.center_x = PLAYER_START_X
        self.player_sprite_chico.center_y = PLAYER_START_Y
        self.player_sprite= self.player_sprite_chico
        self.player_list.append(self.player_sprite)


        # --- Load in a map from the tiled editor ---

        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'plataforma'
        # Name of the layer that has items for pick-up
        coins_layer_name = 'monedas'
        # Name of the layer that has items for foreground
        foreground_layer_name = 'frente'
        # Name of the layer that has items for background
        background_layer_name = 'fondo'
        # Name of the layer that has items we shouldn't touch
        dont_touch_layer_name = "no tocar"

        # Map name
        if self.level ==-1:
            map_name = 'game_over.tmx'
        else:
            map_name = f"mapa_nivel_{self.level}.tmx"
        # Read in the tiled map
        my_map = arcade.read_tiled_map(map_name, TILE_SCALING)

        if self.level == 1:
            self.background = arcade.load_texture("images/fondo1.jpg")
        if self.level == 2:
            self.background = arcade.load_texture("images/fondo3.jpg")
        if self.level == 3:
            self.background = arcade.load_texture("images/fondo2.jpg")


        # -- Walls
        # Grab the layer of items we can't move through
        map_array = my_map.layers_int_data[platforms_layer_name]

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = len(map_array[0]) * GRID_PIXEL_SIZE

        # -- Background
        self.background_list = arcade.generate_sprites(my_map, background_layer_name, TILE_SCALING)

        # -- Foreground
        self.foreground_list = arcade.generate_sprites(my_map, foreground_layer_name, TILE_SCALING)

        # -- Platforms
        self.wall_list = arcade.generate_sprites(my_map, platforms_layer_name, TILE_SCALING)

        # -- Platforms
        self.wall_list = arcade.generate_sprites(my_map, platforms_layer_name, TILE_SCALING)

        # -- Coins
        self.coin_list = arcade.generate_sprites(my_map, coins_layer_name, TILE_SCALING)

        # -- Don't Touch Layer
        self.dont_touch_list = arcade.generate_sprites(my_map, dont_touch_layer_name, TILE_SCALING)

        self.end_of_map = (len(map_array[0]) - 1) * GRID_PIXEL_SIZE

        # --- Other stuff
        # Set the background color
        if my_map.backgroundcolor:
            arcade.set_background_color(my_map.backgroundcolor)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             GRAVITY)

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        # Draw the background texture
        if self.level==1:
            arcade.draw_texture_rectangle(SCREEN_WIDTH/2+self.view_left,SCREEN_HEIGHT/2+self.view_bottom,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        if self.level==2:
            arcade.draw_texture_rectangle(SCREEN_WIDTH/2+self.view_left,SCREEN_HEIGHT/2+self.view_bottom,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background2)

        # Draw our sprites
        self.wall_list.draw()
        self.background_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()
        self.dont_touch_list.draw()
        self.foreground_list.draw()

        if self.level != -1:
            self.player_list.draw()
        else:
            self.player_list.draw()
        # Draw our luna on the screen, scrolling it with the viewport
        if self.level != -1:
            luna_text = f"luna: {self.luna}"
            arcade.draw_text(luna_text, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.csscolor.YELLOW, 18)

        #MOSTRAR LA CANTIDAD DE VIDAS
        if self.level != -1:
            vidas_text = f"vidas: {self.vidas}"
            arcade.draw_text(vidas_text, 5 + self.view_left, self.view_bottom + SCREEN_HEIGHT -30,
                        arcade.csscolor.YELLOW, 18)





    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if self.level ==-1:
            self.level =1
            self.setup(1)

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED


    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0


    def update(self, delta_time):
        """ Movement and game logic """

        if self.tsluna > 0 and (time.time () - self.tsluna)> 1:
            self.tsluna = 0
            self.player_sprite_chico.center_x = self.player_sprite.center_x
            self.player_sprite_chico.center_y = self.player_sprite.center_y
            self.player_list = arcade.SpriteList()
            self.player_sprite = self.player_sprite_chico
            self.player_list.append(self.player_sprite)
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                                 self.wall_list,
                                                                 GRAVITY)
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        # See if we hit any coins
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.coin_list)

        # Loop through each coin we hit (if any) and remove it
        for coin in coin_hit_list:
            # Remove the coin
            coin.remove_from_sprite_lists()
            # Play a sound
            arcade.play_sound(self.collect_coin_sound)
            # Add one to the luna
            self.luna += 1
            self.tsluna = time.time()
            self.player_sprite_grande.center_x = self.player_sprite.center_x
            self.player_sprite_grande.center_y = self.player_sprite.center_y
            self.player_list = arcade.SpriteList()
            self.player_sprite = self.player_sprite_grande
            self.player_list.append(self.player_sprite)
            self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                                 self.wall_list,
                                                                 GRAVITY)
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0


        # Track if we need to change the viewport
        changed_viewport = False

        # Cuando el jugador toca algo que no deberia.
        if arcade.check_for_collision_with_list(self.player_sprite, self.dont_touch_list):
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True
            arcade.play_sound(self.game_over)

            #Quitar una vida y verificar si llega  0 vidas.
            self.vidas -=1

            #Si llega a 0 vidas volver a comenzar el juego.
        if self.vidas == 0:
            self.level =-1
            self.setup(self.level)


        # See if the user got to the end of the level
        if self.luna == 10 and self.level == 1:
            # Advance to the next level
            self.level = 2

            # Load the next level
            self.setup(self.level)

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

        # See if the user got to the end of the level
        if self.luna == 20 and self.level==2:
            # Advance to the next level
            self.level = 3

            # Load the next level
            self.setup(self.level)

            # Set the camera to the start
            self.view_left = 0
            self.view_bottom = 0
            changed_viewport = True

        # --- Manage Scrolling ---

        # Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed_viewport = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        if changed_viewport:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


def main():
    """ Main method """
    window = MyGame()
    window.setup(window.level)
    arcade.run()


if __name__ == "__main__":
    main()
