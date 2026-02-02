// Thanks Qwen
document.addEventListener('DOMContentLoaded', function() {
    const pathParts = window.location.pathname.split('/');
    const mmsi = pathParts[pathParts.length - 1];
    
    const mapElement = document.getElementById('map');
    const shipsTableBody = document.querySelector('#ships-table tbody');
    const positionCount = document.getElementById('position-count');
    const loadingOverlay = document.getElementById('loading');
    
    // Vessel details elements
    const shipNameElement = document.getElementById('ship-name');
    const mmsiValueElement = document.getElementById('mmsi-value');
    const countryValueElement = document.getElementById('country-value');
    const typeValueElement = document.getElementById('type-value');
    
    // Initialize map
    const map = L.map(mapElement).setView([20, 0], 2);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    let shipMarker = null;
    let routeLine = null;
    let positions = [];
    let shipInfo = null;
    
    async function fetchShipHistory() {
        try {
            const response = await fetch(`/api/recent/${mmsi}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching ship history:', error);
            return [];
        }
    }
    
    async function fetchShipInfo() {
        try {
            const response = await fetch(`/api/ship/${mmsi}`);
            if (!response.ok) {
                return null;
            }
            return await response.json();
        } catch (error) {
            console.error('Error fetching ship info:', error);
            return null;
        }
    }
    
    function updateVesselDetails(info) {
        if (info) {
            shipNameElement.textContent = info.name || 'Unknown Vessel';
            mmsiValueElement.textContent = info.mmsi;
            countryValueElement.textContent = info.country || 'Unknown';
            typeValueElement.textContent = info.type || 'Unknown';
            
            // Update the ship color based on type
            const shipColor = info.type === "Tug" ? "#16b22eff" : 
                             (info.type === "Military" || info.type === "SAR") ? "#eb2525ff" : 
                             "#2563eb";
            document.querySelector('.detail-card').style.borderLeftColor = shipColor;
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
        
        // Determine ship color based on type from ship info
        const shipColor = shipInfo ? 
                         (shipInfo.type === "Tug" ? "#16b22eff" : 
                         (shipInfo.type === "Military" || shipInfo.type === "SAR") ? "#eb2525ff" : 
                         "#2563eb") : 
                         "#2563eb";
        
        const coordinates = data.map(pos => [pos.lat, pos.lng]);
        
        routeLine = L.polyline(coordinates, {
            color: shipColor,
            weight: 3,
            opacity: 0.8
        }).addTo(map);
        
        const lastPos = data[data.length - 1];
        shipMarker = L.marker([lastPos.lat, lastPos.lng], { 
            icon: createShipIcon(0, 20, shipInfo ? shipInfo.type : 'Other')
        })
        .addTo(map)
        .bindPopup(`<b>Current Position</b><br>Time: ${formatTimestamp(lastPos.timestamp)}`);
        
        const bounds = routeLine.getBounds();
        map.fitBounds(bounds.pad(0.1));
        
        shipsTableBody.innerHTML = '';
        data.forEach(pos => {
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
        
        // Fetch both history and ship info
        const [historyData, infoData] = await Promise.all([
            fetchShipHistory(),
            fetchShipInfo()
        ]);
        
        shipInfo = infoData;
        updateVesselDetails(infoData);
        renderPositions(historyData);
        
        loadingOverlay.classList.add('hidden');
    }
    
    // Setup common elements
    setupRefreshButton();
    
    init();
});