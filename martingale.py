import numpy as np
import numba
import matplotlib.pyplot as plt


@numba.jit(nopython=True,fastmath=True)
def martingale_strategy(bankroll, bet_size, win_probability):
    """
    Simulate a Martingale betting strategy.

    Parameters:
    - bankroll: Initial bankroll.
    - bet_size: Initial bet size.
    - win_probability: Probability of winning a bet.
    
    Returns:
    - A list of bankroll values over time.
    """
    bankroll_values = [bankroll]
    current_bet_size = bet_size
    current_bet_size_values = [bet_size]
    while bankroll > 0:
        if np.random.rand() < win_probability:
            bankroll += current_bet_size
            current_bet_size = bet_size
        else:
            bankroll -= current_bet_size
            current_bet_size *= 2
        
        bankroll_values.append(bankroll)
        current_bet_size_values.append(current_bet_size)
    return bankroll_values, current_bet_size_values

@numba.jit(nopython=True,fastmath=True)
def martingale_with_stop(bet_size, win_probability):
    """
    Simulate a Martingale betting strategy.

    Parameters:  
    - bet_size: Initial bet size.
    - win_probability: Probability of winning a bet.
    
  
    """
  
    current_bet_size = bet_size   
    success=False
    duration=0
    while not success:
        duration+=1
        if np.random.rand() < win_probability:                 
            success=True                
        else:
            current_bet_size=2*current_bet_size
      
       
    return duration


def main():
    bankroll = 1000
    bet_size = 1
    win_probability = 0.5
    bankroll_values, current_bet_size_values,duration = martingale_strategy(bankroll, bet_size, win_probability)
    #print("Bankroll values over time:", bankroll_values)
    plt.plot(bankroll_values)
    plt.xlabel("Time")
    plt.ylabel("Bankroll")
    plt.title("Martingale Strategy Simulation")
    plt.plot(current_bet_size_values)
    plt.xlabel("Time")
    plt.ylabel("Current Bet Size")
    plt.title("Martingale Strategy Simulation")
    plt.legend(["Bankroll", "Current Bet Size"])
    plt.grid(True)
    plt.show()

@numba.jit(nopython=True,fastmath=True)
def main_with_stop():  
    bet_size = 1
    win_probability = 0.5
    duration = martingale_with_stop(bet_size, win_probability)
    return duration

@numba.jit(nopython=True,fastmath=True)
def stat_with_stop():
    N=10000       
    bet_size = 1
    win_probability = 0.5
    total_duration=0
    for i in range(N):        
        duration = martingale_with_stop(bet_size, win_probability)
        total_duration+=duration    

    return total_duration/N
       
   
if __name__ == "__main__":
    mean_duration = stat_with_stop()
    print("Mean Duration:", mean_duration)