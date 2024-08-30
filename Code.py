# Import essential libraries
import random  # For generating random decisions
import numpy as np  # For numerical operations
import seaborn as sns  # For plotting distributions
import matplotlib.pyplot as plt  # For creating plots

# Strategy Function
def strategy(type, opDecision, flag=0, lastResults="CC"):
    # GRIM Strategy: Cooperate unless the opponent defects, then defect forever
    if type == "grim":
        if opDecision == "D" or flag == 1:
            return "D", 1  # Defect and set flag to 1
        elif opDecision == "C":
            return "C", 0  # Cooperate and reset flag
    
    # Random Strategy: Randomly choose to Cooperate or Defect
    elif type == "random":
        return random.choice(["C", "D"]), flag
    
    # Always Cooperate Strategy
    elif type == "allC":
        return "C", 0
    
    # Always Defect Strategy
    elif type == "allD":
        return "D", 0
    
    # Tit-for-tat Strategy: Mimic opponent's last decision
    elif type == 'tft':
        if flag == 0:
            return "C", 1  # Start by cooperating
        else:
            return opDecision, flag  # Then mimic opponent
    
    # Suspicious Tit-for-tat Strategy: Start by defecting, then mimic opponent
    elif type == 'stft':
        if flag == 0:
            return "D", 1  # Start by defecting
        else:
            return opDecision, flag  # Then mimic opponent
    
    # Probability p Cooperator Strategy: Cooperate with a probability p
    elif type == 'prob':
        p = 0.25  # Probability of cooperating
        return random.choices(["C", "D"], weights=[p, 1-p])[0], 0
    
    # Reactive Strategy R(y, p, q): Respond based on a probability depending on previous moves
    elif type == 'reactive': 
        y = 0.5  # Initial probability of cooperating
        p = 0.25  # Probability of cooperating after cooperation
        q = 1 - p  # Probability of cooperating after defection
        if flag == 0:
            return random.choices(["C", "D"], weights=[y, 1-y])[0], 2  # Start with y
        elif flag == 2:
            return random.choices(["C", "D"], weights=[p, q])[0], 2  # Follow with p or q
    
    # ZD Strategy: Zero-determinant strategy based on the history of moves
    elif type == 'zd':
        if lastResults == "CC":
            return random.choices(["C", "D"], weights=[3/4, 1-3/4])[0], 0
        elif lastResults == "CD": 
            return random.choices(["C", "D"], weights=[1/4, 1-1/4])[0], 0
        elif lastResults == "DC":  
            return random.choices(["C", "D"], weights=[1/2, 1-1/2])[0], 0
        elif lastResults == "DD": 
            return random.choices(["C", "D"], weights=[1/4, 1-1/4])[0], 0
        else:
            return random.choices(["C", "D"], weights=[3/4, 1-3/4])[0], 0

# Scoring Function: Assign scores based on the combination of decisions
def score(decision1, decision2):
    if decision1 == "C" and decision2 == "C":
        return np.array([2, 2])  # Mutual cooperation
    elif decision1 == "C" and decision2 == "D":
        return np.array([0, 3])  # Opponent defects, player cooperates
    elif decision1 == "D" and decision2 == "C":
        return np.array([3, 0])  # Player defects, opponent cooperates
    elif decision1 == "D" and decision2 == "D":
        return np.array([1, 1])  # Mutual defection

# Simulation Game: Simulate a game between two strategies over N rounds
def simulateGame(N, player1strategy, player2strategy, flag2=0):
    player1, flag1 = strategy(player1strategy, "C")  # Initialize player 1's strategy
    player2, flag2 = strategy(player2strategy, player1, flag2)  # Initialize player 2's strategy
    Score = np.array([0, 0])  # Initialize scores
    for i in range(N):
        Score += score(player1, player2)  # Accumulate scores
        player1, flag1 = strategy(player1strategy, player2, flag1, player1+player2)  # Update player 1's decision
        player2, flag2 = strategy(player2strategy, player1, flag2, player1+player2)  # Update player 2's decision
    return Score/N  # Return average score over N rounds

# Replication of Game: Repeat the simulation M times to analyze results
def replicateGame(M, N, player1strategy, player2strategy):
    Scores = []
    for i in range(M):
        Scores.append(simulateGame(N, player1strategy, player2strategy))  # Simulate M games
    return np.array(Scores)  # Return array of scores

# Number of Replications
M = 1000  # Number of games to replicate

# Number of Rounds per Game
N = 10  # Number of rounds in each game

# Simulate and Plot Results
player1strategy = "grim"  # Player 1 uses the GRIM strategy
for player2strategy in ["random", 'prob', 'reactive', 'zd']:
    Scores = replicateGame(M, N, player1strategy, player2strategy)  # Replicate the game
    plt.subplot(2, 1, 1)  # Create first subplot
    sns.histplot(Scores, alpha=0.5, stat='density')  # Plot histogram of scores
    plt.legend([player2strategy, player1strategy])  # Add legend
    plt.xlabel('Average Score')  # Label x-axis
    plt.title(player1strategy + ' versus ' + player2strategy)  # Add title
    
    plt.subplot(2, 1, 2)  # Create second subplot
    ax = sns.violinplot(Scores, orient='h')  # Plot violin plot of scores
    ax.set_yticks([0, 1])  # Set y-ticks
    ax.set_yticklabels([player1strategy, player2strategy])  # Label y-ticks
    ax.set_xlabel('Average Score')  # Label x-axis
    
    # Uncomment the following block to get ECDF (Empirical Cumulative Distribution Function)
    # ax = sns.ecdfplot(Scores)
    # ax.set_title('CDF of ' + player1strategy + ' and ' + player2strategy)
    # ax.legend([player2strategy, player1strategy])
    # ax.set_xlabel('Average Score')
    
    plt.show()  # Show the plot
