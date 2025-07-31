document.addEventListener('DOMContentLoaded', () => {
    // --- WebSocket Setup ---
    const WEBSOCKET_URL = `ws://${window.location.host}/ws`;
    let socket;

    function connect() {
        socket = new WebSocket(WEBSOCKET_URL);
        socket.onopen = () => console.log('WebSocket connection established.');
        socket.onmessage = handleWebSocketMessage;
        socket.onclose = () => {
            console.log('WebSocket connection closed. Reconnecting...');
            setTimeout(connect, 2000);
        };
        socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            socket.close();
        };
    }

    // --- DOM Element Cache ---
    const elements = {
        // Run Status
        systemMode: document.getElementById('system-mode'),
        activeProfileDisplay: document.getElementById('active-profile-display'),
        conveyorBelt: document.getElementById('conveyor-belt'),
        // Counts & Progress
        countExited: document.getElementById('count-exited'),
        progressCirclePath: document.querySelector('.progress-circle__path'),
        progressPercentage: document.getElementById('progress-percentage'),
        progressDetails: document.getElementById('progress-details'),
        // Controls
        profileSelect: document.getElementById('object-profile-select'),
        startRunBtn: document.getElementById('start-run-btn'),
        stopRunBtn: document.getElementById('stop-run-btn'),
        resetAllBtn: document.getElementById('reset-all-btn'),
        // Dynamic Elements
        cameraFeeds: {},
        cameraOfflineOverlays: {},
        cameraStatusBadges: {},
        // Hardware Status Grid
        statusSensor1: document.getElementById('status-sensor-1'),
        statusSensor2: document.getElementById('status-sensor-2'),
        statusConveyorRelay: document.getElementById('status-conveyor-relay'),
        statusGateRelay: document.getElementById('status-gate-relay'),
        statusDiverterRelay: document.getElementById('status-diverter-relay'),
        statusGpio: document.getElementById('status-gpio'),
        statusIoModule: document.getElementById('status-io-module'),
    };
    
    // Dynamically cache camera elements
    document.querySelectorAll('[id^="live-camera-feed-"]').forEach(el => {
        const camId = el.id.replace('live-camera-feed-', '');
        elements.cameraFeeds[camId] = el;
        elements.cameraOfflineOverlays[camId] = document.getElementById(`camera-offline-overlay-${camId}`);
        elements.cameraStatusBadges[camId] = document.querySelector(`#system-status-zone [id="status-camera-${camId}"]`);
    });

    // --- WebSocket Message Handlers ---

    function handleWebSocketMessage(event) {
        try {
            const message = JSON.parse(event.data);
            if (message.type === 'system_status') {
                handleSystemStatus(message.data);
            } else if (message.type === 'orchestration_status') {
                handleOrchestrationStatus(message.data);
            }
        } catch (error) {
            console.error("Error parsing WebSocket message:", error);
        }
    }

    function handleOrchestrationStatus(data) {
        if (!data) return;
        const { mode, active_profile, run_progress } = data;

        updateBadge(elements.systemMode, mode);
        elements.activeProfileDisplay.textContent = active_profile || 'None';
        elements.countExited.textContent = run_progress || 0;

        const isRunning = mode === 'Running';
        elements.conveyorBelt.classList.toggle('running', isRunning);
        elements.startRunBtn.disabled = isRunning;
        elements.profileSelect.disabled = isRunning;

        // Update progress circle
        const circumference = 2 * Math.PI * 45;
        elements.progressCirclePath.style.strokeDasharray = circumference;
        if (isRunning) {
            elements.progressCirclePath.style.strokeDashoffset = 0;
            elements.progressPercentage.textContent = '100%';
            elements.progressDetails.textContent = 'RUNNING';
        } else {
            elements.progressCirclePath.style.strokeDashoffset = circumference;
            elements.progressPercentage.textContent = '0%';
            elements.progressDetails.textContent = mode.toUpperCase();
        }
    }

    function handleSystemStatus(data) {
        if (!data) return;
        updateBadge(elements.statusSensor1, data.sensor_1_status ? 'TRIGGERED' : 'CLEAR', { true: 'warn', false: 'clear' });
        updateBadge(elements.statusSensor2, data.sensor_2_status ? 'TRIGGERED' : 'CLEAR', { true: 'warn', false: 'clear' });
        updateBadge(elements.statusConveyorRelay, data.conveyor_relay_status ? 'ON' : 'OFF', { true: 'on', false: 'off' });
        updateBadge(elements.statusGateRelay, data.gate_relay_status ? 'ON' : 'OFF', { true: 'on', false: 'off' });
        updateBadge(elements.statusDiverterRelay, data.diverter_relay_status ? 'ON' : 'OFF', { true: 'on', false: 'off' });
        updateBadge(elements.statusGpio, data.gpio_status, { 'ok': 'ok' });
        updateBadge(elements.statusIoModule, data.io_module_status, { 'connected': 'ok' });

        for (const camId in data.camera_statuses) {
            const status = data.camera_statuses[camId];
            const isConnected = status === 'connected';

            updateBadge(elements.cameraStatusBadges[camId], status, { 'connected': 'ok' });

            if (elements.cameraFeeds[camId]) {
                const expectedSrc = isConnected ? `/api/v1/camera/stream/${camId}` : '/static/images/placeholder.jpg';
                if (!elements.cameraFeeds[camId].src.includes(expectedSrc)) {
                    elements.cameraFeeds[camId].src = expectedSrc;
                }
            }
            if (elements.cameraOfflineOverlays[camId]) {
                elements.cameraOfflineOverlays[camId].classList.toggle('hidden', isConnected);
            }
        }
    }

    // --- UI Helper Functions ---
    const statusClassMap = {
        'ok': 'ok', 'on': 'ok', 'connected': 'ok',
        'error': 'error', 'off': 'error', 'disconnected': 'error',
        'warn': 'warn', 'triggered': 'warn', 'clear': 'clear',
    };

    function updateBadge(element, text, classLogic = {}) {
        if (!element) return;
        const textContent = (text === true ? 'ON' : (text === false ? 'OFF' : text || '--')).toUpperCase();
        element.textContent = textContent;
        
        let statusClass = 'clear';
        if (classLogic[text]) {
            statusClass = classLogic[text];
        } else if (statusClassMap[textContent.toLowerCase()]) {
            statusClass = statusClassMap[textContent.toLowerCase()];
        }
        
        element.className = 'status-badge'; // Reset classes
        element.classList.add(statusClass);
    }
    

    // --- API Call Functions ---
    async function apiPost(url, body = null) {
        try {
            const options = { method: 'POST' };
            if (body) {
                options.headers = { 'Content-Type': 'application/json' };
                options.body = JSON.stringify(body);
            }
            const response = await fetch(url, options);
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || response.statusText);
            }
            return await response.json();
        } catch (error) {
            console.error(`Error with POST request to ${url}:`, error);
            alert(`Error: ${error.message}`);
            return null;
        }
    }

    async function setProfileAndStartRun() {
        const profileId = elements.profileSelect.value;
        if (!profileId) {
            alert('Please select an object profile (recipe) first.');
            return;
        }
        const setResult = await apiPost('/api/v1/orchestration/run/set-profile', { object_profile_id: parseInt(profileId) });
        if (setResult) {
            await new Promise(resolve => setTimeout(resolve, 250));
            await apiPost('/api/v1/orchestration/run/start');
        }
    }

    async function stopRun() {
        await apiPost('/api/v1/orchestration/run/stop');
    }
    
    async function resetAllState() {
        if (confirm('Are you sure you want to stop the run and reset all system state?')) {
            await apiPost('/api/v1/system/reset-all');
        }
    }
    
    // --- Attach Event Listeners ---
    elements.startRunBtn?.addEventListener('click', setProfileAndStartRun);
    elements.stopRunBtn?.addEventListener('click', stopRun);
    elements.resetAllBtn?.addEventListener('click', resetAllState);

    // --- Initial Connection ---
    connect();
});