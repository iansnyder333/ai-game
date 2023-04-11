from time import sleep
import pygame
import pygame_menu
from pygame_menu import themes
from snake_game import SnakeGameClient

pygame.init()
surface = pygame.display.set_mode((640, 480))
difficulty = 15
def set_difficulty(value, difficulty):
    difficulty=difficulty
 
def start_the_game(val=15):
    game = SnakeGameClient(difficulty=val)

    # game loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score', score)

    pygame.quit()

    
 
def level_menu():
    mainmenu._open(level)
 
 
mainmenu = pygame_menu.Menu('Welcome', 640, 480, theme=themes.THEME_SOLARIZED)
mainmenu.add.text_input('Name: ', default='username')
mainmenu.add.button('Play', start_the_game)
mainmenu.add.button('Levels', level_menu)
mainmenu.add.button('Quit', pygame_menu.events.EXIT)
level = pygame_menu.Menu('Select a Difficulty', 640, 480, theme=themes.THEME_BLUE)
level.add.button('Easy', start_the_game(15))
level.add.selector('Difficulty :', [('Easy', 10), ('Medium', 15),('Hard', 20), ('Extreme', 40) ], onchange=set_difficulty)
 
loading = pygame_menu.Menu('Loading the Game...', 640, 480, theme=themes.THEME_DARK)
loading.add.progress_bar("Get Ready!", progressbar_id = "1", default=0, width = 200, )

arrow = pygame_menu.widgets.LeftArrowSelection(arrow_size = (10, 15))
 
update_loading = pygame.USEREVENT + 0
if __name__=='__main__':
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == update_loading:
                progress = loading.get_widget("1")
                progress.set_value(progress.get_value() + 1)
                if progress.get_value() == 100:
                    pygame.time.set_timer(update_loading, 0)
            if event.type == pygame.QUIT:
                exit()
    
        if mainmenu.is_enabled():
            mainmenu.update(events)
            mainmenu.draw(surface)
            if (mainmenu.get_current().get_selected_widget()):
                arrow.draw(surface, mainmenu.get_current().get_selected_widget())
    
        pygame.display.update()

