import pygame
from enum import Enum
from collections import namedtuple
import pygame_menu
from pygame_menu import themes
from time import sleep
import sys

from src.Client.snake_game import SnakeGameClient,Direction,Point
from src.AI.agent_driver import AgentDriver 
from src.AI.train import Train


#Constants 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
AQUA = (0, 255, 255)
AQUAMARINE4 = (69, 139, 116)
class GameDriver:
    def __init__(self):
        pass 
    def run(self):
        self.main_menu()

    def main_game(self, d=15):
        game = SnakeGameClient(difficulty=d)

        # game loop
        while True:
            game_over, score = game.play_step()

            if game_over:
                break

        print('Final Score', score)

   
    def main_game_AI(self):
        agent = AgentDriver()
        agent.run()
        
    def train_game(self):
        agent = Train()
        agent.run()
    
    def main_menu(self):
        pygame.init()
        
        font = pygame.font.Font('static/Retro Gaming.ttf', 25)
        surface = pygame.display.set_mode((640, 480))
        # Create menu
        my_theme = themes.Theme(
            background_color=BLACK,
            title_font=font,
            widget_font=font,
            widget_font_color=WHITE,
            widget_alignment=pygame_menu.locals.ALIGN_CENTER,
            title_offset=(0, 20),
            selection_color=AQUAMARINE4,
            cursor_color=AQUA,
            cursor_selection_color=AQUAMARINE4,
           
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
 
        def play_easy():
            self.main_game(d=10)
            menu._open(end)
            
        def play_medium():
            self.main_game(d=15)
            menu._open(end)

        def play_hard():
            self.main_game(d=20)
            menu._open(end)

        def play_extreme():
            self.main_game(d=40)
            menu._open(end)

        def play_game_AI():
            self.main_game_AI()
            menu._open(end)

        def play_train():
            self.train_game()
            menu._open(end)

        def level_menu():
            menu._open(level)

        def select_menu():
            menu._open(player)

        def train_menu():
            menu._open(trainer)

        menu.add.button('Press Enter to Play', select_menu)
        menu.add.button('Press Enter to Train AI', train_menu)
        menu.add.button('Press Enter to Quit', exit_game)
        level = pygame_menu.Menu('Select a Difficulty', 640, 480, theme=my_theme)
        level.add.button('Easy', play_easy)
        level.add.button('Medium', play_medium)
        level.add.button('Hard', play_hard)
        level.add.button('Extreme', play_extreme)
        level.add.button('Return to Main Menu', pygame_menu.events.BACK)

        player = pygame_menu.Menu('Select a Player', 640, 480, theme=my_theme)
        player.add.button('Human (You)', level_menu)
        player.add.button('Artificial Intelligence', play_game_AI)
        
        player.add.button('Return to Main Menu', pygame_menu.events.BACK)
        
        end = pygame_menu.Menu('GAME OVER', 640, 480, theme=my_theme)
        end.add.button('Play Again', level_menu)
        end.add.button('Return to Main Menu', pygame_menu.events.RESET)
        end.add.button('Quit',exit_game )

        trainer=pygame_menu.Menu('AI Trainer', 640, 480, theme=my_theme)
        trainer.add.button('Train AI (10 games): (cntrl-c to end)', play_train)
        trainer.add.button('Return to Main Menu', pygame_menu.events.RESET)

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