// Thanks Qwen
document.addEventListener('DOMContentLoaded', function() {
    const mapElement = document.getElementById('map');
    const shipsTableBody = document.querySelector('#ships-table tbody');
    const vesselCountElement = document.getElementById('vessel-count');
    const searchBox = document.getElementById('search-box');
    const searchBtn = document.getElementById('search-btn');
    const zoomAllBtn = document.getElementById('zoom-all-btn');
    const exportBtn = document.getElementById('export-btn');
    const sortBySelect = document.getElementById('sort-by');
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');
    const pageInfoElement = document.getElementById('page-info');
    const lastRefreshElement = document.getElementById('last-refresh');
    const loadingOverlay = document.getElementById('loading');
    
    // Initialize map
    const map = L.map(mapElement).setView([20, 0], 2);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    let allShips = [];
    let filteredShips = [];
    let currentPage = 1;
    const itemsPerPage = 15;
    
    async function fetchShipData() {
        try {
            loadingOverlay.classList.remove('hidden');
            const response = await fetch('/api/ships/last24h');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            allShips = await response.json();
            lastRefreshElement.textContent = new Date().toLocaleTimeString();
            processShipData();
        } catch (error) {
            console.error('Error fetching ship ', error);
            alert('Failed to load ship data. Please try refreshing.');
        } finally {
            loadingOverlay.classList.add('hidden');
        }
    }
    
    function processShipData() {
        // Clear existing markers
        map.eachLayer(layer => {
            if (layer instanceof L.Marker) {
                map.removeLayer(layer);
            }
        });
        
        const searchTerm = searchBox.value.toLowerCase();
        filteredShips = allShips.filter(ship => 
            ship.mmsi.toString().includes(searchTerm) || 
            (ship.name && ship.name.toLowerCase().includes(searchTerm))
        );
        
        vesselCountElement.textContent = `${filteredShips.length} vessels`;
        
        // Add markers to map
        filteredShips.forEach(ship => {
            if (ship.lat && ship.lng) {
                const marker = L.marker([ship.lat, ship.lng], {
                    icon: createShipIcon(ship.course || 0, 18, ship.shiptype)
                });
                
                const popupContent = `
                    <b>${ship.name || 'Unknown Vessel'}</b><br>
                    MMSI: ${ship.mmsi}<br>
                    Type: ${ship.shiptype}<br>
                    Position: ${formatCoordinates(ship.lat, ship.lng)}<br>
                    Last Update: ${formatTimestamp(ship.timestamp)}<br>
                    Speed: ${ship.speed ? ship.speed.toFixed(1) : 'N/A'} knots<br>
                    Course: ${ship.course ? ship.course.toFixed(0) : 'N/A'}°<br>
                    <a href="/recent/${ship.mmsi}" style="
                        display: inline-block;
                        margin-top: 8px; 
                        padding: 4px 8px; 
                        background: #3182ce; 
                        color: white; 
                        border-radius: 3px; 
                        text-decoration: none;
                    ">View History</a>
                `;
                
                marker.bindPopup(popupContent);
                marker.addTo(map);
            }
        });
        
        renderTablePage();
        
        if (filteredShips.length > 0) {
            const group = L.featureGroup(filteredShips
                .filter(ship => ship.lat && ship.lng)
                .map(ship => L.marker([ship.lat, ship.lng])));
            map.fitBounds(group.getBounds().pad(0.1));
        }
    }
    
    function renderTablePage() {
        shipsTableBody.innerHTML = '';
        
        const totalPages = Math.ceil(filteredShips.length / itemsPerPage);
        currentPage = Math.max(1, Math.min(currentPage, totalPages || 1));
        
        prevPageBtn.disabled = currentPage === 1;
        nextPageBtn.disabled = currentPage === totalPages || totalPages === 0;
        pageInfoElement.textContent = `Page ${currentPage} of ${totalPages || 1}`;
        
        const startIndex = (currentPage - 1) * itemsPerPage;
        const pageShips = filteredShips.slice(startIndex, startIndex + itemsPerPage);
        
        pageShips.forEach(ship => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td class="mmsi clickable" data-mmsi="${ship.mmsi}">${ship.mmsi}</td>
                <td class="ship-name clickable" data-mmsi="${ship.mmsi}">${ship.name || 'Unknown'}</td>
                <td class="shiptype">${ship.shiptype || 'N/A'}</td>
                <td class="position">${ship.lat ? formatCoordinates(ship.lat, ship.lng) : 'N/A'}</td>
                <td class="timestamp">${ship.timestamp ? formatTimestamp(ship.timestamp) : 'N/A'}</td>
                <td>${ship.speed ? ship.speed.toFixed(1) : 'N/A'}</td>
                <td>${ship.course ? ship.course.toFixed(0) : 'N/A'}°</td>
                <td>
                    <a href="/recent/${ship.mmsi}" class="action-link">History</a>
                </td>
            `;
            shipsTableBody.appendChild(row);
        });
        
        // Add click event listeners to clickable cells
        document.querySelectorAll('.clickable').forEach(cell => {
            cell.addEventListener('click', function() {
                const mmsi = this.getAttribute('data-mmsi');
                window.location.href = `/history/${mmsi}`;
            });
        });
    }
    
    // Event Listeners
    searchBtn.addEventListener('click', processShipData);
    searchBox.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') processShipData();
    });
    
    zoomAllBtn.addEventListener('click', () => {
        if (filteredShips.length > 0) {
            const group = L.featureGroup(filteredShips
                .filter(ship => ship.lat && ship.lng)
                .map(ship => L.marker([ship.lat, ship.lng])));
            map.fitBounds(group.getBounds().pad(0.1));
        }
    });
    
    sortBySelect.addEventListener('change', (e) => {
        const sortBy = e.target.value;
        filteredShips.sort((a, b) => {
            switch(sortBy) {
                case 'time':
                    return (b.timestamp || 0) - (a.timestamp || 0);
                case 'mmsi':
                    return a.mmsi - b.mmsi;
                case 'name':
                    return (a.name || '').localeCompare(b.name || '');
                default:
                    return 0;
            }
        });
        renderTablePage();
    });
    
    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            renderTablePage();
        }
    });
    
    nextPageBtn.addEventListener('click', () => {
        const totalPages = Math.ceil(filteredShips.length / itemsPerPage);
        if (currentPage < totalPages) {
            currentPage++;
            renderTablePage();
        }
    });
    
    exportBtn.addEventListener('click', () => {
        if (filteredShips.length === 0) {
            alert('No data to export');
            return;
        }
        
        const headers = ['MMSI', 'Ship Name', 'Latitude', 'Longitude', 'Timestamp', 'Speed', 'Course'];
        const rows = filteredShips.map(ship => [
            ship.mmsi,
            ship.name || '',
            ship.lat ? ship.lat.toFixed(6) : '',
            ship.lng ? ship.lng.toFixed(6) : '',
            ship.timestamp || '',
            ship.speed ? ship.speed.toFixed(1) : '',
            ship.course ? ship.course.toFixed(1) : ''
        ]);
        
        let csvContent = 'text/csv;charset=utf-8,';
        csvContent += headers.join(',') + '\n';
        csvContent += rows.map(row => row.join(',')).join('\n');
        
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement('a');
        link.setAttribute('href', encodedUri);
        link.setAttribute('download', `ships_${new Date().toISOString().slice(0,10)}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });
    
    // Setup common elements
    setupRefreshButton();
    
    // Initialize
    fetchShipData();
    
    // Auto-refresh every 5 minutes
    setInterval(fetchShipData, 300000);
});