document.addEventListener('DOMContentLoaded', function() {
    const shipsTableBody = document.getElementById('ships-tbody');
    const searchBox = document.getElementById('search-box');
    const searchBtn = document.getElementById('search-btn');
    const refreshBtn = document.getElementById('refresh-btn');
    const exportBtn = document.getElementById('export-btn');
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');
    const pageInfoElement = document.getElementById('page-info');
    const totalShipsElement = document.getElementById('total-ships');
    const lastRefreshElement = document.getElementById('last-refresh');
    const loadingOverlay = document.getElementById('loading');
    
    let currentPage = 1;
    const itemsPerPage = 20; // N parameter in your function
    let allShips = []; // Store all ships for export
    
    async function fetchShips(offset = 0) {
        try {
            loadingOverlay.classList.remove('hidden');
            const response = await fetch(`/api/ships/page/${offset}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error fetching ships:', error);
            alert('Failed to load ship data. Please try refreshing.');
            return { ships: [], total: 0 };
        } finally {
            loadingOverlay.classList.add('hidden');
        }
    }
    
    async function loadShips(page = 1) {
        const offset = (page - 1) * itemsPerPage;
        const result = await fetchShips(offset);
        
        const ships = result.ships || [];
        const totalShips = result.total || 0;
        
        // Store all ships for export functionality
        allShips = ships;
        
        // Update the table with new data
        renderTable(ships);
        
        // Update pagination
        const totalPages = Math.ceil(totalShips / itemsPerPage);
        currentPage = Math.max(1, Math.min(page, totalPages || 1));
        
        prevPageBtn.disabled = currentPage === 1;
        nextPageBtn.disabled = currentPage === totalPages || totalPages === 0;
        pageInfoElement.textContent = `Page ${currentPage} of ${totalPages || 1}`;
        
        totalShipsElement.textContent = `Total: ${totalShips} ships`;
        lastRefreshElement.textContent = new Date().toLocaleTimeString();
    }
    
    function renderTable(ships) {
        shipsTableBody.innerHTML = '';
        
        ships.forEach(ship => {
            // Determine row color based on ship type using the existing createShipIcon logic
            let shipColor;
            if (ship.type === "Tug") {
                shipColor = "#16b22eff";
            } else if (ship.type === "Military" || ship.type === "SAR") {
                shipColor = "#eb2525ff";
            } else {
                shipColor = "#2563eb";
            }
            
            const row = document.createElement('tr');
            row.innerHTML = `
                <td style="color: ${shipColor}; font-weight: bold;">${ship.mmsi}</td>
                <td class="ship-name">${ship['name*'] || ship.name || 'Unknown'}</td>
                <td>${ship.country || 'Unknown'}</td>
                <td>${ship.type || 'Unknown'}</td>
                <td class="action-btn-cell">
                    <a href="/history/${ship.mmsi}" class="view-history-btn">View History</a>
                </td>
            `;
            shipsTableBody.appendChild(row);
        });
    }
    
    // Event Listeners
    searchBtn.addEventListener('click', () => {
        // No filtering - just clear the search box
        searchBox.value = '';
    });
    
    searchBox.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            // No filtering - just clear the search box
            searchBox.value = '';
        }
    });
    
    refreshBtn.addEventListener('click', () => {
        loadShips(currentPage);
    });
    
    prevPageBtn.addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            loadShips(currentPage);
        }
    });
    
    nextPageBtn.addEventListener('click', () => {
        // Calculate total pages again to ensure we have the correct value
        fetchShips(0).then(result => {
            const totalPages = Math.ceil(result.total / itemsPerPage);
            if (currentPage < totalPages) {
                currentPage++;
                loadShips(currentPage);
            }
        });
    });
    
    exportBtn.addEventListener('click', () => {
        if (allShips.length === 0) {
            alert('No data to export');
            return;
        }
        
        const headers = ['MMSI', 'Name', 'Country', 'Type'];
        const rows = allShips.map(ship => [
            ship.mmsi,
            ship['name*'] || ship.name || '',
            ship.country || '',
            ship.type || ''
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
    loadShips(currentPage);
});