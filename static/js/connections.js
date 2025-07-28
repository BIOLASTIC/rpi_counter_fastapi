document.addEventListener('DOMContentLoaded', function() {

    // --- Element Cache ---
    const elements = {
        conveyor: document.getElementById('conn-conveyor'),
        gate: document.getElementById('conn-gate'),
        buzzer: document.getElementById('conn-buzzer'),
        ledGreen: document.getElementById('conn-led-green'),
        ledRed: document.getElementById('conn-led-red'),
        ioModule: document.getElementById('conn-io-module'),
        camera: document.getElementById('conn-camera'),
    };

    // --- WebSocket Handler ---
    function connectWebSocket() {
        const socket = new WebSocket(`ws://${window.location.host}/ws`);

        socket.onmessage = function(event) {
            const message = JSON.parse(event.data);
            if (message.type === 'system_status') {
                updateConnectionStatus(message.data);
            }
        };

        socket.onclose = function() {
            console.log('WebSocket disconnected. Reconnecting in 3 seconds...');
            setAllToUnknown();
            setTimeout(connectWebSocket, 3000);
        };

        socket.onerror = function(err) {
            console.error('WebSocket error:', err);
            socket.close();
        };
    }

    // --- UI Update Functions ---
    function updateConnectionStatus(data) {
        // GPIO Pins
        updatePinStatus(elements.conveyor, data.conveyor_relay_status);
        updatePinStatus(elements.gate, data.gate_relay_status);
        updatePinStatus(elements.buzzer, data.buzzer_status);
        updatePinStatus(elements.ledGreen, data.led_green_status);
        updatePinStatus(elements.ledRed, data.led_red_status);
        
        // Other Modules
        updateModuleStatus(elements.ioModule, data.io_module_status);
        updateModuleStatus(elements.camera, data.camera_status);
    }
    
    function updatePinStatus(element, is_on) {
        if (!element) return;
        element.textContent = is_on ? 'ON' : 'OFF';
        updateBadgeClass(element, is_on, { true: 'bg-success', false: 'bg-secondary' });
    }
    
    function updateModuleStatus(element, status) {
        if (!element) return;
        status = status || 'unknown';
        element.textContent = status.toUpperCase();
        const classMap = {
            'connected': 'bg-success',
            'ok': 'bg-success',
            'disconnected': 'bg-warning',
            'error': 'bg-danger',
            'unknown': 'bg-dark',
        };
        updateBadgeClass(element, status, classMap);
    }

    function updateBadgeClass(element, value, classMap) {
        // Remove all possible classes first
        Object.values(classMap).forEach(cls => element.classList.remove(cls));
        // Add the correct class based on the current value
        if (classMap[value] !== undefined) {
            element.classList.add(classMap[value]);
        } else {
            element.classList.add('bg-dark'); // Default for unexpected values
        }
    }
    
    function setAllToUnknown() {
        Object.values(elements).forEach(el => {
            if (el) {
                el.textContent = 'UNKNOWN';
                updateBadgeClass(el, 'unknown', {});
            }
        });
    }

    // --- Initial Kick-off ---
    connectWebSocket();
});