import random
import numpy as np
import matplotlib.pyplot as plt

# Создание списка городов (пунктов) и расстояний между ними
cities = {
    "Ростов-на-Дону": (0, 0),
    "Саратов": (1, 3),
    "Казань": (2, 5),
    "Уфа": (4, 2),
    "Самара": (5, 0),
    "Уральск": (6, 4)
}

# Создание начальной популяции
def create_population(size):
    population = []
    for _ in range(size):
        route = list(cities.keys())
        random.shuffle(route)
        population.append(route)
    return population

# Вычисление длины маршрута
def calculate_distance(route):
    distance = 0
    for i in range(len(route) - 1):
        city1 = route[i]
        city2 = route[i + 1]
        dist = np.linalg.norm(np.array(cities[city1]) - np.array(cities[city2]))
        print(f"Distance from {city1} to {city2}: {dist}")
        distance += dist
    return distance

# Выбор родителей с использованием турнирного отбора
def select_parents(population, tournament_size=3):
    participants = random.sample(population, tournament_size)
    participants.sort(key=lambda x: calculate_distance(x))
    return participants[0]

# Скрещивание двух родителей для создания потомка
def crossover(parent1, parent2):
    crossover_point = random.randint(1, len(parent1) - 1)
    child = parent1[:crossover_point]
    for city in parent2:
        if city not in child:
            child.append(city)
    return child

# Мутация путем обмена двух городов
def mutate(route):
    idx1, idx2 = random.sample(range(len(route)), 2)
    route[idx1], route[idx2] = route[idx2], route[idx1]
    return route

# Генетический алгоритм
def genetic_algorithm(population_size, generations):
    population = create_population(population_size)

    for _ in range(generations):
        new_population = []

        for _ in range(population_size // 2):
            parent1 = select_parents(population)
            parent2 = select_parents(population)
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            new_population.extend([mutate(child1), mutate(child2)])

        population = new_population

    best_route = min(population, key=lambda x: calculate_distance(x))
    best_distance = calculate_distance(best_route)

    return best_route, best_distance

# Запуск генетического алгоритма
population_size = 100
generations = 500
best_route, best_distance = genetic_algorithm(population_size, generations)

# Вывод результатов
print("Best Route:", best_route)
print("Best Distance:", best_distance)

# Визуализация маршрута на карте
plt.figure(figsize=(8, 6))
x, y = zip(*[cities[city] for city in best_route + [best_route[0]]])
plt.plot(x, y, marker='o')
plt.title('Optimal TSP Route')
plt.xlabel('X-coordinate')
plt.ylabel('Y-coordinate')
plt.show()
