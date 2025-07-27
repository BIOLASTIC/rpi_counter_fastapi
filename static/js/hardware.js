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
        // Module Status
        updateStatusBadge('hw-camera', status.camera_status);
        updateStatusBadge('hw-gpio', status.gpio_status);
        updateStatusBadge('hw-io-module', status.io_module_status);
        
        // Sensor Status
        updateStatusBadge('hw-sensor-1', status.sensor_1_status ? 'TRIGGERED' : 'CLEARED');
        updateStatusBadge('hw-sensor-2', status.sensor_2_status ? 'TRIGGERED' : 'CLEARED');
        
        // Relay Status
        updateStatusBadge('hw-conveyor-relay', status.conveyor_relay_status);
        updateStatusBadge('hw-gate-relay', status.gate_relay_status ? 'ON' : 'OFF');
    }
    
    function updateStatusBadge(id, status) {
        const el = document.getElementById(id);
        if (!el) return;

        const statusText = status.toString().toUpperCase().replace("_", " ");
        el.textContent = statusText;
        el.className = 'badge';
        
        const successStates = ['connected', 'ok', 'CLEARED', 'OFF'];
        const activeStates = ['ON', 'TRIGGERED'];
        
        if (successStates.includes(statusText)) el.classList.add('bg-success');
        else if (activeStates.includes(statusText)) el.classList.add('bg-warning', 'text-dark');
        else el.classList.add('bg-danger');
    }

    connect();
});
