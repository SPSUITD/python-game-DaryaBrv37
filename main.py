"""
Platformer Game
"""

import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Mooncalf"

# Константы, используемые для масштабирования наших спрайтов по сравнению с их первоначальным размером
CHARACTER_SCALING = 0.9
TILE_SCALING = 0.5
# Скорость перемещения игрока, в пикселях на кадр. Гравитация и скорость прыжка
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Вызовите родительский класс и настройте окно
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # Это "списки", которые отслеживают наши спрайты. Каждый спрайт должен
        # перейдите в список.
        # self.wall_list = None #набор плиточек стен ###
        # self.player_list = None #набор спрайтов ###

        # Отдельная переменная, содержащая спрайт проигрывателя
        self.player_sprite = None

        # Our Scene Object
        self.scene = None ###

        # Камера, которую можно использовать для прокрутки экрана
        self.camera = None

        # Our physics engine
        self.physics_engine = None
        self.player_jump = False
        self.jump_start = None
        self.camera_max = 0

        arcade.set_background_color(arcade.csscolor.MOCCASIN)
    def setup (self):

        # Инициализировать сцену
        self.camera = arcade.Camera(self.width, self.height)

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)


        # Initialize Scene ###
        self.scene = arcade.Scene() ###

        # Create the Sprite lists ###
        self.scene.add_sprite_list("Player") ###
        self.scene.add_sprite_list("Walls", use_spatial_hash=True) ###


        # Настройте проигрыватель, специально разместив его по этим координатам.

        image_source = "images/mooncalf.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 140

        self.scene.add_sprite("Player", self.player_sprite) ### Player вместо картинки

        # Создайте почву
        # Это показывает использование цикла для размещения нескольких спрайтов горизонтально
        for x in range(0, 1250, 63):
            wall = arcade.Sprite("images/zemlya.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 30

            self.scene.add_sprite("Walls", wall)

            self.jump_start = self.player_sprite.center_x

        # Поставьте несколько ящиков на землю
        # Это показывает использование списка координат для размещения спрайтов
        coordinate_list = [[540, 80], [300, 80], [768, 80]]

        for coordinate in coordinate_list:
            # Поставьте ящик на землю
            wall = arcade.Sprite(
                "images/barrier.png", TILE_SCALING
            )

            wall.position = coordinate
            self.wall_list.append(wall)


            self.scene.add_sprite("Walls", wall)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)



    def on_draw(self):
        """Render the screen."""

        # Очистите экран до цвета фона
        self.clear()

        # Activate our Camera
        self.camera.use()


        # Рисуем наши спрайты

        self.scene.draw() ### scene вместо player_list


    def on_update(self, delta_time):
        """Movement and game logic"""

        # Position the camera
        self.center_camera_to_player()

        self.player_sprite.center_x += 0
        self.physics_engine.update()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0



def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()



    #45:56 ЛЕКЦИЯ 26/02 ✓
    #  10:14  ЛЕКЦИЯ 5/03
