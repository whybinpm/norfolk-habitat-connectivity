import folium
import geopandas as gpd
import rasterio
from pyproj import Transformer

# Convert BNG bounds to WGS84
transformer = Transformer.from_crs("EPSG:27700", "EPSG:4326", always_xy=True)

with rasterio.open('outputs/SSI_raster_proximity_map_referenced_image.tif') as src:
    b = src.bounds

west, south = transformer.transform(b.left, b.bottom)
east, north = transformer.transform(b.right, b.top)

print(f"WGS84 bounds: south={south:.4f}, west={west:.4f}, north={north:.4f}, east={east:.4f}")

# Load SSSI layer
sssi = gpd.read_file('shapefiles/processed/SSSI_northnorfolk.gpkg')
print(f"SSSI layer loaded - {len(sssi)} features")

# Reproject to WGS84
sssi = sssi.to_crs(epsg=4326)
print("Reprojected to WGS84")

# Get centre coordinates
bounds = sssi.total_bounds
centre_lat = (bounds[1] + bounds[3]) / 2
centre_lon = (bounds[0] + bounds[2]) / 2
print(f"Map centre: {centre_lat:.4f}, {centre_lon:.4f}")

# Create base map
m = folium.Map(
    location=[centre_lat, centre_lon],
    zoom_start=10,
    tiles='CartoDB positron'
)

# Load Priority Habitat Inventory
phi = gpd.read_file('shapefiles/processed/priority_habitat_inventory_NN_clipped.gpkg')
print(f"PHI layer loaded - {len(phi)} features")

# Reproject to WGS84
phi = phi.to_crs(epsg=4326)

# Define colours by habitat type
habitat_colours = {
    'Coastal and floodplain grazing marsh': '#4B0082',
    'Coastal sand dunes': '#F4A460',
    'Deciduous woodland': '#228B22',
    'Good quality semi improved grassland': '#90EE90',
    'Lowland calcareous grassland': '#00FF00',
    'Lowland dry acid grassland': '#ADFF2F',
    'Lowland fens': '#BFFF00',
    'Lowland heathland': '#FFD700',
    'Lowland meadows': '#FFA500',
    'Maritime cliff and slope': '#FF8C00',
    'No main habitat but additional habitats present': '#808080',
    'Purple moor grass and rush pastures': '#00FFFF',
    'Traditional orchard': '#8B0000',
}

def habitat_style(feature):
    habitat = feature['properties'].get('mainhabs', '')
    colour = habitat_colours.get(habitat, '#808080')
    return {
        'fillColor': colour,
        'color': 'black',
        'weight': 0.5,
        'fillOpacity': 0.6
    }

# Add PHI layer
folium.GeoJson(
    phi,
    name='Priority Habitats (Natural England)',
    style_function=habitat_style,
    tooltip=folium.GeoJsonTooltip(fields=['mainhabs'])
).add_to(m)

# Load corridor links layer
corridors = gpd.read_file('outputs/potential_PHI_corridor_links.gpkg')
print(f"Corridor links loaded - {len(corridors)} features")

# Reproject to WGS84
corridors = corridors.to_crs(epsg=4326)

# Add corridor links layer
folium.GeoJson(
    corridors,
    name='Potential Habitat Corridor Links',
    style_function=habitat_style,
    tooltip=folium.GeoJsonTooltip(fields=['mainhabs'])
).add_to(m)

# Add SSSI layer
folium.GeoJson(
    sssi,
    name='Sites of Special Scientific Interest (SSSIs)',
    style_function=lambda x: {
        'fillColor': 'none',
        'color': 'red',
        'weight': 2,
        'fillOpacity': 0
    },
    tooltip=folium.GeoJsonTooltip(fields=['SSSI_NAME'] if 'SSSI_NAME' in sssi.columns else [])
).add_to(m)

# Add proximity raster as image overlay
folium.raster_layers.ImageOverlay(
    image='outputs/proximity_styled.png',
    bounds=[[52.6758, 0.7026], [52.9947, 1.6943]],
    opacity=0.4,
    name='Distance from nearest SSSI (metres)',
    overlay=True
).add_to(m)

title_html = '''
<div style="position: fixed; top: 10px; left: 50px; z-index:1000; 
background-color: white; padding: 10px; border-radius: 5px;
border: 1px solid grey; font-size: 14px; font-family: Arial;">
<b>North Norfolk Habitat Connectivity Analysis</b><br>
<span style="font-size: 11px; color: grey;">SSSI proximity and priority habitat distribution</span>
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Add layer control
folium.LayerControl().add_to(m)

# Save output
m.save('outputs/norfolk_habitat_map.html')
print("Map saved to outputs/norfolk_habitat_map.html")