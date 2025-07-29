document.addEventListener('DOMContentLoaded', function () {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    let socket;

    // Select all elements dynamically, so we don't need to hardcode IDs
    const elements = {
        cpuUsage: document.getElementById('status-cpu-usage'),
        memUsage: document.getElementById('status-mem-usage'),
        diskUsage: document.getElementById('status-disk-usage'),
        cpuTemp: document.getElementById('status-cpu-temp'),
        uptime: document.getElementById('status-uptime'),
        gpio: document.getElementById('status-gpio'),
        ioModule: document.getElementById('status-io-module'),
        sensor1: document.getElementById('status-sensor-1'),
        sensor2: document.getElementById('status-sensor-2'),
        conveyorRelay: document.getElementById('status-conveyor-relay'),
        gateRelay: document.getElementById('status-gate-relay')
    };

    function connect() {
        socket = new WebSocket(wsUrl);
        socket.onopen = () => console.log('Status page WebSocket connected.');
        socket.onclose = () => setTimeout(connect, 2000);
        socket.onerror = (err) => {
            console.error('WebSocket error on status page.', err);
            socket.close();
        };
        socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            if (message.type === 'system_status') {
                updateStatus(message.data);
            }
        };
    }

    function updateStatusBadge(element, statusText, statusType) {
        if (!element) return;
        element.textContent = statusText.toUpperCase();
        element.className = 'badge'; // Reset classes
        switch (String(statusType).toLowerCase()) {
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
    
    function updateTriggerBadge(element, isTriggered) {
        if (!element) return;
        element.textContent = isTriggered ? 'TRIGGERED' : 'CLEAR';
        element.className = 'badge';
        element.classList.add(isTriggered ? 'bg-danger' : 'bg-success');
    }

    function formatUptime(seconds) {
        const d = Math.floor(seconds / (3600*24));
        const h = Math.floor(seconds % (3600*24) / 3600);
        const m = Math.floor(seconds % 3600 / 60);
        const s = Math.floor(seconds % 60);
        return `${d}d ${h}h ${m}m ${s}s`;
    }

    function updateStatus(data) {
        if(elements.cpuUsage) elements.cpuUsage.textContent = `${data.cpu_usage.toFixed(1)} %`;
        if(elements.memUsage) elements.memUsage.textContent = `${data.memory_usage.toFixed(1)} %`;
        if(elements.diskUsage) elements.diskUsage.textContent = `${data.disk_usage.toFixed(1)} %`;
        if(elements.cpuTemp) elements.cpuTemp.textContent = data.cpu_temperature ? `${data.cpu_temperature.toFixed(1)} °C` : 'N/A';
        if(elements.uptime) elements.uptime.textContent = formatUptime(data.uptime_seconds);
        
        // --- THE FIX: Loop over the camera_statuses dictionary ---
        if (data.camera_statuses) {
            for (const [cam_id, status] of Object.entries(data.camera_statuses)) {
                // Find the specific camera element using its data attribute
                const camElement = document.querySelector(`[data-camera-id="${cam_id}"]`);
                if (camElement) {
                    updateStatusBadge(camElement, status, status);
                }
            }
        }
        
        updateStatusBadge(elements.gpio, data.gpio_status, data.gpio_status);
        updateStatusBadge(elements.ioModule, data.io_module_status, data.io_module_status);
        
        updateTriggerBadge(elements.sensor1, data.sensor_1_status);
        updateTriggerBadge(elements.sensor2, data.sensor_2_status);

        updateTriggerBadge(elements.conveyorRelay, data.conveyor_relay_status);
        updateTriggerBadge(elements.gateRelay, data.gate_relay_status);
    }

    connect();
});