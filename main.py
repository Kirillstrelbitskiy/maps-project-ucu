import time
import doctest
import argparse
import folium
from geopy.geocoders import Nominatim
from geopy import distance
from functools import cmp_to_key

geolocator = Nominatim(user_agent="geomap-app")


def coordinates(address):
    """
    Return coordinates by address.
    """

    return geolocator.geocode(address)


def parse_locations(file_name):
    """
    Parses given file to get films list.
    """

    locations = []

    print("Started the parsing of locations file")

    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            line = line.split("\t")

            if len(line) > 2:
                location_address = line[len(line) - 2]

                if location_address:
                    pos = line[0].find(')')
                    film_name = line[0][:pos+1]

                    location = coordinates(location_address)

                    if location:
                        film_data = [film_name, location.address,
                                     (location.latitude, location.longitude)]

                        if film_data not in locations:
                            locations.append(film_data)

    print("Finished the parsing of locations file")

    return locations


def check_int(value):
    """
    Function checks whether given value is integer.
    >>> check_int("2016_")
    False
    >>> check_int("2016")
    True
    """

    str_value = str(value)

    for element in str_value:
        if element not in "0123456789":
            return False

    return True


def year_locations(locations, year):
    """
    Selects only locations with given year.
    """

    selected_locations = []

    for film_data in locations:
        film = film_data[0]

        pos = len(film)

        film_year = film[pos-5:pos-1]

        if check_int(film_year):
            film_year = int(film[pos-5:pos-1])

            if film_year == year:
                selected_locations.append(film_data)

    return selected_locations


def compare(item1, item2):
    """
    Custom comparator for sorting.
    """

    if item1[3] < item2[3]:
        return 1
    if item1[3] > item2[3]:
        return -1
    return 0


def sort_by_dist(locations, geo):
    """
    Sorting locations by distance from the position.
    """

    locations_dist = []

    for location in locations:
        locations_dist.append(location)

        dist = distance.distance(location[2], geo).km
        locations_dist[-1].append(dist)

    sorted_locations = sorted(
        locations_dist, key=cmp_to_key(compare), reverse=True)

    return sorted_locations


def find_closest(locations, number, max_dist):
    """
    Finds the closest locations with given restrictions.
    """

    if not locations:
        return []

    pos = 1
    while pos < number and locations[pos][3] <= max_dist:
        pos += 1

    return locations[:pos]


def build_map(geo, locations):
    """
    Builds map and save it to map.html.
    """

    mp = folium.Map(location=geo, zoom_start=7)

    for film in locations:
        folium.Marker(
            [film[2][0], film[2][1]], popup=film[0]
        ).add_to(mp)

    folium.Marker(
        [geo[0], geo[1]],
        popup="Given spot",
        icon=folium.Icon(color="red")
    ).add_to(mp)

    if locations:
        farest_dist = (locations[-1][3] + 1) * 1000

        folium.Circle(location=[geo[0], geo[1]],
                      radius=farest_dist, weight=1,
                      fill_color='#3186cc').add_to(mp)

    folium.LatLngPopup().add_to(mp)

    mp.save("map.html")


def read_input():
    """
    Read the data using argparse.
    """

    parser = argparse.ArgumentParser(description='Build the map.')
    parser.add_argument('year', type=int,
                        help='The year for search')
    parser.add_argument('latitude', type=float,
                        help='Latitude')
    parser.add_argument('longitude', type=float,
                        help='Longitude')
    parser.add_argument('file_name', type=str,
                        help='File to parse')

    args = parser.parse_args()

    return [args.year, (args.latitude, args.longitude), args.file_name]


def main():
    """
    The main function.
    """

    data = read_input()

    starting_time = time.time()

    all_locations = parse_locations(data[2])

    selected_locations = year_locations(all_locations, data[0])
    sorted_locations = sort_by_dist(selected_locations, data[1])
    final_locations = find_closest(sorted_locations, 10, 1000)

    build_map(data[1], final_locations)

    taken_time = round(time.time() - starting_time, 2)

    print("A map was built successfully!\nTaken time: " + str(taken_time) + "s.")


if __name__ == "__main__":
    main()

# python main.py 2016 43.422037 -80.525161 locations_simple.list

doctest.testmod()
