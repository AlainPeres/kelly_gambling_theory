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
def martingale_with_stop(bankroll, bet_size, win_probability):
    """
    Simulate a Martingale betting strategy. Stop after the first success.

    Parameters:  
    - bet_size: Initial bet size.
    - win_probability: Probability of winning a bet.
    Returns the duration of the betting session until the first success.
  
    """
    current_bankroll = bankroll
    current_bet_size = bet_size
    success=False
    duration=0
    while not success:
        
        duration+=1
        if np.random.rand() < win_probability:  
            current_bankroll += current_bet_size               
            success=True                
        else:
            current_bankroll -= current_bet_size
            current_bet_size=2*current_bet_size 

       
    return duration,current_bankroll,current_bet_size


def main_martigale_strategy():
    bankroll = 1000
    bet_size = 1
    win_probability = 0.5
    bankroll_values, current_bet_size_values = martingale_strategy(bankroll, bet_size, win_probability)
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
def main_martingale_with_stop():  
    bet_size = 1
    win_probability = 0.5
    bankroll = 0
    final_bankroll = 0
    final_bet_size = 0
    duration, final_bankroll, final_bet_size = martingale_with_stop(bankroll, bet_size, win_probability)
    return duration, final_bankroll, final_bet_size

@numba.jit(nopython=True,fastmath=True)
def stat_with_stop():
    N=10000     
    total_duration=0
    total_bankroll=0
    total_bet_size=0
    max_duration=0
    max_bankroll=0
    max_bet_size=0
   
    for i in range(N):        
        duration,final_bankroll,final_bet_size = main_martingale_with_stop()

        if duration>max_duration:
            max_duration=duration
        if final_bankroll>max_bankroll:
            max_bankroll=final_bankroll
        if final_bet_size>max_bet_size:
            max_bet_size=final_bet_size

        total_duration+=duration
        total_bankroll+=final_bankroll
        total_bet_size+=final_bet_size
    return total_duration/N, total_bankroll/N, total_bet_size/N,max_duration, max_bankroll, max_bet_size
       
   
if __name__ == "__main__":
    mean_duration, mean_bankroll, mean_bet_size, max_duration, max_bankroll, max_bet_size = stat_with_stop()
    print("Mean Duration:", mean_duration)
    print("Mean Bankroll:", mean_bankroll)
    print("Mean Bet Size:", mean_bet_size)
    print("Max Duration:", max_duration)
    print("Max Bankroll:", max_bankroll)
    print("Max Bet Size:", max_bet_size)