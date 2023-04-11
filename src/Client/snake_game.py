import pygame
import random
from enum import Enum
from collections import namedtuple
import pygame_menu
from pygame_menu import themes
from time import sleep
import sys
pygame.init()
font = pygame.font.Font('static/Retro Gaming.ttf', 25)
surface = pygame.display.set_mode((640, 480))

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
AQUA = (0, 255, 255)
AQUAMARINE4 = (69, 139, 116)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 15


class SnakeGameClient:

    def __init__(self, w=640, h=480, difficulty=15):
        self.w = w
        self.h = h
        self.difficulty=difficulty
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('SnakeGame')
        self.clock = pygame.time.Clock()

        # init game state
        self.direction = Direction.RIGHT

        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head,
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]

        self.score = 0
        self.food = None
        self._place_food()

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()

    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # 2. move
        self._move(self.direction)  # update the head
        self.snake.insert(0, self.head)

        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(self.difficulty)
        # 6. return game over and score
        return game_over, self.score

    def _is_collision(self):
        # hits boundary
        if self.head.x > self.w - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h - BLOCK_SIZE or self.head.y < 0:
            return True
        # hits itself
        if self.head in self.snake[1:]:
            return True

        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        for pt in self.snake:
            pygame.draw.rect(self.display, AQUA, pygame.Rect(
                pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, AQUAMARINE4,
                             pygame.Rect(pt.x+4, pt.y+4, 12, 12))

        pygame.draw.rect(self.display, RED, pygame.Rect(
            self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)
'''
def main_game():
    game = SnakeGameClient()

    # game loop
    while True:
        game_over, score = game.play_step()

        if game_over:
            break

    print('Final Score', score)

    main_menu()


def main_menu():
    pygame.init()
    font = pygame.font.Font('static/Retro Gaming.ttf', 25)
    surface = pygame.display.set_mode((640, 480))
    # Create menu
    my_theme = themes.Theme(
        background_color=BLACK,
        title_font=font,
        widget_font=font,
        widget_alignment=pygame_menu.locals.ALIGN_CENTER,
        title_offset=(0, 20)
    )

    menu = pygame_menu.Menu(
        height=480,
        theme=my_theme,
        title='Snake Game',
        width=640
    )

    def exit_game(*args, **kwargs):
        pygame.quit()
        sys.exit()

    def play_game():
        main_game()
        return pygame_menu.events.RESET
    def level_menu():
        menu._open(level)
    menu.add.button('Press Enter to Play', play_game)
    menu.add.button('Change Difficulty', level_menu)
    menu.add.button('Press Enter to Quit', exit_game)
    level = pygame_menu.Menu('Select a Difficulty', 640, 480, theme=my_theme)
    level.add.button('Easy', play_game)
    level.add.button('Medium', play_game)
    level.add.button('Hard', play_game)
    level.add.button('Extreme', play_game)
    #menu.add.text_input('Press Enter to Play', onreturn=play_game, readonly=True, textinput_id='play_button')
    #menu.add.text_input('Press Enter to Quit', onreturn=exit_game, readonly=True, textinput_id='quit_button')

    # Display menu
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        menu_status = menu.update(events)
        menu.draw(surface)
        pygame.display.update()
        pygame.time.Clock().tick(30)

        if menu_status == pygame_menu.events.EXIT:
            break



#if __name__ == '__main__':
   # main_menu()





if __name__ == '__main__':
    game = SnakeGameClient()

    # game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()
'''