from math import log, exp, pow, sqrt

import numpy as np
import pandas as pd
from scipy.stats import norm

from utils import *


def call_black_scholes_merton(*args):
    S, K, r, volatility, T = args[0]

    d1 = (log(S / K) + (r + pow(volatility, 2) / 2) * T) / (volatility * sqrt(T))
    d2 = d1 - volatility * sqrt(T)

    Nd1 = norm.cdf(d1)
    Nd2 = norm.cdf(d2)

    Nd1_ = norm.pdf(d1)

    c_greeks = {'price': S * Nd1 - K * exp(-r * T) * Nd2,
                'delta': Nd1,
                'theta': - (S * Nd1_ * volatility) / (2 * sqrt(T)) - r * K * exp(-r * T) * Nd2,
                'gamma': Nd1_ / (S * volatility * sqrt(T)),
                'vega': S * sqrt(T) * Nd1_,
                'rho': K * T * exp(-r * T) * Nd2
                }

    return c_greeks


def put_black_scholes_merton(*args):
    S, K, r, volatility, T = args[0]

    d1 = (log(S / K) + (r + pow(volatility, 2) / 2) * T) / (volatility * sqrt(T))
    d2 = d1 - volatility * sqrt(T)

    Nd1 = norm.cdf(-d1)
    Nd2 = norm.cdf(-d2)

    Nd1_ = norm.pdf(d1)

    c_greeks = {'price': K * exp(-r * T) * Nd2 - S * Nd1,
                'delta': -Nd1,
                'theta': - (S * Nd1_ * volatility) / (2 * sqrt(T)) + r * K * exp(-r * T) * Nd2,
                'gamma': Nd1_ / (S * volatility * sqrt(T)),
                'vega': S * sqrt(T) * Nd1_,
                'rho': -K * T * exp(-r * T) * Nd2
                }

    return c_greeks


def sensitivity_2D(type, on, S, K, r, volatility, T, n2D=500):
    variables_lookup = ['Underlying price (S)', 'Strike (K)', 'Risk-free (r)', 'Volatility (σ)', 'Maturity (T)']
    variables = [S, K, r, volatility, T]

    sens_variable = None
    for i, variable in enumerate(variables):
        if isinstance(variable, tuple):
            sens_variable = [i, variable, variables_lookup[i]]

    Y = []
    i = sens_variable[0]
    X = np.linspace(sens_variable[1][0], sens_variable[1][1], n2D)
    for x in X:
        variables[i] = x
        if type == 'call':
            c_greeks = call_black_scholes_merton(variables)
        else:
            c_greeks = put_black_scholes_merton(variables)
        Y.append(c_greeks[on])
    return pd.DataFrame(Y, index=X), sens_variable[2]


def sensitivity_3D(type, on, S, K, r, volatility, T, n3D=50):
    variables_lookup = ['Underlying price (S)', 'Strike (K)', 'Risk-free (r)', 'Volatility (σ)', 'Maturity (T)']
    variables = [S, K, r, volatility, T]

    sens_variables = []
    for i, variable in enumerate(variables):
        if isinstance(variable, tuple):
            sens_variables.append([i, variable, variables_lookup[i]])

    sensitivity_matrix = []
    i = sens_variables[0][0]
    j = sens_variables[1][0]
    X = np.linspace(sens_variables[0][1][0], sens_variables[0][1][1], n3D)
    Y = np.linspace(sens_variables[1][1][0], sens_variables[1][1][1], n3D)
    for x in X:
        variables[i] = x
        row = []
        for y in Y:
            variables[j] = y
            if type == 'call':
                c_greeks = call_black_scholes_merton(variables)
            else:
                c_greeks = put_black_scholes_merton(variables)
            row.append(c_greeks[on])
        sensitivity_matrix.append(row)
    output = pd.DataFrame(sensitivity_matrix, index=X, columns=Y)
    return output, sens_variables[0][2], sens_variables[1][2]
