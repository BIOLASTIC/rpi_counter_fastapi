document.addEventListener('DOMContentLoaded', function () {
    const WEBSOCKET_URL = `ws://${window.location.host}/ws`;
    let ws;

    // --- Element Cache ---
    const elements = {
        conveyorBelt: document.getElementById('conveyor-belt'),
        countOnBelt: document.getElementById('count-on-belt'),
        countExited: document.getElementById('count-exited'),
        progressCircle: document.querySelector('.progress-circle__path'),
        progressPercentage: document.getElementById('progress-percentage'),
        progressDetails: document.getElementById('progress-details'),
        systemMode: document.getElementById('system-mode'),
        activeProfileDisplay: document.getElementById('active-profile-display'),
        startRunBtn: document.getElementById('start-run-btn'),
        stopRunBtn: document.getElementById('stop-run-btn'),
        resetAllBtn: document.getElementById('reset-all-btn'),
        objectProfileSelect: document.getElementById('object-profile-select'),
        targetCountInput: document.getElementById('target-count-input'), // NEW
    };
    const CIRCLE_CIRCUMFERENCE = 2 * Math.PI * 45;
    elements.progressCircle.style.strokeDasharray = CIRCLE_CIRCUMFERENCE;

    // --- State ---
    let lastSystemStatus = {};
    let lastOrchestrationStatus = {};

    function connectWebSocket() {
        console.log('Attempting to connect WebSocket...');
        ws = new WebSocket(WEBSOCKET_URL);

        ws.onopen = () => console.log('WebSocket connection established.');
        ws.onclose = () => {
            console.log('WebSocket connection closed. Reconnecting in 3 seconds...');
            setTimeout(connectWebSocket, 3000);
        };
        ws.onerror = (err) => console.error('WebSocket error:', err);
        ws.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                switch (message.type) {
                    case 'system_status':
                        lastSystemStatus = message.data;
                        updateSystemStatus(message.data);
                        break;
                    case 'orchestration_status':
                        lastOrchestrationStatus = message.data;
                        updateOrchestrationStatus(message.data);
                        break;
                }
            } catch (e) {
                console.error('Error parsing WebSocket message:', e);
            }
        };
    }

    // --- UI Update Functions ---
    function updateSystemStatus(data) {
        updateBadge('status-sensor-1', data.sensor_1_status, 'TRIGGERED', 'CLEAR');
        updateBadge('status-sensor-2', data.sensor_2_status, 'TRIGGERED', 'CLEAR');
        updateBadge('status-conveyor-relay', data.conveyor_relay_status, 'ON', 'OFF');
        updateBadge('status-gate-relay', data.gate_relay_status, 'ON', 'OFF');
        updateBadge('status-diverter-relay', data.diverter_relay_status, 'ON', 'OFF');
        updateBadge('status-io-module', data.io_module_status === 'ok', 'OK', 'ERROR');
        
        // --- NEW: Update in-flight count ---
        if (elements.countOnBelt) {
            elements.countOnBelt.textContent = data.in_flight_count ?? 0;
        }

        // Camera statuses
        Object.keys(data.camera_statuses || {}).forEach(camId => {
            const status = data.camera_statuses[camId];
            updateBadge(`status-camera-${camId}`, status === 'connected', 'ONLINE', 'OFFLINE');
            const overlay = document.getElementById(`camera-offline-overlay-${camId}`);
            if (overlay) overlay.classList.toggle('hidden', status === 'connected');
        });

        // Trigger conveyor animation
        const isRunning = data.conveyor_relay_status;
        elements.conveyorBelt.classList.toggle('running', isRunning);
    }
    
    function updateOrchestrationStatus(data) {
        const { mode, active_profile, run_progress, target_count } = data;

        elements.systemMode.textContent = mode;
        updateBadgeClass(elements.systemMode, mode);
        elements.activeProfileDisplay.textContent = active_profile;
        elements.countExited.textContent = run_progress;

        let percentage = 0;
        if (target_count > 0) {
            percentage = Math.min((run_progress / target_count) * 100, 100);
            elements.progressDetails.textContent = `${run_progress} / ${target_count}`;
        } else {
            // If no target, show unlimited mode
            elements.progressDetails.textContent = "Unlimited";
            percentage = 0; // Or keep it at 0 for unlimited runs
        }

        elements.progressPercentage.textContent = `${Math.round(percentage)}%`;
        const offset = CIRCLE_CIRCUMFERENCE * (1 - percentage / 100);
        elements.progressCircle.style.strokeDashoffset = offset;
    }


    function updateBadge(elementId, isPositive, positiveText, negativeText) {
        const el = document.getElementById(elementId);
        if (el) {
            const text = isPositive ? positiveText : negativeText;
            const positiveClass = positiveText.toLowerCase();
            const negativeClass = negativeText.toLowerCase();
            el.textContent = text;
            el.classList.remove('ok', 'on', 'connected', 'triggered', 'error', 'off', 'disconnected', 'clear');
            el.classList.add(isPositive ? positiveClass : negativeClass);
        }
    }

    function updateBadgeClass(element, mode) {
        element.className = 'status-badge'; // Reset
        switch (mode) {
            case 'Running':
                element.classList.add('ok'); break;
            case 'Stopped':
                element.classList.add('error'); break;
            case 'Idle (Profile Loaded)':
            case 'Complete':
                element.classList.add('warn'); break;
            default:
                element.classList.add('clear');
        }
    }


    // --- API Call Functions ---
    async function postData(url, data) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || `HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (e) {
            console.error(`Failed to POST to ${url}:`, e);
            alert(`Error: ${e.message}`);
        }
    }
    
    // --- Event Listeners ---
    elements.startRunBtn.addEventListener('click', async () => {
        const profileId = elements.objectProfileSelect.value;
        const targetCount = parseInt(elements.targetCountInput.value, 10);

        if (!profileId) {
            alert('Please select an Object Profile first.');
            return;
        }
        if (isNaN(targetCount) || targetCount < 0) {
            alert('Please enter a valid, non-negative Target Count.');
            return;
        }

        console.log(`Setting active profile to ID: ${profileId}`);
        await postData('/api/v1/orchestration/run/set-profile', { object_profile_id: parseInt(profileId) });
        
        console.log(`Starting run with target: ${targetCount}`);
        await postData('/api/v1/orchestration/run/start', { target_count: targetCount });
    });

    elements.stopRunBtn.addEventListener('click', () => {
        console.log('Stopping run...');
        postData('/api/v1/orchestration/run/stop', {});
    });

    elements.resetAllBtn.addEventListener('click', () => {
        if (confirm('Are you sure you want to stop all hardware and reset the state?')) {
            console.log('Resetting all system state...');
            postData('/api/v1/system/reset-all', {});
        }
    });

    // --- Initialization ---
    connectWebSocket();
});