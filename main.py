"""
Platformer Game
"""

import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Mooncalf"

# Константы, используемые для масштабирования наших спрайтов по сравнению с их первоначальным размером
CHARACTER_SCALING = 0.055
TILE_SCALING = 0.5

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

        # Отдельная переменная, содержащая спрайт проигрывателя
        self.player_sprite = None

        arcade.set_background_color(arcade.csscolor.MOCCASIN)

    def setup (self):
        """Set up the game here. Call this function to restart the game."""
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Настройте проигрыватель, специально разместив его по этим координатам.
        image_source = "images/mooncalf_pic.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 70
        self.player_sprite.center_y = 140
        self.player_list.append(self.player_sprite)

        # Создайте почву
        # Это показывает использование цикла для размещения нескольких спрайтов горизонтально
        for x in range(0, 1250, 64):
            wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)

        # Поставьте несколько ящиков на землю
        # Это показывает использование списка координат для размещения спрайтов
        coordinate_list = [[512, 96], [256, 96], [768, 96]]

        for coordinate in coordinate_list:
            # Поставьте ящик на землю
            wall = arcade.Sprite(
                ":resources:images/tiles/boxCrate_double.png", TILE_SCALING
            )
            wall.position = coordinate
            self.wall_list.append(wall)

    def on_draw(self):
        """Render the screen."""

        self.clear()
        # Очистите экран до цвета фона

        # Рисуем наши спрайты
        self.wall_list.draw()
        self.player_list.draw()


def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()



    #45:56 ЛЕКЦИЯ 26/02