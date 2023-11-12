import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
import tkinter as tk

# Инициализация данных
data = {'X': [], 'Y': [], 'Class': []}

# Функция для добавления точек в списки данных
def add_point(event):
    x, y = event.xdata, event.ydata
    data['X'].append(x)
    data['Y'].append(y)
    data['Class'].append(1 if event.button == 1 else -1)

    color = 'red' if event.button == 1 else 'blue'
    plt.scatter(x, y, c=color)
    plt.draw()

# Функция для обучения SVM и рисования разделяющей прямой
def train_and_plot():
    if len(data['X']) < 2:
        print("Необходимо добавить минимум две точки для обучения.")
        return

    X = np.array(list(zip(data['X'], data['Y'])))
    y = np.array(data['Class'])

    # Обучение модели
    clf.fit(X, y)

    # Рисуем разделяющую прямую
    ax.plot([-10, 10], [(-clf.intercept_[0] - clf.coef_[0][0] * (-10)) / clf.coef_[0][1],
                       (-clf.intercept_[0] - clf.coef_[0][0] * 10) / clf.coef_[0][1]], 'k--')
    plt.draw()

# Функция для добавления новой точки после обучения
def add_new_point(event):
    x, y = event.xdata, event.ydata
    new_point = np.array([[x, y]])
    prediction = clf.predict(new_point)

    color = 'red' if prediction == 1 else 'blue'
    plt.scatter(x, y, c=color)
    plt.draw()

# Создание окна tkinter
root = tk.Tk()
root.title("SVM Example")

# Создание поля для рисования
fig, ax = plt.subplots()
ax.set_title('Click to add points (left: class 1, right: class -1)')
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

# Привязка событий к функциям
fig.canvas.mpl_connect('button_press_event', add_point)
train_button = tk.Button(root, text="Train SVM", command=train_and_plot)
train_button.pack()
fig.canvas.mpl_connect('button_press_event', add_new_point)

# Создание SVM модели
clf = svm.SVC(kernel='linear', C=1.0)

# Запуск главного цикла tkinter
plt.show()
root.mainloop()
