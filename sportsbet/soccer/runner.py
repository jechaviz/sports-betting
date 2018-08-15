"""
Includes wrapper functions of main function and classes. 
"""

# Author: Georgios Douzas <gdouzas@icloud.com>
# License: BSD 3 clause

from os.path import join
from warnings import filterwarnings
import numpy as np
import pandas as pd
from .configuration import MIN_N_MATCHES, ESTIMATOR, PARAM_GRID, ODDS_THRESHOLD, GENERATE_WEIGHTS
from .data import fetch_raw_data, extract_training_data, extract_odds_dataset
from .optimization import Betting


def fetch_simulation_data(dirpath=None):
    """Download and save training and odds data."""
    spi_data, fd_data = fetch_raw_data()
    training_data = extract_training_data(spi_data, fd_data)
    odds_data = extract_odds_dataset(fd_data)
    if dirpath is not None:
        training_data.to_csv(join(dirpath, 'training_data.csv'), index=False)
        odds_data.to_csv(join(dirpath, 'odds_data.csv'), index=False)
    return training_data, odds_data


def generate_simulation_results(estimator=ESTIMATOR, param_grid=PARAM_GRID, dirpath='data', test_season='17-18', 
                                predicted_result='D', min_matches=MIN_N_MATCHES, odds_threshold=ODDS_THRESHOLD,
                                generate_weights=GENERATE_WEIGHTS, random_state=None):
    """Run betting simulation and generate the results."""
    filterwarnings('ignore')
    training_data = pd.read_csv(join(dirpath, 'training_data.csv'))
    odds_data = pd.read_csv(join(dirpath, 'odds_data.csv'))
    betting = Betting(estimator, param_grid)
    results = betting.simulate_results(training_data, odds_data, test_season, predicted_result, min_matches, odds_threshold, generate_weights, random_state)
    return results
