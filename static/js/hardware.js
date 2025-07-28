document.addEventListener('DOMContentLoaded', function() {
    // --- Element Cache ---
    const pinToggleButtons = document.querySelectorAll('.btn-toggle-pin');
    const statusBadges = {
        conveyor: document.getElementById('hw-conveyor-relay'),
        gate: document.getElementById('hw-gate-relay'),
        led_green: document.getElementById('hw-led-green'),
        led_red: document.getElementById('hw-led-red'),
        buzzer: document.getElementById('hw-buzzer'),
    };

    const API_BASE = '/api/v1/gpio/pin';

    // --- WebSocket Handler ---
    function connectWebSocket() {
        const socket = new WebSocket(`ws://${window.location.host}/ws`);

        socket.onmessage = function(event) {
            const message = JSON.parse(event.data);
            if (message.type === 'system_status') {
                updateHardwareStatus(message.data);
            }
        };

        socket.onclose = function() {
            console.log('WebSocket disconnected. Reconnecting in 3 seconds...');
            setAllToUnknown();
            setTimeout(connectWebSocket, 3000);
        };
    }

    // --- UI Update Function ---
    function updateHardwareStatus(data) {
        updatePinStatus(statusBadges.conveyor, data.conveyor_relay_status);
        updatePinStatus(statusBadges.gate, data.gate_relay_status);
        updatePinStatus(statusBadges.led_green, data.led_green_status);
        updatePinStatus(statusBadges.led_red, data.led_red_status);
        updatePinStatus(statusBadges.buzzer, data.buzzer_status);
    }

    function updatePinStatus(element, is_on) {
        if (!element) return;
        element.textContent = is_on ? 'ON' : 'OFF';
        element.classList.remove('bg-success', 'bg-secondary', 'bg-dark');
        if (is_on) {
            element.classList.add('bg-success');
        } else {
            element.classList.add('bg-secondary');
        }
    }

    function setAllToUnknown() {
        Object.values(statusBadges).forEach(badge => {
            if (badge) {
                badge.textContent = 'UNKNOWN';
                badge.classList.remove('bg-success', 'bg-secondary');
                badge.classList.add('bg-dark');
            }
        });
    }
    
    // --- API Call Functions ---
    async function togglePin(pinName) {
        try {
            const response = await fetch(`${API_BASE}/${pinName}/toggle`, { method: 'POST' });
            if (!response.ok) {
                const errorData = await response.json();
                alert(`Error toggling ${pinName}: ${errorData.detail || 'Unknown error'}`);
            }
            // The UI will update automatically via the next WebSocket message.
        } catch (error) {
            alert(`Network error: ${error.message}`);
        }
    }

    // --- Event Listeners ---
    pinToggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const pinName = this.dataset.pinName;
            if (pinName) {
                togglePin(pinName);
            }
        });
    });

    // --- Initial Kick-off ---
    connectWebSocket();
});