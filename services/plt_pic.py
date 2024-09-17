from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt
from starlette.responses import StreamingResponse


def normalize(data):
    min_vals = np.min(data, axis=0)
    max_vals = np.max(data, axis=0)
    return (data - min_vals) / (max_vals - min_vals)


async def plot(s):
    coordinates = np.array(s)

    # Нормализация данных

    normalized_coordinates = normalize(coordinates)

    # Разделяем на X и Y после нормализации
    x, y = normalized_coordinates[:, 0], normalized_coordinates[:, 1]

    # Создаем график
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title('Нормализованная линия по координатам')
    plt.xlabel('Normalized X')
    plt.ylabel('Normalized Y')
    plt.grid(True)

    # Настройка осей для отображения нормализованного диапазона
    plt.xlim(-1.5, 1.5)
    plt.ylim(-1.5, 1.5)

    # Сохраняем график в буфер
    img = BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)  # Перемещаем курсор в начало файла

    # Возвращаем изображение как ответ
    return StreamingResponse(img, media_type="image/png")
