import numpy as np
import re


def detect_mark(x):
    if re.match("шурф|Шурф ШУРФ", x):
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


lines = []
with open('data2.txt', 'r', encoding='utf-8') as f:
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
for i,v in enumerate(lines):
    mark = detect_mark(v)
    marks.append(mark)
    crd = detect_coordinates(v)
    crds.append(crd)
    points[i].append(mark)
    points[i].append(crd)

with open('data.txt', 'w') as f:
    for i in points:
        f.write(" ".join(list(map(str, i))) + "\n")
for i in points:
    print(" ".join(list(map(str, i))))
