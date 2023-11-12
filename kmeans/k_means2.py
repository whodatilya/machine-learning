import random
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os


# Шаг 1: Создайте случайные точки на плоскости
def generate_random_points(num_points, seed=0):
    random.seed(seed)
    points = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(num_points)]
    return points

# Метод для последующего определения оптимального количества кластеров
def elbow_method(data, max_k):
    inertia_values = []

    for k in range(1, max_k + 1):
        # Вызываем вашу функцию k_means с разными значениями k
        clusters = k_means(data, k)
        # Рассчитываем сумму внутригрупповых дисперсий для этого значения k
        inertia = calculate_inertia(clusters)
        inertia_values.append(inertia)

    # Определение оптимального k на основе метода локтя
    print(inertia_values)
    optimal_k = find_optimal_k(inertia_values)

    # Постройка графика метода локтя
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, max_k + 1), inertia_values, marker='o', linestyle='-')
    plt.title('Метод локтя для определения оптимального k')
    plt.xlabel('Число кластеров (k)')
    plt.ylabel('Сумма внутригрупповых дисперсий')
    plt.grid()
    plt.show()
    print(f"Оптимальное количество кластеров (k): {optimal_k}")

    return optimal_k

def find_optimal_k(inertia_values):
    # Находим разницу между последовательными значениями суммы внутригрупповых дисперсий
    differences = [inertia_values[i] - inertia_values[i - 1] for i in range(1, len(inertia_values))]
    elbow_index = None
    print(differences)
    # Проходим по элементам массива и находим "локоть"
    for i in range(1, len(differences) - 1):
        if differences[i] < differences[i - 1] and differences[i] < differences[i + 1]:
            elbow_index = i
            break

    # Выводим индекс "локтя" (или None, если "локоть" не найден)
    # optimal_k_index = np.argmax(differences) + 1
    # print(np.argmax(differences) + 1)
    # print(optimal_k_index)

    # Возвращаем оптимальное значение k, -1, потому что с 1 id идём
    return elbow_index - 1
    # return optimal_k_index


# Метод для рассчета суммы внутригрупповых дисперсий
def calculate_inertia(clusters):
    #  Это переменная, в которой будет накапливаться сумма внутригрупповых дисперсий.
    inertia = 0
    # clusters -- список, содержащий кластеры, в которые были разделены данные.
    for cluster in clusters:
        # Находим центроид для кластера
        cluster_center = np.mean(cluster, axis=0)
        for point in cluster:
            # Расстояние между каждой точкой и центроидом кластера
            inertia += np.linalg.norm(point - cluster_center) ** 2
    return inertia


# Шаг 2: Определите функцию для вычисления расстояния между двумя точками
def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


# Шаг 3: Определите функцию для определения ближайшего центроида для каждой точки
def assign_to_clusters(points, centroids):
    clusters = [[] for _ in range(len(centroids))]
    for point in points:
        distances = [distance(point, centroid) for centroid in centroids]
        cluster_index = np.argmin(distances)
        clusters[cluster_index].append(point)
    return clusters


# Шаг 4: Определите функцию для обновления центроидов
def update_centroids(clusters):
    new_centroids = []
    for cluster in clusters:
        if len(cluster) > 0:
            cluster_x = [point[0] for point in cluster]
            cluster_y = [point[1] for point in cluster]
            new_centroid = (np.mean(cluster_x), np.mean(cluster_y))
            new_centroids.append(new_centroid)
    return new_centroids


# Шаг 5: Определите функцию для рисования точек и центроидов
def plot_clusters(points, centroids, step, image_filenames):
    plt.figure(figsize=(8, 6))
    for i, cluster in enumerate(points):
        cluster_x = [point[0] for point in cluster]
        cluster_y = [point[1] for point in cluster]
        plt.scatter(cluster_x, cluster_y, label=f'Cluster {i + 1}')
    centroid_x = [centroid[0] for centroid in centroids]
    centroid_y = [centroid[1] for centroid in centroids]
    plt.scatter(centroid_x, centroid_y, marker='x', s=200, color='black', label='Centroids')
    plt.title(f'Step {step}')
    plt.legend()

    # Сохраняем изображение как файл PNG
    image_filename = f'step_{step}.png'
    if os.path.exists(image_filename):
        os.remove(image_filename)
    plt.savefig(image_filename)
    plt.close()

    # Добавляем имя файла изображения в список
    image_filenames.append(image_filename)


# Шаг 6: Основной цикл алгоритма k-means
def k_means(points, k, max_steps=10):
    # Начальное случайное размещение центроидов
    centroids = random.sample(points, k)

    # Создаем список для хранения имен файлов изображений
    image_filenames = []

    for step in range(max_steps):
        # Шаг 2: Назначение точек к ближайшим центроидам
        clusters = assign_to_clusters(points, centroids)
        # Шаг 3: Обновление центроидов
        new_centroids = update_centroids(clusters)
        # Рисование текущего состояния
        plot_clusters(clusters, new_centroids, step, image_filenames)
        # Проверка на сходимость
        if centroids == new_centroids:
            break
        centroids = new_centroids

    # Создаем анимацию GIF из сохраненных изображений
    save_images_as_gif(image_filenames, 'k_means_animation.gif')
    return clusters


# Функция для создания анимации GIF из изображений
def save_images_as_gif(image_filenames, gif_filename):
    images = [Image.open(filename) for filename in image_filenames]
    images[0].save(gif_filename, save_all=True, append_images=images[1:], duration=500, loop=0)


if __name__ == "__main__":

    num_points = 100
    max_k = 10

    points = generate_random_points(num_points)

    k = elbow_method(points, max_k)  # Оптимальное количество кластеров
    k_means(points, k)
