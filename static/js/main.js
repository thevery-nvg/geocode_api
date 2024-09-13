

async function sendData() {
        const input = document.getElementById('input').value;
        const hiddenField = document.getElementById('hiddenField');
        const output = document.getElementById('output');

        try {
            const response = await fetch('/api/geocode', {
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


            hiddenField.textContent = JSON.stringify(data.result, null, 2);
        } catch (error) {
            hiddenField.textContent = 'Произошла ошибка: ' + error.message;
        }
        try {
            const response = await fetch('/api/geocode2', {
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
            let coordinatesList = '';
            data.result.forEach(coord => {
                coordinatesList += 'Lat: ${coord.lat}, Lon: ${coord.lon}<br>';
            });
            output.innerHTML = coordinatesList;

            output.textContent = JSON.stringify(data.result, null, 2);
        } catch (error) {
            output.textContent = 'Произошла ошибка: ' + error.message;
        }
    }



    function downloadData() {
        const output = document.getElementById('hiddenField').textContent;
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
