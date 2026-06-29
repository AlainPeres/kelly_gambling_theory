# -*- coding: utf-8 -*-
"""
Created on Sat Sep 23 13:01:03 2023

@author: Alain
"""

import matplotlib.pyplot as plt
import numba
import numpy as np


@numba.jit(nopython=True, fastmath=True)
def kelly_ratio(p, b):
    # p: probabilité de gain
    # b: ratio gain/perte
    q = 1 - p
    f = p - q / b
    if f < 0:
        f = 0
    if f > 1:
        f = 1
    return f


@numba.jit(nopython=True, fastmath=True)
def step(bet, p, b):
    r = np.random.rand()
    if r < p:
        delta_gain = bet * b
    else:
        delta_gain = -bet
    return delta_gain


@numba.jit(nopython=True, fastmath=True)
def simulate(f, p, b, n):
    capital = np.zeros(n)
    capital[0] = 1
    for i in range(1, n):
        bet = capital[i - 1] * f
        delta_gain = step(bet, p, b)
        capital[i] = capital[i - 1] + delta_gain
    return capital


@numba.jit(nopython=True, fastmath=True)
def final_stats(f, b, p, n, nruns):
    final_capital = np.zeros(nruns)
    for i in range(nruns):
        capital = simulate(f, p, b, n)
        final_capital[i] = capital[-1]
    mean = np.mean(final_capital)
    std = np.std(final_capital)
    return mean, std


@numba.jit(nopython=True, fastmath=True)
def ruin_probability(f, b, p, n, nruns, ruin_threshold):
    final_capital = np.zeros(nruns)
    ruin_count = 0
    for i in range(nruns):
        capital = simulate(f, p, b, n)
        final_capital[i] = capital[-1]
        if final_capital[i] < ruin_threshold:
            ruin_count += 1
    ruin_probability = ruin_count / nruns
    return ruin_probability


def visualize(capital, text=""):
    x = np.arange(len(capital))
    plt.figure()
    plt.title("Simulation" + text)
    plt.xlabel("Temps")
    plt.ylabel("Capital")
    plt.plot(x, capital)
    plt.grid(True)


def visualize_g(p, b):
    g = np.zeros(100)
    f = np.zeros(100)
    for i in range(100):
        f[i] = i / 100
        g[i] = p * np.log(1 + f[i] * b) + (1 - p) * np.log(1 - f[i])

    plt.figure()
    plt.title("g en fonction de f")
    plt.xlabel("f")
    plt.ylabel("g")
    plt.plot(f, g)
    plt.grid(True)


if __name__ == "__main__":
    p = 0.6
    b = 1
    n = 100
    nruns = 10000
    ruin_threshold = 0.1
    f_kelly = kelly_ratio(p, b)
    print("--------------------")
    print("Kelly fraction = ", f_kelly)
    print("--------------------")
    print("")
    capital_kelly = simulate(f_kelly, p, b, n)

    f = min(2.5 * f_kelly, 1)
    capital_other = simulate(f, p, b, n)

    mean_kelly, std_kelly = final_stats(f_kelly, b, p, n, nruns)
    ruin_prob_kelly = ruin_probability(f_kelly, b, p, n, nruns, ruin_threshold)
    print("--------------------")
    print("Kelly: mean final capital = ", mean_kelly, ", std = ", std_kelly)
    print("Kelly: ruin probability = ", ruin_prob_kelly)
    print("--------------------")

    print("")

    mean_other, std_other = final_stats(f, b, p, n, nruns)
    ruin_prob_other = ruin_probability(f, b, p, n, nruns, ruin_threshold)
    print("--------------------")
    print("Other: mean final capital = ", mean_other, ", std = ", std_other)
    print("Other: ruin probability = ", ruin_prob_other)
    print("--------------------")

    visualize(capital_kelly, " - Kelly")
    visualize(capital_other, " - Other")
    visualize_g(p, b)

    try:
        plt.show()
    except KeyboardInterrupt:
        pass
