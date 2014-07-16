import collections

# TODO: add a shell script to fetch the stop data with curl

def load_existing_stops(return_ids=False):

    stop_coords = {}
    with open("datasets/stops.txt") as f:
        for i, line in enumerate(f):

            if i > 0:
                split_line = line.split(",")
                stop_id = int(split_line[0].replace('"', ''))
                lat = float(split_line[-3].replace('"', ''))
                lon = float(split_line[-2].replace('"', ''))
                stop_coords[stop_id] = [lat, lon]

    return return_ids and stop_coords or stop_coords.values()

def load_future_stops():

    existing_stops = load_existing_stops(return_ids=True)

    with open("datasets/deleted_stops.txt") as f:
        for line in f:
            stop_id = int(line.strip())

            if stop_id in existing_stops:
                del existing_stops[stop_id]
            # else:
            #     print stop_id

    return existing_stops.values()
