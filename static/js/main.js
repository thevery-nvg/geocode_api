
async function fetchAndDisplayPlot() {
    try {
        // Отправляем GET-запрос к эндпоинту /api/plot
        const response = await fetch('/api/plot');

        // Проверяем, успешен ли ответ
        if (!response.ok) {
            throw new Error('Ошибка сети: ' + response.statusText);
        }

        // Получаем данные изображения в виде Blob
        const blob = await response.blob();

        // Создаём временный URL для Blob
        const imageUrl = URL.createObjectURL(blob);

        // Устанавливаем источник изображения на полученный URL
        const imgElement = document.getElementById('plotImage');
        imgElement.src = imageUrl;

        // Опционально: освобождаем URL после загрузки изображения
        imgElement.onload = () => {
            URL.revokeObjectURL(imageUrl);
        };

    } catch (error) {
        console.error('Ошибка при загрузке графика:', error);
        alert('Не удалось загрузить график. Проверьте консоль для деталей.');
    }
}

async function sendData() {
    const input = document.getElementById('input').value;
    const hiddenField = document.getElementById('hiddenField');
    const coordinatesList = document.getElementById('coordinatesList');

    try {
        const response = await fetch('/api/geocode_list', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ address: input }),
        });

        if (!response.ok) {
            throw new Error('Ошибка при отправке запроса');
        }

        const data = await response.json();
        displayCoordinates(data)
    } catch (error) {
        coordinatesList.textContent = 'Произошла ошибка: ' + error.message;
    }

    try {
        const response = await fetch('/api/geocode_gpx', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ address: input }),
        });

        if (!response.ok) {
            throw new Error('Ошибка при отправке запроса');
        }

        const data = await response.json();
        hiddenField.value = JSON.stringify(data, null, 2);

    } catch (error) {
        hiddenField.textContent = 'Произошла ошибка: ' + error.message;
    }

}
async function sendData_google() {
    const input = document.getElementById('input').value;
    const hiddenField = document.getElementById('hiddenField');
    const coordinatesList = document.getElementById('coordinatesList');
    const button = document.getElementById('downloadButton');
    try {
        const response = await fetch('/api/google_list', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ address: input }),
        });

        if (!response.ok) {
            throw new Error('Ошибка при отправке запроса');
        }

        const data = await response.json();
        displayCoordinates(data)
    } catch (error) {
        coordinatesList.textContent = 'Произошла ошибка: ' + error.message;
    }

    try {
        const response = await fetch('/api/google_gpx', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ address: input }),
        });

        if (!response.ok) {
            throw new Error('Ошибка при отправке запроса');
        }

        const data = await response.json();
        hiddenField.value = JSON.stringify(data, null, 2);
        button.style.backgroundColor = 'rgb(0, 150, 0)';
        console.log(hiddenField.value);
    } catch (error) {
        hiddenField.textContent = 'Произошла ошибка: ' + error.message;
    }

}

function displayCoordinates(coordinates) {
    const coordinatesList = document.getElementById('coordinatesList');
    coordinatesList.innerHTML = '';
    coordinates.forEach(coord => {
        const li = document.createElement('li');
        li.textContent = coord;
        coordinatesList.appendChild(li);
    });
}

function downloadData() {
    const button = document.getElementById('downloadButton');

    const output = document.getElementById('hiddenField').value;

    if (!output) {
        alert('Нет данных для скачивания');
        return;
    }

    const jsonData = JSON.parse(output);
    const blob = new Blob([jsonData], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'geocoding_result.gpx';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}



function call_autocad() {
    const button = document.getElementById('loadPlotBtn');
    return fetch('/api/autocad', {
        method: 'GET',
    })
    .then(response => {
        if (response.ok) {
            window.alert("Успех!");

        } else {
            window.alert("Неудача!");

        }
    })
    .catch(error => {
        console.error('Ошибка:', error);
        return 'Неудача';  // Если произошла ошибка во время запроса
    });
}
