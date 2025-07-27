document.addEventListener('DOMContentLoaded', function () {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
    let socket;

    function connect() {
        socket = new WebSocket(wsUrl);
        socket.onopen = () => console.log("Status Page: WebSocket connection established.");
        socket.onclose = () => { setTimeout(connect, 3000); };
        socket.onerror = (error) => console.error("WebSocket error:", error);
        socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === 'system_status') {
                updateStatusDisplay(message.data);
            }
        };
    }

    function updateStatusDisplay(status) {
        // System Health
        updateElement('status-cpu-usage', `${status.cpu_usage.toFixed(1)} %`);
        updateElement('status-mem-usage', `${status.memory_usage.toFixed(1)} %`);
        updateElement('status-disk-usage', `${status.disk_usage.toFixed(1)} %`);
        updateElement('status-cpu-temp', `${status.cpu_temperature.toFixed(1)} °C`);
        updateElement('status-uptime', formatUptime(status.uptime_seconds));

        // FIX APPLIED HERE: Update all hardware modules
        updateStatusBadge('status-camera', status.camera_status);
        updateStatusBadge('status-gpio', status.gpio_status);
        updateStatusBadge('status-io-module', status.io_module_status);
        
        // Handle boolean states for sensors and relays
        const sensor1Text = status.sensor_1_status ? 'TRIGGERED' : 'CLEARED';
        const sensor2Text = status.sensor_2_status ? 'TRIGGERED' : 'CLEARED';
        const gateRelayText = status.gate_relay_status ? 'ON' : 'OFF';

        updateStatusBadge('status-sensor-1', sensor1Text);
        updateStatusBadge('status-sensor-2', sensor2Text);
        updateStatusBadge('status-conveyor-relay', status.conveyor_relay_status);
        updateStatusBadge('status-gate-relay', gateRelayText);
    }

    function updateElement(id, text) {
        const el = document.getElementById(id);
        if (el && el.innerText !== text) el.innerText = text;
    }
    
    function updateStatusBadge(id, status) {
        const el = document.getElementById(id);
        if (!el) return;

        const statusText = status.toString().toUpperCase().replace("_", " ");
        el.textContent = statusText;
        el.className = 'badge'; // Reset classes
        
        const successStates = ['connected', 'ok', 'CLEARED', 'OFF', 'open'];
        const warningStates = ['moving', 'degraded'];
        const dangerStates = ['disconnected', 'error', 'TRIGGERED', 'ON', 'closed'];

        if (successStates.includes(statusText)) el.classList.add('bg-success');
        else if (warningStates.includes(statusText)) el.classList.add('bg-warning', 'text-dark');
        else if (dangerStates.includes(statusText)) el.classList.add('bg-danger');
        else el.classList.add('bg-secondary');
    }

    function formatUptime(seconds) {
        const d = Math.floor(seconds / (3600*24));
        const h = Math.floor(seconds % (3600*24) / 3600);
        const m = Math.floor(seconds % 3600 / 60);
        let parts = [];
        if (d > 0) parts.push(d + "d");
        if (h > 0) parts.push(h + "h");
        if (m > 0) parts.push(m + "m");
        if (parts.length === 0) return (seconds % 60) + 's';
        return parts.join(' ');
    }

    connect();
});
