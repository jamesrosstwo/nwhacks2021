import pathlib
from src.definitions import SETTINGS, ROOT_PATH
import folium
from src.map.density.scraper import load_data


def generate_density_choropleth():
    region_geo = str(ROOT_PATH / "map/data/census_subdivisions3.geojson")
    data = load_data()
    region_choropleth = folium.Choropleth(geo_data=region_geo,
                                          data=data,
                                          columns=data.columns,
                                          key_on="feature.properties.CSDUID",
                                          fill_color='YlOrRd',
                                          fill_opacity=0.4,
                                          line_opacity=0,
                                          legend_name='Population Density by Census Division'
                                          )

    region_choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['CSDNAME'], labels=False))
    return region_choropleth
