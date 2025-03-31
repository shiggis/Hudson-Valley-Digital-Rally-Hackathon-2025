import xml.etree.ElementTree as ET
from math import radians, cos, sin, sqrt, atan2 

# Load and parse OSM file
osm_file = r"C:\Users\Shannon\Downloads\HVTech\map.osm"
tree = ET.parse(osm_file)
root = tree.getroot()

# Helper function to calculate the area of a polygon using the Shoelace formula
def calculate_polygon_area(coords):
    n = len(coords)
    if n < 3: # Not a polygon
        return 0
    area = 0
    for i in range(n):
        x1, y1 = coords[i]
        x2, y2 = coords[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    return abs(area) / 2

# Build a dictionary of nodes with their coordinates
nodes = {}
for node in root.findall("node"):
    node_id = node.attrib["id"]
    lat = float(node.attrib["lat"])
    lon = float(node.attrib["lon"])
    nodes[node_id] = (lon, lat) # Store as (longitude, latitude)

# Find all ways tagged as grass areas and calculate their areas
grass_areas = []
for way in root.findall("way"):
    is_grass = False
    coords = []
    for tag in way.findall("tag"):
        if tag.attrib.get("k") == "landuse" and tag.attrib.get("v") == "grass":
            is_grass = True
    if is_grass:
        for nd in way.findall("nd"):
            node_id = nd.attrib["ref"]
            if node_id in nodes:
                coords.append(nodes[node_id])
        if coords:
            area = calculate_polygon_area(coords)
            grass_areas.append({"id": way.attrib["id"], "area": area})

# Print the IDs and area of grass areas
print("Grass Areas:")
for area in grass_areas:
    print(f"Way ID: {area['id']}, Area: {area['area']} square units")