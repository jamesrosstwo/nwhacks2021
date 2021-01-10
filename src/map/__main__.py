from src.map.map import CovidMap, TransportMode

covid_map = CovidMap("Dunbar H mart", TransportMode.DRIVE)

covid_map.plot_route("Angus T")
