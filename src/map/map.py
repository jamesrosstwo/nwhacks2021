from enum import Enum, auto
from typing import Tuple

import osmnx as ox
import networkx as nx
import folium
import polyline
from folium.plugins import MarkerCluster

from src.definitions import SETTINGS, ROOT_PATH
from src.map.density.choropleth import generate_density_choropleth
from src.map.events.exposure_events import get_events
from src.map.risk.risk import calculate_risk_score
from src.map.recommender.recommender import give_recommendation
import googlemaps


class TransportMode(Enum):
    DRIVE = auto(),
    TRANSIT = auto(),
    BIKE = auto(),
    WALK = auto()


transport_mode_gmaps_map = {
    TransportMode.DRIVE: "driving",
    TransportMode.TRANSIT: "transit",
    TransportMode.BIKE: "bicycling",
    TransportMode.WALK: "walking"
}


class CovidMap:
    def __init__(self, location: str, transport_mode: TransportMode):
        """
        Initialize covid map with given location that acts as the home location.
        :param location: String with a location to initialize the map. Example: 'Buffalo, New York, USA'
        :rtype: object
        """
        self.home_loc = location
        self.transport_mode = TransportMode.WALK
        self.settings = SETTINGS["map"]
        self.save_loc = self.settings["save_path"]
        self.api_key = self.settings["api_key"]

        self.client = googlemaps.Client(key=self.api_key)
        self.graph = None
        self.exposures = []

        str(ROOT_PATH / self.settings["save_path"])
        # # Look up an address with reverse geocoding
        # reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
        #
        # # Request directions via public transit
        # now = datetime.now()
        # directions_result = gmaps.directions("Sydney Town Hall",
        #                                      "Parramatta, NSW",
        #                                      mode="transit",
        #                                      departure_time=now)
        # print(directions_result)

        location = self.client.geocode(location)[0]["geometry"]["location"]
        loc_lat, loc_long = location["lat"], location["lng"]

        if transport_mode is TransportMode.DRIVE:
            self.graph = ox.graph_from_point((loc_lat, loc_long), network_type='drive', dist=5000)
        elif transport_mode is TransportMode.TRANSIT:
            pass
        elif transport_mode is TransportMode.BIKE:
            self.graph = ox.graph_from_point((loc_lat, loc_long), network_type='bike')
        elif transport_mode is TransportMode.WALK:
            self.graph = ox.graph_from_point((loc_lat, loc_long), network_type='walk')
        else:
            raise Exception("Invalid transport mode passed to plot_route")

    def find_node(self, location: str):
        geocoded_loc = self.client.geocode(location)[0]["geometry"]["location"]
        lat, long = geocoded_loc["lat"], geocoded_loc["lng"]
        return ox.get_nearest_node(self.graph, (lat, long))

    def make_popup(self, inner_html, width=300):
        iframe = folium.IFrame(inner_html)
        popup = folium.Popup(iframe,
                             min_width=width,
                             max_width=width)
        return popup

    def map_events(self, map_obj):
        events = get_events()
        marker_cluster = MarkerCluster().add_to(map_obj)
        for event in events:
            geocoded_loc = self.client.geocode(event["address"])
            if len(geocoded_loc) == 0:
                continue
            geocoded_loc = geocoded_loc[0]["geometry"]["location"]
            lat, long = geocoded_loc["lat"], geocoded_loc["lng"]
            self.exposures.append((lat, long))
            folium.Marker([lat, long],
                          popup=self.make_popup("<strong>COVID Exposure</strong><br> " + event["date"], width=150),
                          icon=folium.Icon(color="red", icon="exclamation-triangle", angle=0, prefix='fa')).add_to(
                marker_cluster)

    def decode_path(self, gmaps_path):
        return polyline.decode(gmaps_path[0]["overview_polyline"]["points"])

    def get_gmaps_path(self, src_loc: Tuple, dest_loc: Tuple):
        return self.client.directions(src_loc, dest_loc, mode=transport_mode_gmaps_map[self.transport_mode])

    def make_polyline(self, route, color="#0033cc"):
        polyline_path = self.decode_path(route)
        return folium.PolyLine(polyline_path, color=color, width=8)

    def plot_route(self, dest, orig=None):
        if orig is None:
            orig = self.home_loc
        ox.config(log_console=True, use_cache=True)

        origin = self.client.geocode(orig)[0]
        orig_loc = (origin["geometry"]["location"]["lat"], origin["geometry"]["location"]["lng"])
        orig_node = ox.get_nearest_node(self.graph, orig_loc)

        destination = self.client.geocode(dest)[0]
        dest_loc = (destination["geometry"]["location"]["lat"], destination["geometry"]["location"]["lng"])
        dest_node = ox.get_nearest_node(self.graph, dest_loc)

        route = self.get_gmaps_path(orig_loc, dest_loc)

        route_map = folium.Map(location=orig_loc, tiles="Stamen Terrain")

        self.make_polyline(route).add_to(route_map)

        self.map_events(route_map)

        folium.Marker(
            list(orig_loc), popup=self.make_popup("<i>" + orig + "</i>"), tooltip="Origin"
        ).add_to(route_map)

        dest_risk_score = calculate_risk_score(self, *dest_loc)
        destination_html = "<strong> Location: </strong><i>" + dest + \
                           "</i> <br> <strong> Risk Score: " + str(dest_risk_score * 100)[:4] + "%" \
                                                                                                "</strong> <br> <strong> Recommendation: </strong>" + \
                           give_recommendation(destination, dest_risk_score)
        folium.Marker(
            list(dest_loc), popup=self.make_popup(destination_html), tooltip="Destination"
        ).add_to(route_map)

        density_choropleth = generate_density_choropleth()
        density_choropleth.add_to(route_map)

        folium.LayerControl().add_to(route_map)

        route_map.save(str(ROOT_PATH / self.settings["save_path"]))
