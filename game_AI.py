import pygame
import random
import os
import sys
from enum import Enum
from collections import namedtuple, deque
import numpy as np

pygame.mixer.init()
pygame.init()

"""Color and background"""
WHITE = (255,255,255)
RED = (255, 0 , 0)
BLACK = (0,0,0)
GROUND = (189, 255, 49)
BORDER_COLOUR = (0,123,48)
SPECIAL_FOOD = (125, 60, 152)
GREEN1  =(0,183, 17) #dark
GREEN2 = (34,221,3) #light

"""window variables"""
WIDTH, HEIGHT = 640, 480
BORDER = 40
SPEED = 20

"""Snake variable"""
SNAKE_BLOCK = 20

"""DIRECTION CLASS"""
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point','x,y')

"""Snake Game Class"""
class SnakeGame:
    
    def __init__(self, w = WIDTH, h = HEIGHT, b = BORDER):
        self.h = h
        self.w = w
        self.b = b
        
        self.h_nb = self.h - 2*b #height with no border
        self.w_nb = self.w - 2*b #width with no border
        
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Snake Game")
        
        self.font = pygame.font.SysFont(None,40)
        self.clock = pygame.time.Clock()
        self.reset()
    
    """reset function to rest the game in the begining """
    def reset(self):
        """init game Direction"""
        self.direction = Direction.RIGHT
        
        """SNAKE"""
        self.snake_head = Point(80, 80)
        
        """Let's define the snake as a list""" 
        self.snake = [self.snake_head, 
                      Point(self.snake_head.x - SNAKE_BLOCK, self.snake_head.y),
                      Point(self.snake_head.x - (2*SNAKE_BLOCK), self.snake_head.y)]
        
        """some game variable"""
        self.score = 0
        self.small_food = None
        self.big_food = None
        self.frame_iteration = 0
        
        #food variables for big food 
        self.small_food_count = 0
        self.big_food_timer = 0
        self.show_big_food = False
        self.big_food_duration = 3000
        self.big_food_score = 2
        self.big_food_size = 20
        
        self.place_food()
        self.frame_iteration = 0

    """place the small food function"""
    def place_small_food(self):
        x = random.randint(self.b//SNAKE_BLOCK , (self.w_nb - SNAKE_BLOCK)//SNAKE_BLOCK)*SNAKE_BLOCK
        y = random.randint(self.b//SNAKE_BLOCK , (self.h_nb - SNAKE_BLOCK)//SNAKE_BLOCK)*SNAKE_BLOCK
        self.small_food = Point(x,y)
        if self.small_food in self.snake:
            self.place_small_food()
        # print(f"Placed small food at: {self.small_food}")
    
    """Place the big food function"""
    def place_big_food(self):
        x = random.randint(self.b//self.big_food_size , (self.w_nb - self.big_food_size)//self.big_food_size)*self.big_food_size
        y = random.randint(self.b//self.big_food_size , (self.h_nb - self.big_food_size)//self.big_food_size)*self.big_food_size
        self.big_food = Point(x,y)
        if self.big_food in self.snake:
            self.place_big_food()
        # print(f"Placed big food at: {self.big_food}")
    
    """Place food which contain the small food and big food logic""" 
    def place_food(self):
        self.small_food_count += 1   
        if self.small_food_count % 5 == 0:
            self.big_food_timer = pygame.time.get_ticks()
            self.show_big_food = True
            self.place_big_food()
        else:
            self.place_small_food()
    
    def count(self):
        return self.small_food_count
        
    def play_step(self, action):
        self.frame_iteration +=1
        
        '''1. Controls'''
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        """#2. Move the snkae """
        
        self.move(action)
        self.snake.insert(0, self.snake_head)
        
        """#3. check the game over condition""" 
        reward = 0
        game_over = False
        if self.is_collision():
            game_over = True
            reward = -20
            return reward, game_over, self.score
        
        """#4. place the food """
        
        if self.snake_head.x < self.small_food.x +SNAKE_BLOCK and \
            self.snake_head.x + SNAKE_BLOCK > self.small_food.x and \
            self.snake_head.y< self.small_food.y +SNAKE_BLOCK and \
            self.snake_head.y + SNAKE_BLOCK > self.small_food.y:
                pygame.mixer.music.load(r"resource\normal_point_collect.mp3")
                pygame.mixer.music.play()
                self.score += 1
                reward = 10
                self.place_food()
                
        elif self.show_big_food and\
            self.snake_head.x < self.big_food.x +SNAKE_BLOCK and \
            self.snake_head.x + SNAKE_BLOCK > self.big_food.x and \
            self.snake_head.y< self.big_food.y +SNAKE_BLOCK and \
            self.snake_head.y + SNAKE_BLOCK > self.big_food.y:
                pygame.mixer.music.load(r"resource\bonus_point.mp3")
                pygame.mixer.music.play()
                self.score += self.big_food_score
                reward = 15
                self.show_big_food = False
                self.place_food()
        else:
            self.snake.pop()
        
        """#5. Update UI and game and clock""" 
        self.update_ui()
        self.clock.tick(SPEED)
        
        if self.show_big_food and (pygame.time.get_ticks() - self.big_food_timer >= self.big_food_duration):
            self.show_big_food = False
        
        """#6. return game over and score """
        return reward, game_over, self.score         
            
    def is_collision(self, pt=None):
        if pt is None:
            pt = self.snake_head
        if pt.x >= (self.w -self.b)  or pt.x <= 20\
            or pt.y >= (self.h - self.b) or pt.y <= 20:
                 
            # print(f"Collision with boundary at: {pt}")
            # print(self.b, self.w_nb,self.h_nb)
            return True
        if pt in self.snake[1:]:
            
            # print(f"Collision with self at: {pt}")
            return True
        
        return False
    
    """Uddate the ui and window 
    iit contain the snake color , small food and big food color window color """
    def update_ui(self):
        self.display.fill(BORDER_COLOUR)
        pygame.draw.rect(self.display, GROUND, [self.b, self.b, self.w_nb, self.h_nb])
        
        for pt in self.snake:
            pygame.draw.rect(self.display, GREEN1, pygame.Rect(pt.x, pt.y, SNAKE_BLOCK, SNAKE_BLOCK))
            pygame.draw.rect(self.display, GREEN2 , pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        if not self.show_big_food:
            pygame.draw.rect(self.display, RED, pygame.Rect(self.small_food.x, self.small_food.y, SNAKE_BLOCK, SNAKE_BLOCK))
        if self.show_big_food:
            pygame.draw.rect(self.display, SPECIAL_FOOD , pygame.Rect(self.big_food.x, self.big_food.y, self.big_food_size, self.big_food_size))
            remaining_time = max(0, self.big_food_duration - (pygame.time.get_ticks() - self.big_food_timer))
            remaining_time_text = self.font.render("special Food: " + str(int(remaining_time / 1000)) + "s", True, WHITE)
            self.display.blit(remaining_time_text, [self.w - 300, 8])
        
        score_text = self.font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(score_text, [8, 8])
        
        pygame.display.flip()
    
    """ move funtion for direction"""
    def move(self, action):
        # [straight, right, left]

        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_direction = clock_wise[idx] # no change
        elif np.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4
            new_direction = clock_wise[next_idx] # right turn r -> d -> l -> u
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_direction = clock_wise[next_idx] # left turn r -> u -> l -> d

        self.direction = new_direction
        
        x = self.snake_head.x
        y = self.snake_head.y
        
        if self.direction == Direction.RIGHT:
            x += SNAKE_BLOCK 
        elif self.direction == Direction.LEFT:
            x -= SNAKE_BLOCK 
        elif self.direction == Direction.DOWN:
            y += SNAKE_BLOCK 
        elif self.direction == Direction.UP:
            y -= SNAKE_BLOCK   
            
        self.snake_head = Point(x, y)
        # print(f"Moved to: {self.snake_head}")

    # def draw(self, screen):
    #     self.update_ui()
    #     screen.blit(self.display, (53, 78))
