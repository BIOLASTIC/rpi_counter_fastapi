/**
 * Handles user interactions on the Hardware control page.
 *
 * FINAL REVISION: This script is updated to use the new Modbus-based API endpoint
 * for toggling hardware outputs.
 * - The fetch URL is changed from '/api/v1/gpio/pin/...' to '/api/v1/outputs/toggle/...'.
 * - All other features, including real-time status updates via WebSocket, are preserved.
 */
document.addEventListener('DOMContentLoaded', function () {
    const ws = new WebSocket(`ws://${window.location.host}/ws`);

    // MODIFIED: Target the new API endpoint for toggling outputs.
    // The `data-pin-name` attribute still works perfectly for identifying the device.
    const toggleButtons = document.querySelectorAll('.btn-toggle-pin');
    toggleButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const outputName = button.getAttribute('data-pin-name');
            try {
                // The only change needed is this URL.
                const response = await fetch(`/api/v1/outputs/toggle/${outputName}`, { method: 'POST' });
                if (!response.ok) {
                    const errorData = await response.json();
                    alert(`Error toggling ${outputName}: ${errorData.detail || 'Unknown error'}`);
                }
                // The UI will update automatically via the WebSocket broadcast.
            } catch (error) {
                console.error('Failed to toggle output:', error);
                alert('An error occurred. Is the server running? Check the console for details.');
            }
        });
    });

    /**
     * Updates a badge element with an ON/OFF state and color.
     * FEATURE PRESERVED.
     */
    function updateBadge(element, isActive) {
        if (!element) return;
        element.textContent = isActive ? 'ON' : 'OFF';
        element.className = 'badge'; // Reset classes
        element.classList.add(isActive ? 'bg-success' : 'bg-danger');
    }

    /**
     * Handles incoming WebSocket messages to update the UI in real-time.
     * FEATURE PRESERVED. The payload keys were kept consistent in the backend.
     */
    ws.onmessage = function (event) {
        try {
            const message = JSON.parse(event.data);
            if (message.type === 'system_status') {
                const data = message.data;
                // Update badges based on the new status payload keys from system_service
                updateBadge(document.getElementById('hw-conveyor-relay'), data.conveyor_relay_status);
                updateBadge(document.getElementById('hw-gate-relay'), data.gate_relay_status);
                updateBadge(document.getElementById('hw-led-green'), data.led_green_status);
                updateBadge(document.getElementById('hw-led-red'), data.led_red_status);
                updateBadge(document.getElementById('hw-buzzer'), data.buzzer_status);
            }
        } catch (error) {
            console.error("Error processing WebSocket message:", error);
        }
    };

    ws.onopen = function() {
        console.log("Hardware page WebSocket connection established.");
    };

    ws.onclose = function () {
        console.log('WebSocket connection closed.');
        // Optionally, show a "disconnected" message to the user
        document.querySelectorAll('.btn-toggle-pin').forEach(btn => btn.disabled = true);
        alert('Real-time connection to server lost. Please refresh the page.');
    };

    ws.onerror = function (error) {
        console.error('WebSocket error:', error);
    };
});