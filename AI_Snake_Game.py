import torch 
from model_3 import Linear_QNet
from game_AI import SnakeGame, Direction, Point, SNAKE_BLOCK
from agent import Agent
class AI_PLAY:
    def __init__(self, game, model, agent,device):
        self.model = model
        self.agent = agent
        self.game = game
        self.device = device
    def play_with_model(self):
        # game = SnakeGame()
        # agent = Agent()
        
        while True:
            """Get the current state of the game"""
            self.state = self.agent.get_state(game=self.game)
            
            # print("state: ",state)
            """Convert the state to a tensor and move it to the device (CPU or GPU)"""
            self.state_tensor = torch.tensor(self.state, dtype=torch.float).unsqueeze(0).to(self.device)
            # print("State tensor : ",state_tensor)
            
            """"Use the model to predict the next action"""
            with torch.no_grad():
                self.action_probs = self.model(self.state_tensor)
                # print("action probability : ",action_probs)
                
                self.action = torch.argmax(self.action_probs).item()
                # print("action : ",action)
            
            """Map the action index to a valid game action"""
            if self.action == 0:
                self.game_action = [1, 0, 0]  # Move straight
            elif self.action == 1:
                self.game_action = [0, 1, 0]  # Turn right
            else:
                self.game_action = [0, 0, 1]  # Turn left

            """"Play the game step with the selected action"""
            reward, done, score = self.game.play_step(self.game_action)
            # print(40*"-")
            
            """If the game is over, break out of the loop"""
            if done:
                break

        print("\n----- Game over ------\n|| Final score: ",score," ||")

"""Load the saved model"""
def ai_snake_game():
    input_size = 11
    hidden_size = 512
    output_size = 3
    model = Linear_QNet(input_size, hidden_size, output_size)
    model.load_state_dict(torch.load("model_2\model_2.pth"))

    """Set the device (CPU or GPU) for model inference"""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    game = SnakeGame()
    agent = Agent()
    ai_play = AI_PLAY(game=game,model=model,agent=agent,device=device)
    
    return ai_play.play_with_model()

if __name__ == '__main__':
    ai_snake_game()   

