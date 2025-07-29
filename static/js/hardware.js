document.addEventListener('DOMContentLoaded', function () {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    let socket;

    const elements = {
        conveyor: document.getElementById('hw-conveyor-relay'),
        gate: document.getElementById('hw-gate-relay'),
        led_green: document.getElementById('hw-led-green'),
        led_red: document.getElementById('hw-led-red'),
        buzzer: document.getElementById('hw-buzzer'),
    };
    
    const toggleButtons = document.querySelectorAll('.btn-toggle-pin');

    function connect() {
        socket = new WebSocket(wsUrl);
        socket.onopen = () => console.log('Hardware page WebSocket connected.');
        socket.onclose = () => {
            console.log('Hardware page WebSocket disconnected. Reconnecting in 2 seconds...');
            setTimeout(connect, 2000);
        };
        socket.onerror = (err) => {
            console.error('WebSocket error on hardware page.', err);
            socket.close();
        };

        socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === 'system_status') {
                updatePinStatus(message.data);
            }
        };
    }

    function updatePinBadge(element, isOn) {
        if (!element) return;
        element.textContent = isOn ? 'ON' : 'OFF';
        element.className = 'badge';
        element.classList.add(isOn ? 'bg-success' : 'bg-secondary');
    }

    function updatePinStatus(data) {
        updatePinBadge(elements.conveyor, data.conveyor_relay_status);
        updatePinBadge(elements.gate, data.gate_relay_status);
        updatePinBadge(elements.led_green, data.led_green_status);
        updatePinBadge(elements.led_red, data.led_red_status);
        updatePinBadge(elements.buzzer, data.buzzer_status);
    }

    async function togglePin(pinName) {
        try {
            const response = await fetch(`/api/v1/gpio/pin/${pinName}/toggle`, {
                method: 'POST'
            });
            if (!response.ok) {
                console.error(`Failed to toggle pin ${pinName}`, await response.json());
            }
        } catch (error) {
            console.error(`Error toggling pin ${pinName}:`, error);
        }
    }

    toggleButtons.forEach(button => {
        button.addEventListener('click', () => {
            const pinName = button.getAttribute('data-pin-name');
            if (pinName) {
                togglePin(pinName);
            }
        });
    });

    connect();
});