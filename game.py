import pygame
import random
import os
import time 
import sys
from enum import Enum
from collections import namedtuple
import numpy as np 

pygame.mixer.init()

pygame.init()

#Colours and background
WHITE = (255,255,255)
RED = (255, 0 , 0)
BLACK = (0,0,0)
YELLOW = (255, 255, 0)
BROWN = (186, 74, 0)
GREEN = (46, 204, 113)
DEEP_GREEN = (11, 83, 69)
BLUE = (46, 134, 193)
LIGHT_BLUE = (174, 214, 241)
height = 480
width = 680
border= 40

BLUE1  =(0,0,255)
BLUE2 = (0,100,255)
clock = pygame.time.Clock()
#create window
pygame.display.set_caption("snake game")

font = pygame.font.SysFont(None,50)

#shake variables 
snake_x = 60
snake_y = 60
snake_size = 20

#Direction actions 
class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point','x,y')

def resource_path(relative_path):
    """Get absolute path to resourse, works for dev and for pyinstaller"""
    try:
        # pyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path,relative_path)

class SnakeGame:
    def __init__(self, w = width, h = height, b = border):
        self.h = h
        self.w = w
        self.b = b
        # self.snake_x = snake_x
        # self.snake_y = snake_y
        
        #init display settings 
        self.display = pygame.display.set_mode((self.w,self.h))
        pygame.display.set_caption("snake game")
        self.clock = pygame.time.Clock()
        self.reset()
        
        
        
    def resource_path(relative_path):
    #"""Get absolute path to resourse, works for dev and for pyinstaller"""
        try:
        # pyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
            return os.path.join(base_path,relative_path)
    
    def reset(self):
        #init game Directions
        self.Direction = Direction.RIGHT
        
            #SNAKE 
        self.snake_head = Point(snake_x, snake_y) #point the snake head
            #this is the list which define the snake 
        self.snake = [self.snake_head,
                        Point(self.snake_head.x-snake_size, self.snake_head.y ),
                        Point(self.snake_head.x-(2*snake_size), self.snake_head.y)] 
        
        self.score = 0
        self.food = None 
        self.big_food = None
        self.frame_iteration = 0 
        self.velocity = 2
        self.velocity_x = 0
        self.velocity_y = 0
        
        # food variables for big food 
        self.small_food_count  = 0
        self.big_food_timer = 0
        self.show_big_food = False
        self.big_food_duration= 4000
        self.big_food_score = 5
        self.big_food_size = 30
        
        self._place_food()
        
        self.frame_iteration = 0 
    #PLACE THE FOOD IN THE PLAYGROUND
        
    def _place_food(self): 
        x = random.randint(2*self.b+30,self.w-(2*self.b)-30)
        y = random.randint(2*self.b+30,self.h-(2*self.b)-30)
        self.food = Point(x,y)
        self.small_food_count += 1 #count the small foods 
        
        if self.small_food_count%5 ==0: #if 5 small foods are applied than the big food comes
            self.show_big_food = True
            self.big_food_timer = pygame.time.get_ticks() #start the timer for big food
            #Generate big food
            self.big_food = Point(random.randint(2 * self.b + 30, self.w - (2 * self.b) - 30),
                                  random.randint(2 * self.b + 30, self.h - (2 * self.b) - 30))
        
        if self.food in self.snake:
            self._place_food()
        if self.big_food in self.snake:
            self._place_food()
            
    def play_step(self):
        global snake_x, snake_y
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                    
         #1.  controls 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.Direction = Direction.LEFT
                    velocity_x = self.velocity
                    velocity_y = 0  
                if event.key == pygame.K_d:
                    self.Direction = Direction.RIGHT
                    velocity_x = -self.velocity
                    velocity_y = 0
                if event.key == pygame.K_w:
                    self.Direction = Direction.UP
                    velocity_y = -self.velocity
                    velocity_x = 0
                if event.key == pygame.K_s:
                    self.Direction = Direction.DOWN
                    velocity_y = self.velocity
                    velocity_x = 0
                # snake_x = snake_x+velocity_x
                # snake_y = snake_y+velocity_y
                
                # self.snake_head = Point(snake_x, snake_y) #update the snake head
        
        #2.move the snake 
        self._move(self.Direction) #update the head
        self.snake.insert(0,self.snake_head)
        print("Snake head Positionn : ",self.snake_head)
        print("Food Position :",self.food)
        print("Big Food Position :",self.big_food)
        print(30*"-")
        
        #3. check if game over 
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
        
            
        #4. place the food 
        #(snake ta food gulo khabe tar program )
        if self.show_big_food:
            current_time = pygame.time.get_ticks()
            if current_time - self.big_food_timer>= self.big_food_duration:
                self.show_big_food = False
                
        #where there is no any big food
        if self.show_big_food == False:  
            if self.snake_head.x < self.food.x + snake_size and \
                self.snake_head.x + snake_size > self.food.x and \
                self.snake_head.y < self.food.y + snake_size and \
                self.snake_head.y + snake_size > self.food.y:
            
                    self.score += 1
                    pygame.mixer.music.load(resource_path(r"C:\Users\anike\OneDrive\Desktop\pygame\resource\normal_point_collect.mp3"))
                    pygame.mixer.music.play()
                    
                    self._place_food()
            else :
                self.snake.pop()
         
        #where there is big food    
        if self.show_big_food == True:
            # print("Big Food Position :",self.big_food)
            # print(30*"_")
            pt = self.snake_head
            
            if pt.x < self.food.x + snake_size and \
                pt.x + snake_size > self.food.x and \
                pt.y < self.food.y + snake_size and \
                pt.y + snake_size > self.food.y:
            
                    self.score += 1
                    #play music after eat the small food 
                    pygame.mixer.music.load(resource_path(r"C:\Users\anike\OneDrive\Desktop\pygame\resource\normal_point_collect.mp3"))
                    pygame.mixer.music.play()
                    
                    self._place_food()
                    
            if pt.x < self.big_food.x + self.big_food_size and \
            pt.x + snake_size > self.big_food.x and \
            pt.y < self.big_food.y + self.big_food_size and \
            pt.y + snake_size > self.big_food.y:
                # Big food eaten, increase score and reset big food variables...
                self.score += self.big_food_score
                #play music after eat big food 
                pygame.mixer.music.load(resource_path(r"C:\Users\anike\OneDrive\Desktop\pygame\resource\bonus_point.mp3"))
                pygame.mixer.music.play()
                self.show_big_food = False
                self.big_food = None
                     
                self._place_food()
            else:
                self.snake.pop()   
            
        #5. update ui and clock
        self._update_ui()
        self.clock.tick(40)
        
        #6. return game over and score 
        return game_over, self.score
    
    def _is_collision(self, pt = None):
       #hit boundary 
       w = self.w - self.b
       h = self.h - self.b
       b = self.b
       
       if pt is None:
           pt =  self.snake_head
       if pt.x>w - snake_size  or pt.x <b or pt.y >h - snake_size or pt.y<b:
           return True
       
       #hit itself 
       if self.snake_head in self.snake[1:]:
           return True
       
       return False 
    
    def _update_ui(self):
        b = self.b
        h = self.h
        w = self.w
        self.display.fill(GREEN)
        pygame.draw.rect(self.display,YELLOW,[b, b, w - 2*b, h-2*b ])
        
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, snake_size, snake_size))
            pygame.draw.rect(self.display, BLUE2 , pygame.Rect(pt.x+4, pt.y+4,12,12))
            
            if self.show_big_food:
                
                # Display the big food on the screen...
                pygame.draw.rect(self.display, DEEP_GREEN, pygame.Rect(self.big_food.x, self.big_food.y, self.big_food_size, self.big_food_size))
                
                # Calculate the remaining time for the big food...
                remaining_time = max(0, self.big_food_duration - (pygame.time.get_ticks() - self.big_food_timer))
                
                # Display the remaining time on the top right side of the score...
                remaining_time_text = font.render("Big Food: " + str(int(remaining_time / 1000)) + "s", True, BLACK)
                self.display.blit(remaining_time_text, [width - 260, 10])
            
        pygame.draw.rect(self.display, RED , pygame.Rect(self.food.x, self.food.y, snake_size, snake_size))
            
        text = font.render("Score: "+str(self.score),True, BLACK)
        self.display.blit(text, [10,10])
        pygame.display.flip()        
    
    def _move(self, direction):
        x = self.snake_head.x
        y = self.snake_head.y
        print(direction)
        if direction == Direction.RIGHT:
            x += snake_size
        elif direction == Direction.LEFT:
            x -= snake_size
        elif direction == Direction.DOWN:
            y += snake_size
        elif direction == Direction.UP:
            y -= snake_size
            
        self.snake_head = Point(x,y)
            
if __name__ == '__main__':
    game = SnakeGame()
    
    # game._place_food()
    #game loop
    while True:
        pygame.time.delay(75)
        game_over , score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score ',score)
          
    pygame.quit()
        
             

