import io
import numpy as np
import matplotlib.pyplot as plt
from starlette.responses import StreamingResponse


async def get_plot():
    # Пример данных
    coordinates = [(1, 2), (2, 3), (3, 5), (4, 7), (5, 11)]
    # Разделяем на X и Y
    x, y = zip(*coordinates)
    x, y = np.array(x), np.array(y)
    # Создаем график
    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title('Линия по координатам')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.grid(True)
    # Сохраняем график в буфер
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)  # Перемещаем курсор в начало файла
    # Возвращаем изображение как ответ
    return StreamingResponse(img, media_type="image/png")
