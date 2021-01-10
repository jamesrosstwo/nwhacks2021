import numpy as np
import math


def calculate_exposure_score(exposures, lat, long):
    score = 0
    for exposure in exposures:
        # Score += 1 / distance from exposure
        score += 1 / (math.sqrt((lat - exposure[0]) ** 2 + (long - exposure[1]) ** 2))
    return np.tanh(score)  # Clamp between 0 and 1


def calculate_risk_score(covid_map, lat, long):
    return calculate_exposure_score(covid_map.exposures, lat, long)
