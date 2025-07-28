document.addEventListener('DOMContentLoaded', function() {
    // --- Element Cache ---
    const elements = {
        cpuUsage: document.getElementById('status-cpu-usage'),
        memUsage: document.getElementById('status-mem-usage'),
        diskUsage: document.getElementById('status-disk-usage'),
        cpuTemp: document.getElementById('status-cpu-temp'),
        uptime: document.getElementById('status-uptime'),
        camera: document.getElementById('status-camera'),
        gpio: document.getElementById('status-gpio'),
        ioModule: document.getElementById('status-io-module'),
        sensor1: document.getElementById('status-sensor-1'),
        sensor2: document.getElementById('status-sensor-2'),
        conveyorRelay: document.getElementById('status-conveyor-relay'),
        gateRelay: document.getElementById('status-gate-relay'),
    };

    // --- WebSocket Handler ---
    function connectWebSocket() {
        const socket = new WebSocket(`ws://${window.location.host}/ws`);

        socket.onmessage = function(event) {
            const message = JSON.parse(event.data);
            if (message.type === 'system_status') {
                updateStatusDisplay(message.data);
            }
        };

        socket.onclose = function() {
            console.log('WebSocket disconnected. Reconnecting in 3 seconds...');
            setAllToUnknown();
            setTimeout(connectWebSocket, 3000);
        };

        socket.onerror = function(err) {
            console.error('WebSocket error:', err);
            socket.close(); // This will trigger the onclose handler for reconnection
        };
    }

    function updateStatusDisplay(data) {
        // System Metrics
        elements.cpuUsage.textContent = `${(data.cpu_usage || 0).toFixed(1)} %`;
        elements.memUsage.textContent = `${(data.memory_usage || 0).toFixed(1)} %`;
        elements.diskUsage.textContent = `${(data.disk_usage || 0).toFixed(1)} %`;
        elements.cpuTemp.textContent = data.cpu_temperature ? `${data.cpu_temperature.toFixed(1)} °C` : '--';
        elements.uptime.textContent = formatUptime(data.uptime_seconds);

        // Module Status
        updateModuleStatus(elements.camera, data.camera_status);
        updateModuleStatus(elements.gpio, data.gpio_status);
        updateModuleStatus(elements.ioModule, data.io_module_status);
        
        // Pin/Device Status (True = ON/ACTIVE/TRIGGERED)
        updateBooleanStatus(elements.conveyorRelay, data.conveyor_relay_status, 'ON', 'OFF');
        updateBooleanStatus(elements.gateRelay, data.gate_relay_status, 'ON', 'OFF');
        updateBooleanStatus(elements.sensor1, data.sensor_1_status, 'TRIGGERED', 'CLEAR');
        updateBooleanStatus(elements.sensor2, data.sensor_2_status, 'TRIGGERED', 'CLEAR');
    }

    function updateModuleStatus(element, status) {
        if (!element) return;
        status = status || 'unknown';
        element.textContent = status.toUpperCase();
        const classMap = { 'connected': 'bg-success', 'ok': 'bg-success', 'disconnected': 'bg-warning', 'error': 'bg-danger', 'unknown': 'bg-dark' };
        updateBadgeClass(element, status, classMap);
    }

    function updateBooleanStatus(element, is_on, on_text, off_text) {
        if (!element) return;
        const text = is_on ? on_text : off_text;
        const classMap = { true: 'bg-danger', false: 'bg-secondary' };
        if (on_text === 'ON') {
             classMap.true = 'bg-success';
        }
        element.textContent = text;
        updateBadgeClass(element, is_on, classMap);
    }
    
    function updateBadgeClass(element, value, classMap) {
        if (!element) return;
        Object.values(classMap).forEach(cls => element.classList.remove(cls));
        const newClass = classMap[value];
        if (newClass) {
            element.classList.add(newClass);
        } else {
            element.classList.add('bg-dark');
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

    function formatUptime(totalSeconds) {
        if (totalSeconds === undefined) return '--';
        const days = Math.floor(totalSeconds / 86400);
        totalSeconds %= 86400;
        const hours = Math.floor(totalSeconds / 3600);
        totalSeconds %= 3600;
        const minutes = Math.floor(totalSeconds / 60);
        return `${days}d ${hours}h ${minutes}m`;
    }

    // --- Initial Kick-off ---
    connectWebSocket();
});