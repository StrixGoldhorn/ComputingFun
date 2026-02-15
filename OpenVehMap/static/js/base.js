// Thanks Qwen
// Format epoch timestamp to human-readable string
function formatTimestamp(epochSeconds) {
    // Convert epoch seconds to JavaScript milliseconds
    const date = new Date(epochSeconds * 1000);
    return date.toLocaleString();
}

// Create simple ship icon with 5-sided shape
function createShipIcon(course = 0, size = 20, shiptype = 'aaa') {
    if (shiptype == "Tug") {
        color = "#16b22eff";
    } else if (shiptype == "Military" || shiptype == "SAR" || (shiptype != null && shiptype.includes("Law"))) {
        color = "#eb2525ff";
    } else {
        color = "#2563eb";
    }
    const halfSize = size / 2;
    return L.divIcon({
        className: 'ship-icon',
        html: `<div style="
            width: ${size}px; 
            height: ${size}px; 
            background: ${color}; 
            clip-path: polygon(50% 0%, 100% 40%, 100% 100%, 0 100%, 0 40%);
            transform: rotate(${course}deg);
        "></div>`,
        iconSize: [size, size],
        iconAnchor: [halfSize, halfSize]
    });
}

// Format coordinates to 4 decimal places
function formatCoordinates(lat, lng) {
    return `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
}

// Common refresh handling
function setupRefreshButton() {
    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', () => {
            location.reload();
        });
    }
}