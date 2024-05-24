import torch
# import tensorflow as tf 
import random
import numpy as np
from collections import deque
from game_AI import SnakeGame, Direction, Point,SNAKE_BLOCK
from model_3 import Linear_QNet, QTrainer
# from model_4 import Linear_QNet , QTrainer
from model_plot import plot

MAX_MEMORY = 1000_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.epsilon = 1.0
        self.min_epsilon = 0.01
        self.epsilon_decay = 0.9
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11,1024, 3)
        self.trainer = QTrainer(model=self.model, lr=LR, gamma=self.gamma)
    def update_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)
        
    def get_state(self, game):
        head = game.snake[0]
        body = game.snake[1:-1]
        tail = game.snake[-1] if len(game.snake) > 1 else head
    
        point_l = Point(head.x - SNAKE_BLOCK, head.y)
        point_r = Point(head.x + SNAKE_BLOCK, head.y)
        point_u = Point(head.x, head.y - SNAKE_BLOCK)
        point_d = Point(head.x, head.y + SNAKE_BLOCK)
        
        direction_l = game.direction == Direction.LEFT
        direction_r = game.direction == Direction.RIGHT
        direction_u = game.direction == Direction.UP
        direction_d = game.direction == Direction.DOWN

        big_food = game.big_food
        small_food = game.small_food
        
        self.small_food_count = game.count()
        if self.small_food_count %5 ==0:
            food = game.big_food
        else :
            food = game.small_food
            
        # if big_food == None:
        #     big_food = Point(0,0)
        # if small_food == None:
        #     small_food = Point(0,0)

        state = [
            # Danger straight
            (direction_r and game.is_collision(point_r)) or 
            (direction_l and game.is_collision(point_l)) or 
            (direction_u and game.is_collision(point_u)) or 
            (direction_d and game.is_collision(point_d)),

            # Danger right
            (direction_u and game.is_collision(point_r)) or 
            (direction_d and game.is_collision(point_l)) or 
            (direction_l and game.is_collision(point_u)) or 
            (direction_r and game.is_collision(point_d)),

            # Danger left
            (direction_d and game.is_collision(point_r)) or 
            (direction_u and game.is_collision(point_l)) or 
            (direction_r and game.is_collision(point_u)) or 
            (direction_l and game.is_collision(point_d)),
            
            # Move direction
            direction_l,
            direction_r,
            direction_u,
            direction_d,
            
            # Food location 
            # small_food.x < game.snake_head.x or big_food.x < game.snake_head.x,  #small food left
            # small_food.x > game.snake_head.x or big_food.x > game.snake_head.x,  #small food right
            # small_food.y < game.snake_head.y or big_food.y < game.snake_head.y,  #small food up
            # small_food.y > game.snake_head.y or big_food.y > game.snake_head.y,  #small food down
            
            food.x < game.snake_head.x,  #big  food left
            food.x > game.snake_head.x,  #big  food right
            food.y < game.snake_head.y,  #big  food up
            food.y > game.snake_head.y,  #big  food down
            
            
            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 120 - self.n_games
        final_move = [0,0,0]
        if random.randint(0,320) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move
    
    # def get_action(self, state):
    #     # random moves: tradeoff exploration / exploitation
    #     self.epsilon = 80 - self.n_games
    #     final_move = [0, 0, 0]
    #     if random.randint(0, 200) < self.epsilon:
    #         move = random.randint(0, 2)
    #         final_move[move] = 1
    #     else:
    #         state0 = np.array(state, dtype=np.float32).reshape(1, -1)
    #         state0 = tf.convert_to_tensor(state0)
    #         prediction = self.model(state0)
    #         move = tf.argmax(prediction[0]).numpy()  # Ensure move is a scalar integer
    #         final_move[move] = 1

    #     return final_move



def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
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
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)
        # agent.update_epsilon()  # Update epsilon after each episode or time step
        
        if done:
            # train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()
                print("--------------\n||  update  ||\n--------------")
            print('Game', agent.n_games, 'Score', score, 'Record:', record)
            print(40*"-")
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)


if __name__ == '__main__':
    train()