"""
Platformer Game
"""

import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
IMAGE_WIDTH = 16.048
SCREEN_TITLE = "Mooncalf"

# Константы, используемые для масштабирования наших спрайтов по сравнению с их первоначальным размером
CHARACTER_SCALING = 0.9

TILE_SCALING = 0.5

# Скорость перемещения игрока, в пикселях на кадр. Гравитация и скорость прыжка
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1.5
PLAYER_JUMP_SPEED = 20

COIN_SCALING = 0.25

PLAYER_SPRITE_IMAGE_CHANGE_SPEED = 20
RIGHT_FACING = 0
LEFT_FACING = 1

frameInSecond = 0
isKeyPresed = False
isKeyLeft = False
isCameraCentered = False
startCenterPosition_X = 0

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Вызовите родительский класс и настройте окно
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        # Это "списки", которые отслеживают наши спрайты. Каждый спрайт должен
        # перейдите в список.

        self.wall_list = None #набор плиточек стен
        self.player_list = None #набор спрайтов

        self.player_sprite_images = []
        self.player_sprite_images_left = []

        # Фоновое изображение будет сохранено в этой переменной
        self.background = None

        # Отдельная переменная, содержащая спрайт проигрывателя
        self.player_sprite = None

        # Our Scene Object
        self.scene = None

        # Камера, которую можно использовать для прокрутки экрана
        self.camera = None

        # Камера, которую можно использовать для рисования элементов графического интерфейса
        self.gui_camera = None

        # Следите за результатом
        self.score = 0

        # Load sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

        # Our physics engine
        self.physics_engine = None
        self.player_jump = False
        self.jump_start = None
        self.camera_max = 0
        self.collide = False

        arcade.set_background_color(arcade.csscolor.MOCCASIN)
    def setup (self):
        # Загрузите фоновое изображение

        self.background_list = arcade.SpriteList()

        image_source = "images/moon1.png"
        image_source = "images/moon2.png"

        self.background_sprite = arcade.Sprite("images/bg.png")

        self.background_sprite.center_x = IMAGE_WIDTH // 0.0020
        self.background_sprite.center_y = SCREEN_HEIGHT // 1.9
        self.background_sprite.change_x = 0

        self.background_list.append(self.background_sprite)

        global startCenterPosition_X
        startCenterPosition_X = self.background_list.center[0]

        for i in range(1, 4):
            self.player_sprite_images.append(arcade.load_texture(f"images/moon{i}.png"))
        for i in range(1, 4):
            self.player_sprite_images_left.append(arcade.load_texture(f"images/moon{i}.png", flipped_horizontally=True))

        # Инициализировать сцену
        self.camera = arcade.Camera(self.width, self.height)

        #  Настройка камеры с графическим интерфейсом
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Следите за результатом
        self.score = 0

        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)


        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)


        # Настройте проигрыватель, специально разместив его по этим координатам.

        image_source = "images/moon3.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 100
        self.player_sprite.center_y = 140

        self.scene.add_sprite("Player", self.player_sprite)

        # Создайте почву
        # Это показывает использование цикла для размещения нескольких спрайтов горизонтально
        for x in range(0, 16848, 63):
            wall = arcade.Sprite("images/zemlya.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 30


            self.scene.add_sprite("Walls", wall)

            self.jump_start = self.player_sprite.center_x

        # Поставьте несколько ящиков на землю
        # Это показывает использование списка координат для размещения спрайтов
        coordinate_list = [[540, 80], [300, 80], [768, 80], [1250, 80], [1500, 80],
                           [1800, 80], [2300, 80], [2700, 80], [2950, 80], [3500, 80],
                           [4500, 80], [4750, 80], [4990, 80], [5300, 80], [5650, 80],
                           [5999, 80], [6400, 80], [6800, 80], [7100, 80], [7400, 80],
                           [7800, 80], [8150, 80], [8400, 80], [9000, 80], [9500, 80],
                           [10000, 80], [10200, 80], [10750, 80], [10900, 80], [11200, 80],
                           [11500, 80], [11700, 80], [11980, 80], [12200, 80], [12600, 80],
                           [13000, 80], [13300, 80], [13600, 80], [14200, 80], [14400, 80],
                           [14800, 80], [15200, 80], [15600, 80]]

        for coordinate in coordinate_list:
            # Поставьте ящик на землю
            wall = arcade.Sprite(
                "images/barrier.png", TILE_SCALING
            )

            wall.position = coordinate
            self.wall_list.append(wall)


            self.scene.add_sprite("Walls", wall)

        # # Используйте цикл, чтобы поместить несколько монет, которые сможет забрать наш персонаж.
        for x in (620, 380, 848, 1330, 1580, 1720, 1880, 2000, 2080, 2380,
                  2780, 3580, 3680, 3740, 3800, 4000, 4200, 4280, 4580, 5080,
                  5380, 5730, 6080, 6480, 7180, 7480, 7880, 8230, 8480, 8560,
                  8660, 9180, 9280, 9380, 9880, 10080, 10280, 10580, 10830, 10980,
                  11280, 11580, 11780, 12080, 12680, 12780, 12880, 13080, 13680,
                  14280, 14480, 14880, 15280):
            coin = arcade.Sprite("images/coin.png", COIN_SCALING)
            coin.center_x = x
            coin.center_y = 96
            self.scene.add_sprite("Coins", coin)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
        )
        #self.background_sprite.center_x

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        #screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        if self.player_sprite.center_y - (self.camera.viewport_height / 2) >= self.camera_max:
            screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)
            self.camera_max = self.player_sprite.center_y - (self.camera.viewport_height / 2)
        else:
            screen_center_y = self.camera_max

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.background_sprite.center_x = -screen_center_x + startCenterPosition_X
        self.camera.move_to(player_centered)



    def on_draw(self):
        """Render the screen."""

        # Очистите экран до цвета фона
        self.clear()

        arcade.start_render()
        self.background_list.draw()


        # Activate our Camera
        self.camera.use()

        # Рисуем наши спрайты
        self.wall_list.draw()
        self.player_list.draw()

        #arcade.draw_lrwh_rectangle_textured(0, 30, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)


        self.scene.draw()

        # Активируйте камеру графического интерфейса перед рисованием элементов графического интерфейса
        self.gui_camera.use()

        # Нарисуйте наш результат на экране, прокручивая его с помощью окна просмотра
        score_text = f"Coin: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )


    def on_update(self, delta_time):
        """Movement and game logic"""

        # Position the camera
        self.center_camera_to_player()

        if self.player_jump:
            self.player_sprite.center_y += 2
            if self.player_sprite.center_y > self.jump_start + 10:
                self.player_jump = False
        else:
            self.player_sprite.center_y -= 2


        self.player_sprite.center_x += 0
        self.physics_engine.update()

        # # Посмотрим, попадется ли нам хоть одна монетка
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        # Перебираем каждую попавшую монету (если таковая имеется) и удаляем ее
        for coin in coin_hit_list:
            # Достаньте монету
            coin.remove_from_sprite_lists()
            # Воспроизвести звук
            arcade.play_sound(self.collect_coin_sound)
            self.score += 1

        #сбрасывайте изображения,когда они выходятза пределы экрана
        if self.background_sprite.left == -IMAGE_WIDTH:
            self.background_sprite.center_x = SCREEN_WIDTH + IMAGE_WIDTH // 2


        self.background_list.update()
        global frameInSecond
        if (isKeyPresed):
            if (isKeyLeft):
                frameInSecond += 1
                if (frameInSecond < 20):
                    self.player_sprite.texture = self.player_sprite_images_left[0]
                elif (frameInSecond < 40):
                    self.player_sprite.texture = self.player_sprite_images_left[1]
                elif (frameInSecond < 60):
                    self.player_sprite.texture = self.player_sprite_images_left[2]
                elif (frameInSecond < 80):
                    self.player_sprite.texture = self.player_sprite_images_left[1]
                else: frameInSecond = 0
            else:
                frameInSecond += 1
                if (frameInSecond < 20):
                    self.player_sprite.texture = self.player_sprite_images[0]
                elif (frameInSecond < 40):
                    self.player_sprite.texture = self.player_sprite_images[1]
                elif (frameInSecond < 60):
                    self.player_sprite.texture = self.player_sprite_images[2]
                elif (frameInSecond < 80):
                    self.player_sprite.texture = self.player_sprite_images[1]
                else: frameInSecond = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        global isKeyPresed
        global isKeyLeft
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.player_jump = True
            self.jump_start = self.player_sprite.center_y
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
            isKeyPresed = True
            isKeyLeft = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
            isKeyPresed = True
            isKeyLeft = False

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""
        global isKeyPresed
        global isKeyLeft 
        if key == arcade.key.UP or key == arcade.key.W or key == arcade.key.SPACE:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
            isKeyPresed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
            isKeyPresed = False

def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()