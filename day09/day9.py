"""day9 solution"""
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import Iterable


@dataclass
class Route:
    location1: str
    location2: str
    cost: int

    def orient(self, location: str) -> "Route":
        if location == self.location1:
            return self
        return Route(self.location2, self.location1, self.cost)

    def get_destination(self, location: str) -> None | str:
        if location == self.location1:
            return self.location2
        elif location == self.location2:
            return self.location1
        return None


class Location:
    name: str
    connections: dict[str, int]

    def __init__(self, name: str, routes: list[Route]) -> None:
        self.name = name
        self.connections = {}
        for route in routes:
            dest = route.get_destination(self.name)
            if dest is None:
                continue
            self.connections[dest] = route.cost


@dataclass(order=True)
class Tour:
    """Sortable tour"""

    cost: int
    cities: list[str]
    city_set: set[str] = field(repr=False, init=False, compare=False)

    def __post_init__(self) -> None:
        self.city_set = set(self.cities)


def get_input() -> list[Route]:
    """Parses our input file into well defined routes"""
    routes: list[Route] = []
    with open("input.txt") as file:
        for line in file:
            items = line.split()
            loc1, loc2, cost = items[0], items[2], items[4]
            routes.append(Route(loc1, loc2, int(cost)))
    return routes


def main() -> None:
    """solves our tours"""
    routes: list[Route] = get_input()
    tours: list[Tour] = solve(routes)
    tours.sort()
    print(tours[0])
    print(tours[-1])


def get_city_names(routes: list[Route]) -> set[str]:
    """Get city names from list of routes"""
    city_names: set[str] = set()
    for route in routes:
        city_names.add(route.location1)
        city_names.add(route.location2)
    return city_names


def create_locations(
    city_names: Iterable[str], routes: list[Route]
) -> dict[str, Location]:
    """create Locations and map them to a dict based on the city name"""
    return {city_name: Location(city_name, routes) for city_name in city_names}


def solve(routes: list[Route]) -> list[Tour]:
    # init city name list
    city_names = get_city_names(routes)
    locations = create_locations(city_names, routes)

    # add our start points
    queue: PriorityQueue[Tour] = PriorityQueue()
    tours = [Tour(0, [city_name]) for city_name in city_names]
    for starting_tour in tours:
        queue.put(starting_tour)

    # solve
    results = []
    while not queue.empty():
        tour: Tour = queue.get()
        if len(tour.cities) == len(city_names):
            results.append(tour)
            continue
        current_city: Location = locations[tour.cities[-1]]
        for connection, cost in current_city.connections.items():
            if connection in tour.city_set:
                continue
            to_add: Tour = Tour(tour.cost + cost, tour.cities + [connection])
            queue.put(to_add)
    return results


if __name__ == "__main__":
    main()
