document.addEventListener('DOMContentLoaded', function () {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    let socket;

    const statusElements = {
        conveyor: document.getElementById('conn-conveyor'),
        gate: document.getElementById('conn-gate'),
        buzzer: document.getElementById('conn-buzzer'),
        ledGreen: document.getElementById('conn-led-green'),
        ledRed: document.getElementById('conn-led-red'),
        ioModule: document.getElementById('conn-io-module'),
        camera: document.getElementById('conn-camera')
    };

    function connect() {
        socket = new WebSocket(wsUrl);

        socket.onopen = function() {
            console.log('WebSocket connection established for connections page.');
        };

        socket.onmessage = function(event) {
            const message = JSON.parse(event.data);
            if (message.type === 'system_status') {
                updateHardwareStatus(message.data);
            }
        };

        socket.onclose = function(e) {
            console.log('WebSocket connection closed. Reconnecting in 2 seconds...', e.reason);
            setTimeout(connect, 2000);
        };

        socket.onerror = function(err) {
            console.error('WebSocket error:', err);
            socket.close();
        };
    }

    function updateBadge(element, text, isOk, onText = 'ON', offText = 'OFF') {
        if (!element) return;
        
        let statusText = isOk ? onText : offText;
        let addClass = isOk ? 'bg-success' : 'bg-danger';
        let removeClass = isOk ? 'bg-danger' : 'bg-success';

        if (text) {
             statusText = text;
        }

        element.textContent = statusText;
        element.classList.add(addClass);
        element.classList.remove(removeClass, 'bg-warning', 'bg-secondary');
    }

    function updateConnectionBadge(element, status) {
        if (!element) return;
        
        element.textContent = status.toUpperCase();
        element.classList.remove('bg-success', 'bg-danger', 'bg-warning', 'bg-secondary');

        switch (status.toLowerCase()) {
            case 'connected':
            case 'ok':
                element.classList.add('bg-success');
                break;
            case 'disconnected':
                element.classList.add('bg-warning', 'text-dark');
                break;
            case 'error':
                element.classList.add('bg-danger');
                break;
            default:
                element.classList.add('bg-secondary');
        }
    }


    function updateHardwareStatus(data) {
        // Relays and discrete outputs
        updateBadge(statusElements.conveyor, null, data.conveyor_relay_status);
        updateBadge(statusElements.gate, null, data.gate_relay_status);
        updateBadge(statusElements.buzzer, null, data.buzzer_status);
        updateBadge(statusElements.ledGreen, null, data.led_green_status);
        updateBadge(statusElements.ledRed, null, data.led_red_status);

        // Module statuses
        updateConnectionBadge(statusElements.ioModule, data.io_module_status);
        updateConnectionBadge(statusElements.camera, data.camera_status);
    }

    connect();
});