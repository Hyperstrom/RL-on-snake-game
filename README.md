# **🐍 Traditional Snake Game with a Twist and AI Integration 🤖**

This repository features a traditional snake game implemented using the Pygame library, with an exciting twist: after consuming 4 food items, a special food appears for 3 seconds, offering double points. 🎯

## **📸 Screenshots of the game:**

![image](https://github.com/Hyperstrom/RL-on-snake-game-/assets/112319058/83ac989f-65c2-4da1-8310-6e84b0294466)

---

# **🧠 Applying Reinforcement Learning to the Snake Game**

In addition to the traditional gameplay, I have integrated reinforcement learning into the game. Using a feedforward neural network built with PyTorch, I trained an AI agent to play the game. The model takes 11 game states as input and makes decisions to move straight, left, or right based on these states. 🕹️

Apologies for misunderstanding. Let's correct that:

## **💻 Model Details**

**File:** `model_3.py`

- **Input Nodes:** 11
- **Hidden Nodes:** 512
- **Output Nodes:** 3
- **Optimizer:** Adam
- **Loss Function:** Mean Squared Error (MSE)

### Reinforcement Learning Approach

The AI agent employs the Bellman equation to update its Q-values during training. The equation used is:

$$ Q(s, a) = (1 - \alpha) \cdot Q(s, a) + \alpha \cdot (r + \gamma \cdot \max Q(s', a')) $$

Where:
- Q(s, a) is the Q-value for a given state-action pair.
- α is the learning rate.
- r is the immediate reward received after taking action a in state s.
- γ is the discount factor.
- max Q(s', a') is the maximum Q-value for the next state s'.
This equation guides the snake's learning process, enabling it to optimize expected future rewards effectively.

## **🔍 Training Details:**
---

- The model was trained over 950+ episodes. 📈
- The AI agent learns and improves its performance through experience. 🧑‍🏫
- Below is the score plot with episodes:

![Figure_2](https://github.com/Hyperstrom/RL-on-snake-game-/assets/112319058/322fac1f-495f-443d-a60b-49ea86b8e547)

you can see that in that training process the highesr score is 90 and avarage score is arround 30

Feel free to explore the code, experiment with the AI, and contribute to the project! 🚀

**🔗 Links:**

- [Pygame Documentation](https://www.pygame.org/docs/)
- [PyTorch Documentation](https://pytorch.org/docs/)

Contributions are welcome! Check out the issues for ways to get involved. 💡



## **📺Demo Video**

Check out this demo video to see how the AI snake players perform.

https://github.com/Hyperstrom/RL-on-snake-game-/assets/112319058/4a8c7e6a-adb4-4b50-b8c7-3eb539223268

---

## **How to Run the Game:**

1. Clone the repository: `git clone https://github.com/Hyperstrom/RL-on-snake-game`
2. Navigate to the project directory: `cd RL-on-snake-game-`
3. Install the required dependencies: `pip install -r requirements.txt`
4. Run the game with AI: `python AI_Snake_Game.py`
5. Play the game using keyboard( W, A, S, D) : `python game_Human.py`

**How to Train the AI Agent:**

1. Follow the steps above to clone the repository and install dependencies.
2. Run the training script: `python agent.py`
3. Monitor the training progress and performance through the generated plots.

Enjoy playing and experimenting with the AI-powered snake game! 🐍🎮

## **💡 Contributions**

Feel free to explore the code, experiment with the AI, and contribute to the project! Check out the issues for ways to get involved.
