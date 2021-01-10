def best_time(location):
    pass


def give_recommendation(location, risk_score):
    safest_time = "Xpm"
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
