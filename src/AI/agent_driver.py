import torch
import os
from src.AI.game import SnakeGame
from src.AI.control_agent import ControlAgent 
import sys
class AgentDriver:
    def __init__(self):
        #Load Previous Model(state, checkpoint, optimizer, games played, record)
        if os.path.exists('src/AI/model/model.pth'):
            self.agent = ControlAgent()
            checkpoint = torch.load('src/AI/model/model.pth')
            self.agent.model.load_state_dict(checkpoint['model_state_dict'])
            self.agent.trainer.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            self.agent.n_games = checkpoint['n_games']
            self.record = checkpoint['Record']
            self.agent.model.eval()
        else:
            print('No Valid Agent Trained')
            sys.exit()
        
    def run(self):
        #Initiliaze agent and enviroment
        agent = self.agent 
        game = SnakeGame()
        while True:
            # get old state
            state_old = agent.get_state(game)
            # get move
            final_move = agent.get_action(state_old)

            # perform move and get new state
            reward, done, score = game.play_step(final_move)
            state_new = agent.get_state(game)

            # train short memory
            agent.train_short_memory(
                state_old, final_move, reward, state_new, done)
            agent.remember(state_old, final_move, reward, state_new, done)
            if done:
                print(f'Score: {score}')
                return
            