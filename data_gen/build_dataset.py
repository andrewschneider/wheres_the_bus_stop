import sys
import json

from data_gen.geo import build_grid, get_closest_point
from data_gen.metro import load_existing_stops, load_future_stops

OUT_FPATH = "datasets/delta_distance.json"

MIN_MAX_FPATH = "datasets/legend_ticks_data.json"

def build_dataset(node_spacing=100):

    node_coordinates, lat_node_spacing, lon_node_spacing = build_grid(node_spacing)
    existing_stops = sorted(load_existing_stops())
    future_stops = sorted(load_future_stops())

    geo_json = {"type": "FeatureCollection", "features": []}

    output = []
    for [node_lon, node_lat] in node_coordinates:

        closest_existing = get_closest_point(node_lat, node_lon, existing_stops, manhattan=True)
        closest_future = get_closest_point(node_lat, node_lon, future_stops, manhattan=True)

        if closest_future["dist"] != closest_existing["dist"]:
            delta = (closest_future["dist"] - closest_existing["dist"]) / 80.45
            output.append([node_lat, node_lon, delta])

    max_delta = max([x[2] for x in output])
    min_delta = min([x[2] for x in output])

    for (node_lat, node_lon, delta) in output:
            coords = [
                [node_lon - lon_node_spacing / 2., node_lat + lat_node_spacing / 2.],  # NW corner
                [node_lon + lon_node_spacing / 2., node_lat + lat_node_spacing / 2.],  # NE corner
                [node_lon + lon_node_spacing / 2., node_lat - lat_node_spacing / 2.],  # SW corner
                [node_lon - lon_node_spacing / 2., node_lat - lat_node_spacing / 2.],  # SW corner
                [node_lon - lon_node_spacing / 2., node_lat + lat_node_spacing / 2.]   # NW corner
            ]

            idx = int(round((delta - min_delta) / (max_delta - min_delta) * 8.0))

            geo_json["features"].append({
                "type": "Feature", 
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords]
                },
                "properties": {
                    "color_idx": idx,
                    "max_delta": max_delta,
                    "min_delta": min_delta
                }
            })

    with open(OUT_FPATH, 'w') as f:
        f.write(json.dumps(geo_json))

    with open(MIN_MAX_FPATH, 'w') as g:
        step = (max_delta - min_delta) / 9.
        g.write(json.dumps([round(min_delta + i * step, 1) for i in xrange(0, 9)]))

if __name__ == "__main__":

    if len(sys.argv) > 1:
        node_spacing = float(sys.argv[1])
        build_dataset(node_spacing)
    else:
        build_dataset()
