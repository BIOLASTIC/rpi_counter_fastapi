// /static/js/dashboard_v3.js

document.addEventListener('DOMContentLoaded', function () {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
    let socket;

    const appState = {
        lastSensor1State: false,
        currentMode: 'Stopped',
    };

    const DOMElements = {
        // Animation
        animationZone: document.getElementById('animation-zone'),
        conveyorBelt: document.getElementById('conveyor-belt'),
        countOnBelt: document.getElementById('count-on-belt'),
        countExited: document.getElementById('count-exited'),
        conveyorMode: document.getElementById('conveyor-mode'),

        // Run Status
        activeProfile: document.getElementById('active-profile-display'),
        progressPath: document.getElementById('progress-path'),
        progressPercentage: document.getElementById('progress-percentage'),
        progressDetails: document.getElementById('progress-details'),
        
        // Hardware Status
        statusSensor1: document.getElementById('status-sensor-1'),
        statusSensor2: document.getElementById('status-sensor-2'),
        statusIoModule: document.getElementById('status-io-module'),
        aiServiceStatus: document.getElementById('status-ai-service'),
        
        // Manual Controls
        conveyorToggle: document.getElementById('control-conveyor-toggle'),
        gateToggle: document.getElementById('control-gate-toggle'),
        diverterToggle: document.getElementById('control-diverter-toggle'),
        cameraLightToggle: document.getElementById('control-camlight-toggle'),
        aiDetectionToggle: document.getElementById('control-ai-toggle'),
        
        // Production Run Controls
        startRunBtn: document.getElementById('start-run-btn'),
        stopRunBtn: document.getElementById('stop-run-btn'),
        resetAllBtn: document.getElementById('reset-all-btn'),
        profileSelect: document.getElementById('object-profile-select'),
        targetCountInput: document.getElementById('target-count-input'),
        postBatchDelayInput: document.getElementById('post-batch-delay-input'),

        // AI Display
        aiOfflineOverlay: document.getElementById('ai-offline-overlay-usb'),
        liveAiFeed: document.getElementById('live-ai-feed-usb'),
        aiLastDetection: document.getElementById('ai-last-detection-display'),
    };

    function connect() {
        socket = new WebSocket(wsUrl);
        socket.onopen = () => console.log('[WebSocket] Connection established');
        socket.onclose = () => setTimeout(connect, 3000);
        socket.onerror = (error) => console.error('[WebSocket] Error:', error);
        socket.onmessage = handleWebSocketMessage;
    }

    function handleWebSocketMessage(event) {
        try {
            const message = JSON.parse(event.data);
            switch (message.type) {
                case 'system_status':
                    updateSystemStatus(message.data);
                    break;
                case 'orchestration_status':
                    updateOrchestrationStatus(message.data);
                    break;
                // --- NEW: Handle the AI update message ---
                case 'ai_update':
                    updateAiDetectionInfo(message.data);
                    break;
            }
        } catch (e) {
            // Ignore non-JSON messages
        }
    }

    function updateSystemStatus(data) {
        if (!data) return;
        const isSensor1Active = data.sensor_1_status;
        if (isSensor1Active && !appState.lastSensor1State && appState.currentMode === 'Running') {
            spawnBoxAnimation();
        }
        appState.lastSensor1State = isSensor1Active;
        
        updateStatusBadge(DOMElements.statusSensor1, data.sensor_1_status, 'triggered', 'clear');
        updateStatusBadge(DOMElements.statusSensor2, data.sensor_2_status, 'triggered', 'clear');
        updateStatusBadge(DOMElements.statusIoModule, data.io_module_status === 'ok', 'ok', 'error', data.io_module_status);
        updateStatusBadge(DOMElements.aiServiceStatus, data.ai_service_status === 'online', 'online', 'offline');

        setToggleState(DOMElements.conveyorToggle, data.conveyor_relay_status);
        setToggleState(DOMElements.gateToggle, data.gate_relay_status);
        setToggleState(DOMElements.diverterToggle, data.diverter_relay_status);
        setToggleState(DOMElements.cameraLightToggle, data.camera_light_status);
        setToggleState(DOMElements.aiDetectionToggle, data.ai_service_enabled);

        DOMElements.liveAiFeed.style.filter = data.ai_service_enabled ? 'none' : 'grayscale(100%) opacity(0.5)';
        DOMElements.aiOfflineOverlay.classList.toggle('hidden', data.ai_service_status === 'online');

        DOMElements.countOnBelt.textContent = data.in_flight_count || '0';
    }

    function updateOrchestrationStatus(data) {
        if (!data) return;
        const mode = data.mode || "Stopped";
        appState.currentMode = mode;
        DOMElements.conveyorMode.textContent = mode.toUpperCase();
        DOMElements.activeProfile.textContent = data.active_profile || 'None';
        DOMElements.countExited.textContent = data.run_progress || '0';
        
        const isRunning = mode === 'Running';
        DOMElements.conveyorBelt.classList.toggle('running', isRunning);

        const target = data.target_count;
        const progress = data.run_progress;
        let percentage = target > 0 ? Math.min((progress / target) * 100, 100) : 0;
        
        const circumference = 2 * Math.PI * 45;
        const offset = circumference - (percentage / 100) * circumference;
        DOMElements.progressPath.style.strokeDasharray = circumference;
        DOMElements.progressPath.style.strokeDashoffset = offset;
        DOMElements.progressPercentage.textContent = `${Math.round(percentage)}%`;
        DOMElements.progressDetails.textContent = `${progress} / ${target > 0 ? target : '∞'}`;
    }

    // --- NEW: Function to update the "Last Detected" display ---
    function updateAiDetectionInfo(data) {
        if (!DOMElements.aiLastDetection || !data) return;
        
        const lastDetected = data.last_detected;
        const isSearching = lastDetected === "Searching...";
        
        if (isSearching) {
            DOMElements.aiLastDetection.innerHTML = `<i class="bi bi-search"></i> ${lastDetected}`;
            DOMElements.aiLastDetection.classList.remove('visible');
        } else {
            DOMElements.aiLastDetection.innerHTML = `Last Detected: <span class="detected-object">${lastDetected}</span>`;
            DOMElements.aiLastDetection.classList.add('visible');
        }
    }

    function spawnBoxAnimation() {
        const box = document.createElement('div');
        box.className = 'box';
        const transitTime = DOMElements.animationZone.dataset.animationTime || 5;
        box.style.setProperty('--box-transit-time', `${transitTime}s`);
        DOMElements.conveyorBelt.appendChild(box);
        setTimeout(() => box.remove(), transitTime * 1000);
    }

    function updateStatusBadge(element, isActive, activeClass, inactiveClass, text) {
        if (!element) return;
        element.className = 'status-badge';
        const stateClass = isActive ? activeClass : inactiveClass;
        element.classList.add(stateClass);
        element.textContent = text || stateClass;
    }
    
    function setToggleState(toggleInput, isActive) {
        if (toggleInput) toggleInput.checked = isActive;
    }

    async function postAPI(endpoint, body = {}) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            if (!response.ok) console.error(`API Error on ${endpoint}:`, await response.json());
        } catch (error) {
            console.error(`Network Error on ${endpoint}:`, error);
        }
    }

    // Event Listeners
    DOMElements.startRunBtn?.addEventListener('click', () => {
        const profileId = DOMElements.profileSelect.value;
        if (!profileId) return alert('Please select a Profile.');
        postAPI('/api/v1/orchestration/run/start', {
            object_profile_id: parseInt(profileId),
            target_count: parseInt(DOMElements.targetCountInput.value),
            post_batch_delay_sec: parseInt(DOMElements.postBatchDelayInput.value)
        });
    });
    DOMElements.stopRunBtn?.addEventListener('click', () => postAPI('/api/v1/orchestration/run/stop'));
    DOMElements.resetAllBtn?.addEventListener('click', () => postAPI('/api/v1/system/reset-all'));
    DOMElements.conveyorToggle?.addEventListener('change', () => postAPI('/api/v1/outputs/toggle/conveyor'));
    DOMElements.gateToggle?.addEventListener('change', () => postAPI('/api/v1/outputs/toggle/gate'));
    DOMElements.diverterToggle?.addEventListener('change', () => postAPI('/api/v1/outputs/toggle/diverter'));
    DOMElements.cameraLightToggle?.addEventListener('change', () => postAPI('/api/v1/outputs/toggle/camera_light'));
    DOMElements.aiDetectionToggle?.addEventListener('change', () => postAPI('/api/v1/system/ai/toggle'));

    connect();
});