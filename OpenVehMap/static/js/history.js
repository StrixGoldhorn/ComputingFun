// Thanks Qwen
document.addEventListener('DOMContentLoaded', function() {
    const pathParts = window.location.pathname.split('/');
    const mmsi = pathParts[pathParts.length - 1];
    
    const mapElement = document.getElementById('map');
    const shipsTableBody = document.querySelector('#ships-table tbody');
    const positionCount = document.getElementById('position-count');
    const loadingOverlay = document.getElementById('loading');
    
    // Initialize map
    const map = L.map(mapElement).setView([20, 0], 2);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    let shipMarker = null;
    let routeLine = null;
    let positions = [];
    
    async function fetchShipHistory() {
        try {
            const response = await fetch(`/api/history/${mmsi}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching ship history:', error);
            return [];
        }
    }
    
    function renderPositions(data) {
        if (!data || data.length === 0) {
            positionCount.textContent = 'No positions found';
            return;
        }
        
        positions = data;
        positionCount.textContent = `${data.length} positions`;
        
        if (shipMarker) map.removeLayer(shipMarker);
        if (routeLine) map.removeLayer(routeLine);
        
        const coordinates = data.map(pos => [pos.lat, pos.lng]);
        
        routeLine = L.polyline(coordinates, {
            color: '#2563eb',
            weight: 3,
            opacity: 0.8
        }).addTo(map);
        
        const lastPos = data[data.length - 1];
        shipMarker = L.marker([lastPos.lat, lastPos.lng], { 
            icon: createShipIcon(0, 20, '')
        })
        .addTo(map)
        .bindPopup(`<b>Current Position</b><br>Time: ${formatTimestamp(lastPos.timestamp)}`);
        
        const bounds = routeLine.getBounds();
        map.fitBounds(bounds.pad(0.1));
        
        shipsTableBody.innerHTML = '';
        data.slice(0, 50).forEach(pos => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="timestamp">${formatTimestamp(pos.timestamp)}</td>
                <td class="position">${formatCoordinates(pos.lat, pos.lng)}</td>
                <td>${pos.speed ? pos.speed.toFixed(1) : 'N/A'}</td>
                <td>${pos.course ? pos.course.toFixed(0) : 'N/A'}°</td>
            `;
            shipsTableBody.appendChild(row);
        });
    }
    
    async function init() {
        loadingOverlay.classList.remove('hidden');
        
        const historyData = await fetchShipHistory();
        renderPositions(historyData);
        
        loadingOverlay.classList.add('hidden');
    }
    
    // Setup common elements
    setupRefreshButton();
    
    init();
});