import numpy as np


def create_rotation_matrix(angle_degrees):
    print(f"{angle_degrees=}")
    """
    Создает поворотную матрицу для заданного угла в градусах.

    Args:
        angle_degrees (int): Угол в градусах. Должен быть в диапазоне от -120 до 120.

    Returns:
        np.ndarray: Поворотная матрица для заданного угла.
    """
    # Проверяем, что угол в градусах находится в диапазоне от -120 до 120
    if not -120 <= angle_degrees <= 120:
        raise ValueError("Угол должен быть в диапазоне от -120 до 120 градусов")

    # Преобразуем угол из градусов в радианы
    angle_radians = np.deg2rad(angle_degrees)

    # Создаем поворотную матрицу
    rotation_matrix = np.array([[np.cos(angle_radians), -np.sin(angle_radians)],
                                [np.sin(angle_radians), np.cos(angle_radians)]])
    return rotation_matrix


def autocad_decode_api(labels):
    labels = [x for x in labels.values()]
    # Начальная точка
    start_point = np.array([50, 100])
    # Шаг длины
    step_length = 25
    # Углы в радианах для поворотов на 120 градусов
    angle_right = -1 * np.pi / 3  # -120 градусов
    angle_left = 1 * np.pi / 3  # +120 градусов

    # Матрицы поворота
    rotation_right = np.array([[np.cos(angle_right), -np.sin(angle_right)],
                               [np.sin(angle_right), np.cos(angle_right)]])
    rotation_left = np.array([[np.cos(angle_left), -np.sin(angle_left)],
                              [np.sin(angle_left), np.cos(angle_left)]])
    # Начальное направление
    current_direction = np.array([1, -0.5])
    points = [start_point]
    for label in labels:
        if "+" in label:
            # Поворот вправо
            current_direction = np.dot(rotation_right, current_direction)
        elif "-" in label:
            # Поворот влево
            current_direction = np.dot(rotation_left, current_direction)
        new_point = points[-1] + current_direction * step_length
        new_point = new_point.tolist()
        points.append(new_point)
    d = {}
    for i in points[:-1]:
        d[float(i[0])] = float(i[1])
    return d
