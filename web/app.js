// Fetch data from API and update table
async function fetchData() {
    const response = await fetch('https://your-api-url.onrender.com/data');
    const data = await response.json();

    const table = document.getElementById('data-table');
    table.innerHTML = '';

    data.forEach(item => {
        const row = `
            <tr>
                <td>${item['Timestamp']}</td>
                <td>${item['Temperature (°C)']}</td>
                <td>${item['Humidity (%)']}</td>
                <td>${item['Voltage (V)']}</td>
                <td>${item['Energy Produced (Wh)']}</td>
                <td>${item['Relay State']}</td>
            </tr>
        `;
        table.innerHTML += row;
    });
}

// Refresh data every 5 seconds
setInterval(fetchData, 5000);
fetchData();
