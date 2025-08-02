// /static/js/dashboard_v3.js

document.addEventListener('DOMContentLoaded', () => {
    // --- WebSocket Connection ---
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
    let socket;

    function connectWebSocket() {
        socket = new WebSocket(wsUrl);

        socket.onopen = () => console.log("[WebSocket] Connection established.");
        socket.onclose = () => {
            console.error('[WebSocket] Connection died. Reconnecting in 3 seconds...');
            setTimeout(connectWebSocket, 3000);
        };
        socket.onerror = (error) => console.error(`[WebSocket] Error: ${error.message}`);
        socket.onmessage = handleWebSocketMessage;
    }

    // --- Element Selectors ---
    const elements = {
        // Animation & Run Status
        animationZone: document.getElementById('animation-zone'),
        conveyorBelt: document.getElementById('conveyor-belt'),
        countOnBelt: document.getElementById('count-on-belt'),
        countExited: document.getElementById('count-exited'),
        conveyorMode: document.getElementById('conveyor-mode'),
        progressPath: document.getElementById('progress-path'),
        progressPercentage: document.getElementById('progress-percentage'),
        progressDetails: document.getElementById('progress-details'),
        activeProfileDisplay: document.getElementById('active-profile-display'),
        // Live Feeds
        rawFeedImg: document.getElementById('live-camera-feed'),
        aiFeedImg: document.getElementById('live-ai-feed'),
        rawFeedTitle: document.getElementById('raw-feed-title'),
        aiOfflineOverlay: document.getElementById('ai-offline-overlay'),
        // Controls
        startRunBtn: document.getElementById('start-run-btn'),
        stopRunBtn: document.getElementById('stop-run-btn'),
        resetAllBtn: document.getElementById('reset-all-btn'),
        profileSelect: document.getElementById('object-profile-select'),
        targetCountInput: document.getElementById('target-count-input'),
        postBatchDelayInput: document.getElementById('post-batch-delay-input'),
        // System Status Badges
        sensor1Badge: document.getElementById('status-sensor-1'),
        sensor2Badge: document.getElementById('status-sensor-2'),
        ioModuleBadge: document.getElementById('status-io-module'),
        aiServiceBadge: document.getElementById('status-ai-service'),
        // Manual Control Toggles
        conveyorToggle: document.getElementById('control-conveyor-toggle'),
        gateToggle: document.getElementById('control-gate-toggle'),
        diverterToggle: document.getElementById('control-diverter-toggle'),
        camlightToggle: document.getElementById('control-camlight-toggle'),
        aiToggle: document.getElementById('control-ai-toggle'),
        // AI Source Buttons
        aiSourceBtnRpi: document.getElementById('ai-source-btn-rpi'),
        aiSourceBtnUsb: document.getElementById('ai-source-btn-usb'),
    };

    // --- State Variables ---
    const progressCircleRadius = elements.progressPath.r.baseVal.value;
    const progressCircleCircumference = 2 * Math.PI * progressCircleRadius;
    elements.progressPath.style.strokeDasharray = `${progressCircleCircumference} ${progressCircleCircumference}`;
    
    // --- THE FIX: Add a state variable to track the in-flight count ---
    let lastInFlightCount = 0;


    // --- Event Handlers ---
    function handleWebSocketMessage(event) {
        try {
            const message = JSON.parse(event.data);
            if (message.type === 'system_status') {
                updateSystemStatus(message.data);
            } else if (message.type === 'orchestration_status') {
                updateOrchestrationStatus(message.data);
            }
        } catch (e) {
            console.warn("Received non-JSON message from WebSocket:", event.data);
        }
    }

    // --- Update Functions ---
    function updateSystemStatus(data) {
        updateBadge(elements.sensor1Badge, data.sensor_1_status ? 'TRIGGERED' : 'CLEAR', { 'triggered': data.sensor_1_status, 'clear': !data.sensor_1_status });
        updateBadge(elements.sensor2Badge, data.sensor_2_status ? 'TRIGGERED' : 'CLEAR', { 'triggered': data.sensor_2_status, 'clear': !data.sensor_2_status });
        updateBadge(elements.ioModuleBadge, data.io_module_status, { 'ok': data.io_module_status === 'ok', 'error': data.io_module_status !== 'ok' });
        updateBadge(elements.aiServiceBadge, data.ai_service_status, { 'online': data.ai_service_status === 'online', 'offline': data.ai_service_status !== 'online' });
        
        elements.aiOfflineOverlay.classList.toggle('hidden', data.ai_service_status === 'online');
        elements.countOnBelt.textContent = data.in_flight_count;

        // Sync toggle switches with actual hardware state
        updateToggle(elements.conveyorToggle, data.conveyor_relay_status);
        updateToggle(elements.gateToggle, data.gate_relay_status);
        updateToggle(elements.diverterToggle, data.diverter_relay_status);
        updateToggle(elements.camlightToggle, data.camera_light_status);
        updateToggle(elements.aiToggle, data.ai_service_enabled);
        
        // Update video feeds AND the active button style
        updateVideoFeeds(data.ai_detection_source);
        updateActiveButton(data.ai_detection_source);

        // --- THE FIX: Trigger the animation when a new box enters ---
        // 1. Check if the in-flight count has increased.
        if (data.in_flight_count > lastInFlightCount) {
            spawnBox();
        }
        // 2. Update the state for the next message.
        lastInFlightCount = data.in_flight_count;
    }

    function updateOrchestrationStatus(data) {
        elements.conveyorMode.textContent = data.mode.toUpperCase();
        elements.conveyorBelt.classList.toggle('running', data.mode === 'Running');

        const profileName = data.active_profile || 'None';
        elements.activeProfileDisplay.textContent = profileName;
        elements.activeProfileDisplay.style.backgroundColor = profileName === 'None' ? 'var(--text-secondary)' : 'var(--accent-teal)';

        // Update progress circle
        const target = data.target_count;
        const progress = data.run_progress;
        const percentage = (target > 0) ? Math.min((progress / target) * 100, 100) : 0;
        const offset = progressCircleCircumference - (percentage / 100) * progressCircleCircumference;
        elements.progressPath.style.strokeDashoffset = offset;
        elements.progressPercentage.textContent = `${Math.floor(percentage)}%`;
        elements.progressDetails.textContent = `${progress} / ${target > 0 ? target : '∞'}`;

        elements.countExited.textContent = progress;

        // --- THE FIX: Remove the old, incorrect animation trigger ---
        // The animation is now handled by updateSystemStatus.
        /*
        if (progress > lastExitedCount) {
            spawnBox();
        }
        lastExitedCount = progress;
        */
    }

    function updateVideoFeeds(aiSource) {
        if (!aiSource) return;
        const rawSrc = `/api/v1/camera/stream/${aiSource}`;
        const aiSrc = `/api/v1/camera/ai_stream/${aiSource}`;
        const titleText = `${aiSource.toUpperCase()} CAM (RAW)`;

        if (elements.rawFeedImg.src.endsWith(rawSrc) === false) elements.rawFeedImg.src = rawSrc;
        if (elements.aiFeedImg.src.endsWith(aiSrc) === false) elements.aiFeedImg.src = aiSrc;
        if (elements.rawFeedTitle.textContent !== titleText) elements.rawFeedTitle.textContent = titleText;
    }

    function updateActiveButton(activeSource) {
        if (activeSource === 'rpi') {
            elements.aiSourceBtnRpi.classList.add('active');
            elements.aiSourceBtnUsb.classList.remove('active');
        } else if (activeSource === 'usb') {
            elements.aiSourceBtnUsb.classList.add('active');
            elements.aiSourceBtnRpi.classList.remove('active');
        }
    }

    function updateBadge(element, text, stateClasses) {
        if (!element) return;
        element.textContent = text;
        for (const [cls, is_active] of Object.entries(stateClasses)) {
            element.classList.toggle(cls, is_active);
        }
    }

    function updateToggle(toggleElement, isActive) {
        if (toggleElement && toggleElement.checked !== isActive) {
            toggleElement.checked = isActive;
        }
    }

    // --- Control Actions ---
    async function apiPost(url, body = {}) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            if (!response.ok) {
                const errorData = await response.json();
                alert(`Error: ${errorData.detail || response.statusText}`);
            }
            return response;
        } catch (error) {
            alert(`Network error: ${error.message}`);
        }
    }

    function setAiSource(source) {
        console.log(`Requesting AI source switch to: ${source.toUpperCase()}`);
        apiPost('/api/v1/system/ai/source', { source });
    }

    function startRun() {
        const profileId = elements.profileSelect.value;
        if (!profileId) {
            alert('Please select an Object Profile first.');
            return;
        }
        const payload = {
            object_profile_id: parseInt(profileId, 10),
            target_count: parseInt(elements.targetCountInput.value, 10),
            post_batch_delay_sec: parseInt(elements.postBatchDelayInput.value, 10),
        };
        apiPost('/api/v1/orchestration/run/start', payload);
    }
    function stopRun() { apiPost('/api/v1/orchestration/run/stop'); }
    function resetAll() {
        if (confirm('Are you sure you want to perform a full system reset?')) {
            apiPost('/api/v1/system/reset-all');
        }
    }
    function toggleOutput(name) { apiPost(`/api/v1/outputs/toggle/${name}`); }
    function toggleAiService() { apiPost('/api/v1/system/ai/toggle'); }

    // --- Animation ---
    function spawnBox() {
        const box = document.createElement('div');
        box.className = 'box';
        const transitTime = elements.animationZone.dataset.animationTime || 5;
        box.style.animationDuration = `${transitTime}s`;
        elements.conveyorBelt.appendChild(box);
        setTimeout(() => box.remove(), transitTime * 1000);
    }

    // --- Initial Setup ---
    elements.startRunBtn.addEventListener('click', startRun);
    elements.stopRunBtn.addEventListener('click', stopRun);
    elements.resetAllBtn.addEventListener('click', resetAll);
    
    elements.conveyorToggle.addEventListener('change', () => toggleOutput('conveyor'));
    elements.gateToggle.addEventListener('change', () => toggleOutput('gate'));
    elements.diverterToggle.addEventListener('change', () => toggleOutput('diverter'));
    elements.camlightToggle.addEventListener('change', () => toggleOutput('camera_light'));
    elements.aiToggle.addEventListener('change', toggleAiService);

    elements.aiSourceBtnRpi.addEventListener('click', () => setAiSource('rpi'));
    elements.aiSourceBtnUsb.addEventListener('click', () => setAiSource('usb'));

    connectWebSocket();
});