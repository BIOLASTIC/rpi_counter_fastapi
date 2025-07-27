document.addEventListener('DOMContentLoaded', function () {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
    let socket;

    function connect() {
        socket = new WebSocket(wsUrl);

        socket.onopen = () => console.log("WebSocket connection established.");
        socket.onclose = () => {
            console.log("WebSocket connection closed. Reconnecting in 3 seconds...");
            setTimeout(connect, 3000);
        };
        socket.onerror = (error) => console.error("WebSocket error:", error);
        socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            handleWebSocketMessage(message);
        };
    }

    function handleWebSocketMessage(msg) {
        if (msg.type === 'detection_status') {
            updateElement('box-count', msg.data.count);
            updateElement('detection-state', msg.data.state);
        } else if (msg.type === 'system_status') {
            updateElement('cpu-usage', `${msg.data.cpu_usage.toFixed(1)}%`);
            updateElement('mem-usage', `${msg.data.memory_usage.toFixed(1)}%`);
            updateElement('cpu-temp', `${msg.data.cpu_temperature.toFixed(1)}°C`);
            updateStatusBadge('camera-status', msg.data.camera_status);
            updateStatusBadge('conveyor-status', msg.data.conveyor_running ? 'RUNNING' : 'STOPPED');
        }
    }

    function updateElement(id, text) {
        const el = document.getElementById(id);
        if (el && el.innerText !== text) {
            el.innerText = text;
        }
    }
    
    function updateStatusBadge(id, status) {
        const el = document.getElementById(id);
        if (!el) return;

        el.textContent = status.toUpperCase();
        el.className = 'badge'; // Reset classes
        if (status === 'connected' || status === 'RUNNING') {
            el.classList.add('bg-success');
        } else if (status === 'disconnected' || status === 'STOPPED') {
            el.classList.add('bg-secondary');
        } else {
            el.classList.add('bg-danger');
        }
    }
    
    // --- API Interactions ---
    const sendApiRequest = async (url, method = 'POST') => {
        try {
            const response = await fetch(url, { method });
            if (!response.ok) {
                console.error(`API request failed: ${response.statusText}`);
            }
        } catch (error) {
            console.error('Failed to send API request:', error);
        }
    };
    
    document.getElementById('reset-button')?.addEventListener('click', () => sendApiRequest('/api/v1/detection/reset'));
    document.getElementById('conveyor-start-btn')?.addEventListener('click', () => sendApiRequest('/api/v1/gpio/conveyor/start'));
    document.getElementById('conveyor-stop-btn')?.addEventListener('click', () => sendApiRequest('/api/v1/gpio/conveyor/stop'));
    document.getElementById('emergency-stop-btn')?.addEventListener('click', () => sendApiRequest('/api/v1/system/emergency-stop'));

    // Initial connection
    connect();
});
