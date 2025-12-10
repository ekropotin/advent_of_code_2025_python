from dataclasses import dataclass


@dataclass
class Edge:
    from_x: int
    from_y: int
    to_x: int
    to_y: int


def area(x1, y1, x2, y2):
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


def main():
    tiles = []
    edges = []
    with open("input.txt") as f:
        lines = f.readlines()
        y, x = map(int, lines[0].split(","))
        first_tile = (x, y)
        for i in range(0, len(lines) - 1):
            y, x = map(int, lines[i].split(","))
            next_y, next_x = map(int, lines[i + 1].split(","))
            tiles.append((x, y))
            edges.append(Edge(x, y, next_x, next_y))
        tiles.append((x, y))
        # complete polygon
        edges.append(Edge(next_x, next_y, first_tile[0], first_tile[1]))

    ## The key to the solution is the observation, that a rectangular is fully enclosed within the polygon
    ## If none of the polygon's edges cross the edges of the rectangle.
    ## We can use AABB collision detection algorithm to detect that.
    def intersect(x1, y1, x2, y2):
        for edge in edges:
            min_x, max_x = min(x1, x2), max(x1, x2)
            min_y, max_y = min(y1, y2), max(y1, y2)
            edge_min_x, edge_max_x = (
                min(edge.from_x, edge.to_x),
                max(edge.from_x, edge.to_x),
            )
            edge_min_y, edge_max_y = (
                min(edge.from_y, edge.to_y),
                max(edge.from_y, edge.to_y),
            )
            if (
                min_x < edge_max_x
                and max_x > edge_min_x
                and min_y < edge_max_y
                and max_y > edge_min_y
            ):
                return True
        return False

    max_area = 0
    for i in range(0, len(tiles)):
        x1, y1 = tiles[i]
        for j in range(0, len(tiles)):
            x2, y2 = tiles[j]
            a = area(x1, y1, x2, y2)
            if a <= max_area:
                continue
            if not intersect(x1, y1, x2, y2):
                max_area = a

    print(max_area)


if __name__ == "__main__":
    main()
