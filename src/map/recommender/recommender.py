from datetime import datetime

import requests
from src.definitions import SETTINGS, ROOT_PATH
import json


def best_time(location, query):
    url = "https://besttime.app/api/v1/keys/" + SETTINGS["map"]["best_time_api_key"]

    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)

    url = "https://besttime.app/api/v1/forecasts"

    params = {
        'api_key_private': SETTINGS["map"]["best_time_api_key"],
        'venue_name': query,
        'venue_address': location["formatted_address"]
    }

    response = requests.request("POST", url, params=params)
    data = json.loads(response.text)

    return data["analysis"][datetime.today().weekday()]


def give_recommendation(location, query, risk_score):
    best_time_analysis = best_time(location, query)
    safest_times = [str(x) + ":00, " for x in best_time_analysis["quiet_hours"][:-1]]
    safest_time = "".join(safest_times) + "or " + str(best_time_analysis["quiet_hours"][-1]) + ":00"

    if risk_score > 0.8:
        return "This is in an area with high risk, it may be a good idea to consider going somewhere else. " \
               "Safer alternatives to this location have been placed on your map with a green marker. " \
               "If you need to go to this location, we recommend going at " + safest_time + ", when it should be the least crowded."
    if risk_score > 0.5:
        return "This is in an area that has a higher than average risk. " \
               "We recommend going at " + safest_time + ", when it should be the least crowded." \
                                                        "If you are interested in looking at alternative locations, they have been placed on your map as green markers."
    if risk_score > 0.2:
        return "This is in an area with normal risk. " \
               "If you'd like to be safest, we recommend visiting at " + safest_time + ", when it is least busy."
    else:
        return "This is in an area with low risk, and is safer than most other locations. Extra precautions you could" \
               "take include visiting at " + safest_time + ", when it is least busy."
