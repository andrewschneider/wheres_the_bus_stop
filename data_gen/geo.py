import bisect
import math
import json

from shapely.geometry import shape, Point

EARTH_RADIUS = 6367000.  # mean Earth radius in meters
EARTH_CIRCUMFERENCE = EARTH_RADIUS * 2 * math.pi
MAX_DISTANCE = EARTH_CIRCUMFERENCE / 2  # ~ largest possible distance between 2 points as traced along Earth's surface

def haversine(coords1, coords2):
    """
    Calculates the distance between two gps coordinates using the Haversine forumla
    See http://en.wikipedia.org/wiki/Haversine_formula for reference
    """

    if False:
        return haversine_approx(coords1, coords2)

    else:
        lat1, lon1, lat2, lon2 = map(math.radians, [coords1[0], coords1[1], coords2[0], coords2[1]])

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2.) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2.) ** 2
        c = 2 * math.asin(math.sqrt(a))
        dist = EARTH_RADIUS * c
        return dist

def build_grid(node_spacing):
    "Return a list of [lon, lat] pairs that represent gaussian grid points inside the confines of the city of seattle"

    with open('datasets/seattle_outline.json') as f:
        seattle_outline = json.loads(f.read())

    coordinates = seattle_outline['features'][0]['geometry']['coordinates'][0]
    lon_values, lat_values = zip(*coordinates)
    polygon = shape(seattle_outline['features'][0]['geometry'])

    max_lat = max(lat_values)
    min_lat = min(lat_values)
    max_lon = max(lon_values)
    min_lon = min(lon_values)

    mid_lat = (max(lat_values) + min(lat_values)) / 2

    meters_per_degree_lat = EARTH_CIRCUMFERENCE / 360
    meters_per_degree_lon = haversine([mid_lat, 0.0], [mid_lat, 1.0])

    lat_node_spacing = node_spacing * (1. / meters_per_degree_lat)
    lon_node_spacing = node_spacing * (1. / meters_per_degree_lon)

    num_y_nodes = int(math.ceil((max_lat - min_lat) / lat_node_spacing))
    num_x_nodes = int(math.ceil((max_lon - min_lon) / lon_node_spacing))

    node_coords = []
    # start from SW corner
    for j in xrange(0, num_y_nodes):
        for i in xrange(0, num_x_nodes):
            point = Point(min_lon + i * lon_node_spacing, min_lat + j * lat_node_spacing)
            if polygon.contains(point):
                node_coords.append([point.x, point.y])

    return sorted(node_coords), lat_node_spacing, lon_node_spacing

def get_closest_point(lat, lon, points, manhattan=False):
    "points is a list of [lat, lon]"

    if [lat, lon] in points:
        return lat, lon, 0

    insert_index = bisect.bisect(points, [lat, lon])
    first_half = points[:insert_index]
    first_half.reverse()
    second_half = points[insert_index:]

    candidates = []
    min_d = MAX_DISTANCE

    for idx in xrange(0, max(len(first_half or []), len(second_half or []))):
        should_break = []

        if first_half and idx < len(first_half):
            candidate_lat = first_half[idx][0]
            candidate_lon = first_half[idx][1]

            dy = haversine([lat, lon], [candidate_lat, lon])
            if manhattan:
                dx = haversine([lat, lon], [lat, candidate_lon])
                d = dx + dy
            else:
                d = haversine([lat, lon], first_half[idx])

            min_d = min(min_d, d)
            candidates.append([d, candidate_lat, candidate_lon])

            if dy > min_d:
                should_break.append(True)
            else:
                should_break.append(False)

        if second_half and idx < len(second_half):
            candidate_lat = second_half[idx][0]
            candidate_lon = second_half[idx][1]

            dy = haversine([lat, lon], [candidate_lat, lon])
            if manhattan:
                dx = haversine([lat, lon], [lat, candidate_lon])
                d = dx + dy
            else:
                d = haversine([lat, lon], first_half[idx])

            min_d = min(min_d, d)
            candidates.append([d, candidate_lat, candidate_lon])

            if dy > min_d:
                should_break.append(True)
            else:
                should_break.append(False)

        if should_break and all(should_break):
            break

    if candidates:
        (closest_d, closest_lat, closest_lon) = sorted(candidates)[0]

        return {
            "dist": closest_d,
            "lat": closest_lat,
            "lon": closest_lon
        }
