import sys

import pygame
import numpy as np

colors = ["#00FF00",
          "#0000FF",
          "#FFFF00",
          "#FF00FF",
          "#00FFFF",
          "#800080",
          "#FFD700",
          "#008080",
          "#FF1493"
          ]

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)


class Point:
    def __init__(self, x, y, flag, name, cluster_id, point_id):
        self.x = x
        self.y = y
        self.flag = flag
        self.name = name
        self.cluster_id = cluster_id
        self.point_id = point_id


def init_screen():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    screen.fill(color=WHITE)
    pygame.display.update()
    return screen


def draw(screen, radius, m):
    drawing = True
    clock = pygame.time.Clock()
    points = []
    count_point_id = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if drawing:
                if pygame.mouse.get_pressed()[0]:
                    position = pygame.mouse.get_pos()
                    pygame.draw.circle(screen, color=BLACK, center=position, radius=7)
                    x1, y1 = position
                    count_point_id += 1
                    points.append(Point(x1, y1, False, "", None, count_point_id))

            if event.type == pygame.KEYDOWN:
                # при нажатии на 1
                if event.key == pygame.K_1:
                    points = db_scan(points, radius, m)
                # при нажатии на 2
                if event.key == pygame.K_2:
                    paint_clusters(points)

        pygame.display.update()
        clock.tick(10)


def db_scan(points, radius, m):
    clusters_point = 0
    for point in points:
        if point.flag is True:
            continue
        point.flag = True
        neighbor_points = region_query(points, point, radius)
        if len(neighbor_points) == 0:
            point.name = "noise"
        elif len(neighbor_points) >= m:
            clusters_point += 1
            point.name = "core"
            point.cluster_id = clusters_point
            expand_cluster(points, neighbor_points, clusters_point, radius, m)
    points = paint(points, radius)
    return points


def expand_cluster(points, neighbour_points, cluster, radius, m):
    for point in neighbour_points:
        if point.flag is False:
            point.flag = True
            q_neighbor_points = region_query(points, point, radius)
            if len(q_neighbor_points) >= m:
                point.name = "core"
                neighbour_points += q_neighbor_points  # Объединить списки соседей
            else:
                point.name = "border"
        if point.cluster_id is None:
            point.cluster_id = cluster
    for point in points:
        for neighbor in neighbour_points:
            if point.point_id == neighbor.point_id:
                point = neighbor

# Найти всех соседей точки в радиусе
def region_query(points, pointA, radius):
    neighbours = []
    for pointB in points:
        if (pointA != pointB):
            distance_to_point = calculate_distance(pointA, pointB)
            if distance_to_point <= radius:
                neighbours.append(pointB)
    return neighbours


def paint(points, radius):
    screen.fill(color=WHITE)
    pygame.display.update()
    noise_checking(points, radius)
    for point in points:
        if point.name == "core":
            pygame.draw.circle(screen, color=GREEN, center=(point.x, point.y), radius=7)
        if point.name == "border":
            pygame.draw.circle(screen, color=YELLOW, center=(point.x, point.y), radius=7)
        if point.name == "noise":
            pygame.draw.circle(screen, color=RED, center=(point.x, point.y), radius=7)
    return points


def noise_checking(points, radius):
    for point in points:
        if point.name == "":
            minimal_distance = sys.maxsize
            neighborhood = region_query(points, point, radius)
            for n in neighborhood:
                distance = calculate_distance(point, n)
                if n.name == "core" and minimal_distance > distance:
                    point.name = "border"
                    minimal_distance = distance
            if point.name == "":
                point.name = "noise"


def paint_clusters(points):
    screen.fill(color=WHITE)
    pygame.display.update()
    for point in points:
        if point.cluster_id is not None:
            pygame.draw.circle(screen, color=colors[point.cluster_id], center=(point.x, point.y), radius=7)
        else:
            pygame.draw.circle(screen, color=RED, center=(point.x, point.y), radius=7)


def calculate_distance(pointA, pointB):
    x1, y1 = pointA.x, pointA.y
    x2, y2 = pointB.x, pointB.y
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


if __name__ == "__main__":
    min_points_for_cluster = 5
    radius = 50

    screen = init_screen()
    draw(screen, radius, min_points_for_cluster)