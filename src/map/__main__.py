from src.map.map import CovidMap, TransportMode

covid_map = CovidMap("Vancouver, British Columbia, Canada", TransportMode.WALK)

covid_map.plot_route("University of British Columbia")
