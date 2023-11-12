import sys

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris

def normalize_iris_dataset(dataset):
    normalized_dataset = dataset

    data = normalized_dataset.data
    # минимум и максимум для каждого столбца
    for j in range(4):
        minimum = min_dataset_param(data, j)
        maximum = max_dataset_param(data, j)

        # нормализируем столбец
        for i in range(len(data)):
            data[i][j] = (data[i][j] - minimum) / (maximum - minimum)

    return normalized_dataset

def plot_iris(dataset):
    fig, ax = plt.subplots(3, 3, figsize=(12, 10))
    for i in range(4):
        for j in range(i + 1, 4):
            # точки
            scatter = ax[i][j - 1].scatter(dataset.data[:, i], dataset.data[:, j], c=dataset.target)
            # метки по осям
            ax[i][j - 1].set(xlabel=dataset.feature_names[i], ylabel=dataset.feature_names[j])
            # вывод классов
            ax[i][j - 1].legend(scatter.legend_elements()[0], dataset.target_names,
                                loc="lower right", title="classes")

    plt.show()



def normalize_new_object(item, dataset):
    for i in range(4):
        minimum = min_dataset_param(dataset.data, i)
        maximum = max_dataset_param(dataset.data, i)

        item[i] = min((item[i] - minimum) / (maximum - minimum), 1)

    return item


def min_dataset_param(data, index):
    min_param = sys.maxsize
    for i in range(len(data)):
        if data[i][index] < min_param:
            min_param = data[i][index]
    return min_param


def max_dataset_param(data, index):
    max_param = -float('inf')
    for i in range(len(data)):
        if data[i][index] > max_param:
            max_param = data[i][index]
    return max_param


def generate_test_dataset(dataset):
    test_dataset = []
    train_dataset = []

    dataset_items = []
    for i in range(len(dataset.data)):
        dataset_items.append([dataset.data[i], dataset.target[i]])

    for i in range(len(dataset.data)):
        # В тестовые данные уходит каждый 5-ый эл-т
        if i % 5 == 0:
            test_dataset.append(dataset_items[i])
        else:
            train_dataset.append(dataset_items[i])

    return train_dataset, test_dataset


def optimal_k(train_dataset, test_dataset):
    n = len(train_dataset) + len(test_dataset)
    optimal = 1
    best_accuracy = 0

    for k in range(1, int(np.sqrt(n))):
        counter = 0
        for item in test_dataset:
            item_class = knn_class(item[0], train_dataset, k)
            if item_class == item[1]:
                counter += 1
        accuracy = counter / len(test_dataset)

        if accuracy > best_accuracy:
            optimal = k
            best_accuracy = accuracy
    return optimal, best_accuracy


def knn_class(item, train_dataset, k):
    # отсортированный массив массивов. Первый элемент дистанция, а второй до какого класса
    distances = sorted_of_distance(item, train_dataset)
    # массив для дальнейшего высчитывания частоты
    class_arr = []
    # словарь для частоты классов
    freq_arr = {0: 0, 1: 0, 2: 0}

    for j in range(k):
        class_arr.append(distances[j][1])
        # Частота каждого числа
    for num in class_arr:
        freq_arr[num] += 1
        # Число с максимальной частотой
    most_common_class = max(freq_arr, key=freq_arr.get)
    return most_common_class


def sorted_of_distance(item, train_dataset):
    dist_array = []
    for i in range(len(train_dataset)):
        empty_array = []
        empty_array.append(dist(train_dataset[i][0], item))
        empty_array.append(train_dataset[i][1])

        dist_array.append(empty_array)
    sorted_array = sorted(dist_array, key=lambda x: x[0])

    return sorted_array


def dist(a, b):
    return np.sqrt(
        (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2 + (a[3] - b[3]) ** 2)


if __name__ == "__main__":
    iris_dataset = load_iris()
    # график до нормализации
    plot_iris(iris_dataset)

    normalize_dataset = normalize_iris_dataset(iris_dataset)
    # график после нормализации
    plot_iris(iris_dataset)

    # делим данные на тестовые
    train_dataset, test_dataset = generate_test_dataset(normalize_dataset)
    # находим оптимальное количество соседей
    optimal, best_accuracy = optimal_k(train_dataset, test_dataset)

    print(f'Оптимальное количество соседей: {optimal}, Точность: {best_accuracy}')

    iris_dataset = load_iris()

    new_object = [
        5,   # sep l
        4,   # sep w
        3,   # pet l
        2    # pet w
    ]

    new_object = normalize_new_object(new_object, iris_dataset)
    print(f'Новый объект после нормализации - {new_object}')
    new_object_class = knn_class(new_object, train_dataset, optimal)
    print(f'Класс нового объекта - {iris_dataset.target_names[new_object_class]}')

