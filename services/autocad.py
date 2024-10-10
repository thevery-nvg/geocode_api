import numpy as np
import math
import matplotlib.pyplot as plt
import re


def plot_line(points, labels):
    x_coords, y_coords = zip(*points)

    plt.figure(figsize=(8, 8))
    plt.plot(x_coords, y_coords, '-o')
    for i, j, l in zip(x_coords, y_coords, labels):
        plt.text(i, j, l)
    plt.grid()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Ломаная линия')
    plt.show()


def detect_mark(x):
    if re.search(r"[шШ][Фф]|шурф", x):
        return "ШФ"
    elif re.search(r"\+", x):
        return "УПП"
    elif re.search(r"\-", x):
        return "УПЛ"
    elif re.search(r"НПД|КПД|[Дд]орога", x):
        return "Дорога"
    elif re.search(r"[кК][тТ]", x):
        return "КТ"
    elif re.match(r"[Лл][эЭеЕ][пП]", x):
        return "ЛЭП"
    elif re.search(r"[оО][уУ]|открытый", x):
        return "ОУ"
    elif re.search(r"обваловка", x):
        return "обваловка"
    else:
        return "НЕТ МЕТКИ"


def detect_coordinates(x):
    lat = re.search(r"[nN].+[eE]", x).group()[:-1]
    lon = re.search(r"[Ee].+", x).group()
    return " ".join([lat, lon])


def autocad_decode():
    lines = []
    with open('E:\\Public\\web\\acad_data\data.txt', 'r') as f:
        for i in f.readlines():
            lines.append(re.sub(r'\"|\'| ', '', i))
    labels = []
    coordinates = []
    for i in lines:
        coordinates.append(detect_coordinates(i))
    for i in lines:
        labels.append(detect_mark(i))
    # Начальная точка
    start_point = np.array([50, 100])

    # Шаг длины (например, 10 единиц)
    step_length = 25

    # Углы в радианах для поворотов на 120 градусов
    angle_right = -1 * np.pi / 3  # -120 градусов
    angle_left = 1 * np.pi / 3  # +120 градусов

    # Матрицы поворота
    rotation_right = np.array([[np.cos(angle_right), -np.sin(angle_right)],
                               [np.sin(angle_right), np.cos(angle_right)]])
    rotation_left = np.array([[np.cos(angle_left), -np.sin(angle_left)],
                              [np.sin(angle_left), np.cos(angle_left)]])

    # Начальное направление (по оси X, вправо)
    current_direction = np.array([1, -0.5])

    # Список меток для поворотов
    # labels = ["faggot",'+', '-', 'asshole', '+', '-', '+',"motherfucker","+","fuck","-","bitch"]

    # Массив для хранения всех точек
    points = [start_point]

    # Проходим по меткам и вычисляем новые координаты точек
    for i, label in enumerate(labels):
        if "УПП" in label:
            # Поворот вправо
            current_direction = np.dot(rotation_right, current_direction)
        elif "УПЛ" in label:
            # Поворот влево
            current_direction = np.dot(rotation_left, current_direction)

        # Вычисляем новую точку и добавляем её в список
        new_point = points[-1] + current_direction * step_length
        new_point = new_point.tolist()
        points.append(new_point)
    result = []
    for p, l, c in zip(points, labels, coordinates):
        result.append(f"{p[0]} {p[1]} {l} {c}")
    # Преобразуем список точек в массив numpy
    for i in result:
        print(i)
    with open("E:\\Public\web\\acad_data\\lines.txt", "w") as f:
        for i in result:
            f.write(f"{i}\n")
    # plot_line(points,labels)


if __name__ == "__main__":
    autocad_decode()
