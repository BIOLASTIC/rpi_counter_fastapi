document.addEventListener('DOMContentLoaded', function () {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
    let socket;

    function connect() {
        socket = new WebSocket(wsUrl);
        socket.onopen = () => console.log("Hardware Page: WebSocket connected.");
        socket.onclose = () => { setTimeout(connect, 3000); };
        socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === 'system_status') {
                updateHardwareDisplay(message.data);
            }
        };
    }

    function updateHardwareDisplay(status) {
        // --- DEFINITIVE FIX: Update all 5 GPIO devices ---
        updateStatusBadge('hw-conveyor-relay', status.conveyor_relay_status ? 'ON' : 'OFF');
        updateStatusBadge('hw-gate-relay', status.gate_relay_status ? 'ON' : 'OFF');
        updateStatusBadge('hw-led-green', status.led_green_status ? 'ON' : 'OFF');
        updateStatusBadge('hw-led-red', status.led_red_status ? 'ON' : 'OFF');
        updateStatusBadge('hw-buzzer', status.buzzer_status ? 'ON' : 'OFF');
    }
    
    function updateStatusBadge(id, statusText) {
        const el = document.getElementById(id);
        if (!el) return;
        el.textContent = statusText;
        el.className = 'badge';
        if (statusText === 'ON') el.classList.add('bg-warning', 'text-dark');
        else el.classList.add('bg-success');
    }

    // --- DEFINITIVE FIX: Generic listener for all toggle buttons ---
    document.querySelectorAll('.btn-toggle-pin').forEach(button => {
        button.addEventListener('click', async (event) => {
            const pinName = event.target.dataset.pinName;
            if (!pinName) return;
            try {
                // Use the new generic API endpoint
                await fetch(`/api/v1/gpio/pin/${pinName}/toggle`, { method: 'POST' });
            } catch (error) {
                console.error('Error sending toggle command:', error);
            }
        });
    });

    connect();
});
