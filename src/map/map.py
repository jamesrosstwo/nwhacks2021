from enum import Enum, auto
import osmnx as ox
import networkx as nx
import folium

from src.definitions import SETTINGS, ROOT_PATH
import googlemaps


class TransportMode(Enum):
    DRIVE = auto(),
    TRANSIT = auto(),
    BIKE = auto(),
    WALK = auto()


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

        if transport_mode is TransportMode.DRIVE:
            pass
        elif transport_mode is TransportMode.TRANSIT:
            pass
        elif transport_mode is TransportMode.BIKE:
            pass
        elif transport_mode is TransportMode.WALK:
            self.graph = ox.graph_from_place(location, network_type='walk')
        else:
            raise Exception("Invalid transport mode passed to plot_route")

    def find_node(self, location: str):
        geocoded_loc = self.client.geocode(location)[0]["geometry"]["location"]
        lat, long = geocoded_loc["lat"], geocoded_loc["lng"]
        return ox.get_nearest_node(self.graph, (lat, long))

    def plot_route(self, dest, orig=None):
        if orig is None:
            orig = self.home_loc
        ox.config(log_console=True, use_cache=True)
        print("config done")

        origin = self.client.geocode(orig)[0]
        orig_loc = (origin["geometry"]["location"]["lat"], origin["geometry"]["location"]["lng"])
        orig_node = ox.get_nearest_node(self.graph, orig_loc)

        destination = self.client.geocode(dest)[0]
        dest_loc = (destination["geometry"]["location"]["lat"], destination["geometry"]["location"]["lng"])
        dest_node = ox.get_nearest_node(self.graph, dest_loc)

        route = nx.shortest_path(self.graph,
                                 orig_node,
                                 dest_node,
                                 weight='length')

        route_map = ox.plot_route_folium(self.graph, route)

        folium.TileLayer('openstreetmap').add_to(route_map)

        folium.Marker(
            list(orig_loc), popup="<i>" + origin["formatted_address"] + "</i>", tooltip="Origin"
        ).add_to(route_map)
        folium.Marker(
            list(dest_loc), popup="<i>" + destination["formatted_address"] + "</i>", tooltip="Destination"
        ).add_to(route_map)

        route_map.save(str(ROOT_PATH / self.settings["save_path"]))
