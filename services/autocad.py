import numpy as np
import re


def detect_mark(x):
    if re.match("шурф|Шурф|ШУРФ", x):
        return "ШФ"
    elif re.match("ЛЭП|лэп|леп|ЛЕП", x):
        return "ЛЭП"
    elif re.match("открытый|Открытый", x):
        return "ОУ"
    elif re.match("угол|Угол|УГОЛ", x):
        return "УП"
    elif re.match("дорога", x):
        return "ДРГ"
    else:
        return "НЕТ"


def detect_coordinates(x):
    return re.search(r"N.+", x).group()


def get_vectors():
    # Высчитываем вектор налево
    start = np.array([54, 106])
    end_point = np.array([99, 132])
    left_vector = end_point - start
    left_vector = left_vector / np.linalg.norm(left_vector)
    # Высчитываем вектор направо
    start = np.array([99, 132])
    end_point = np.array([191, 79])
    right_vector = end_point - start
    right_vector = right_vector / np.linalg.norm(right_vector)
    return left_vector, right_vector


def get_rectangle_position(start_point, vector, rect_width=20, rect_height=30):
    # Находим нормаль к вектору отрезка
    normal_vector = np.array([-vector[1], vector[0]])  # Поворот на 90 градусов
    normal_vector = normal_vector / np.linalg.norm(normal_vector)  # Нормализуем

    # Смещаем нижний левый угол прямоугольника вдоль нормали
    rectangle_position = start_point + normal_vector * rect_height  # Смещаем на высоту

    return rectangle_position


def autocad_decode():
    lines = []
    with open('data.txt', 'r', encoding='utf-8') as f:
        for i in f.readlines():
            lines.append(re.sub(r'\"', '', i))

    done = False
    length = 30
    direction_vector_right, direction_vector_left = get_vectors()
    marks = []
    crds = []
    while not done:
        start_point = np.array([50, 100])
        points = [start_point.tolist()]
        direction = direction_vector_right
        for i in range(1, len(lines)):
            if "+" in lines[i]:
                direction = direction_vector_right
            elif "-" in lines[i]:
                direction = direction_vector_left
            next_point = points[i - 1] + direction * length
            points.append(next_point.tolist())

        if points[1][0] < 235:
            done = True
        else:
            length -= 2
    for i, v in enumerate(lines):
        mark = detect_mark(v)
        marks.append(mark)
        crd = detect_coordinates(v)
        crds.append(crd)
        points[i].append(mark)
        points[i].append(crd)

    rectangles = []
    for i in range(len(points) - 1):
        start_point = np.array(points[i][:2])
        next_point = np.array(points[i + 1][:2])
        vector = next_point - start_point
        vector = vector / np.linalg.norm(vector)  # Нормализуем вектор
        rect_pos = get_rectangle_position(start_point, vector)
        rectangles.append(rect_pos)
    for i in rectangles:
        print(i)
    with open('data_done.txt', 'w') as f:
        for i in points:
            f.write(" ".join(list(map(str, i))) + "\n")
    for i in points:
        print(" ".join(list(map(str, i))))


if __name__ == '__main__':
    autocad_decode()
