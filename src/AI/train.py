import torch
import os
import numpy as np
from src.AI.game import SnakeGame, Direction, Point
from src.AI.display import plot
from src.AI.control_agent import ControlAgent 


class Train:
    def __init__(self):
        self.record = 0
        self.agent = ControlAgent()
        if os.path.exists('src/AI/model/model.pth'):
            checkpoint = torch.load('src/AI/model/model.pth')
            self.agent.model.load_state_dict(checkpoint['model_state_dict'])
            self.agent.trainer.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            self.agent.n_games = checkpoint['n_games']
            self.record = checkpoint['Record']
            self.agent.model.eval()
         
    def run(self, num_games=10):
        plot_scores = []
        plot_mean_scores = []
        total_score = 0
        session_games = 0
        record = self.record 
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

            # remember
            agent.remember(state_old, final_move, reward, state_new, done)
            if done:
                # train long memory, plot result
                game.reset()
                agent.n_games += 1
                session_games +=1
                agent.train_long_memory()

                if score > record:
                    record = score
                    self.save(agent, record)
                   

                print('Game', agent.n_games, 'Score', score, 'Record:', record)
                plot_scores.append(score)
                total_score += score
                mean_score = total_score / agent.n_games
                plot_mean_scores.append(mean_score)
                plot(plot_scores, plot_mean_scores)
                if session_games==num_games:
                    self.save(agent,record)
                    return 
                
    def save(self, agent,record):
        folder = 'src/AI/model'
        infile = 'model.pth'
        if not os.path.exists(folder):
            os.makedirs(folder)
        file_name = os.path.join(folder, infile)
        torch.save({'model_state_dict': agent.model.state_dict(),
                    'optimizer_state_dict': agent.trainer.optimizer.state_dict(),
                    'n_games':agent.n_games,
                    'Record':record}, file_name)
