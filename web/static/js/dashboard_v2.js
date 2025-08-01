document.addEventListener('DOMContentLoaded', () => {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
    const socket = new WebSocket(wsUrl);

    let lastInFlightCount = 0;

    const ui = {
        // Animation & Progress
        conveyorBelt: document.getElementById('conveyor-belt'),
        countOnBelt: document.getElementById('count-on-belt'),
        countExited: document.getElementById('count-exited'),
        progressCirclePath: document.querySelector('.progress-circle__path'),
        progressPercentage: document.getElementById('progress-percentage'),
        progressDetails: document.getElementById('progress-details'),
        systemMode: document.getElementById('system-mode'),
        activeProfileDisplay: document.getElementById('active-profile-display'),
        
        // Feeds
        liveAiFeed: document.getElementById('live-ai-feed-usb'),
        aiOfflineOverlay: document.getElementById('ai-offline-overlay-usb'),
        aiOfflineText: document.getElementById('ai-offline-overlay-usb').querySelector('span'),
        
        // Hardware Status
        statusSensor1: document.getElementById('status-sensor-1'),
        statusSensor2: document.getElementById('status-sensor-2'),
        statusConveyorRelay: document.getElementById('status-conveyor-relay'),
        statusGateRelay: document.getElementById('status-gate-relay'),
        statusDiverterRelay: document.getElementById('status-diverter-relay'),
        statusIoModule: document.getElementById('status-io-module'),
        
        // Controls
        profileSelect: document.getElementById('object-profile-select'),
        targetCountInput: document.getElementById('target-count-input'),
        postBatchDelayInput: document.getElementById('post-batch-delay-input'),
        startRunBtn: document.getElementById('start-run-btn'),
        stopRunBtn: document.getElementById('stop-run-btn'),
        resetAllBtn: document.getElementById('reset-all-btn'),
    };

    const animationZone = document.getElementById('animation-zone');
    const animationTime = animationZone.dataset.animationTime || 5;
    ui.conveyorBelt.style.setProperty('--box-transit-time', `${animationTime}s`);

    // --- WebSocket Handlers ---
    socket.onopen = () => console.log('[WebSocket] Connection established.');
    socket.onclose = () => {
        console.error('[WebSocket] Connection died.');
        lastInFlightCount = 0;
    };
    socket.onerror = (error) => console.error(`[WebSocket] Error: ${error.message}`);
    socket.onmessage = (event) => {
        try {
            const message = JSON.parse(event.data);
            if (message.type === 'system_status') {
                updateSystemStatus(message.data);
            } else if (message.type === 'orchestration_status') {
                updateOrchestrationStatus(message.data);
            }
        } catch (e) {
            console.warn('Received non-JSON message from WebSocket:', event.data);
        }
    };
    
    if (ui.liveAiFeed) {
        ui.liveAiFeed.onerror = () => {
            console.error("AI video stream error.");
            ui.aiOfflineOverlay.classList.remove('hidden');
            ui.aiOfflineText.textContent = 'Stream Error';
            setTimeout(() => {
                if (ui.liveAiFeed) {
                    ui.liveAiFeed.src = `/api/v1/camera/ai_stream/usb?t=${new Date().getTime()}`;
                }
            }, 5000); 
        };
    }
    
    function updateSystemStatus(status) {
        updateBadge(ui.statusSensor1, status.sensor_1_status, 'TRIGGERED', 'CLEAR');
        updateBadge(ui.statusSensor2, status.sensor_2_status, 'TRIGGERED', 'CLEAR');
        updateBadge(ui.statusConveyorRelay, status.conveyor_relay_status, 'ON', 'OFF');
        updateBadge(ui.statusGateRelay, status.gate_relay_status, 'ON', 'OFF');
        updateBadge(ui.statusDiverterRelay, status.diverter_relay_status, 'ON', 'OFF');
        updateBadge(ui.statusIoModule, status.io_module_status === 'ok', 'CONNECTED', 'ERROR');
        
        for (const camId in status.camera_statuses) {
            const el = document.getElementById(`status-camera-${camId}`);
            if (el) updateBadge(el, status.camera_statuses[camId] === 'connected', 'CONNECTED', 'OFFLINE');
        }

        if (status && 'ai_service_status' in status) {
            ui.aiOfflineOverlay.classList.toggle('hidden', status.ai_service_status === 'online');
            if(status.ai_service_status !== 'online') ui.aiOfflineText.textContent = 'OFFLINE';
        } else {
            ui.aiOfflineOverlay.classList.remove('hidden');
            ui.aiOfflineText.textContent = 'Connecting...';
        }

        const currentInFlightCount = status.in_flight_count || 0;
        ui.countOnBelt.textContent = currentInFlightCount;

        if (currentInFlightCount > lastInFlightCount) {
            createBoxAnimation();
        }
        lastInFlightCount = currentInFlightCount;
    }

    function updateOrchestrationStatus(status) {
        ui.systemMode.textContent = status.mode;
        updateBadge(ui.systemMode, status.mode === 'Running', 'RUNNING', status.mode.toUpperCase());
        
        if (status.mode === 'Paused (Post-Run)') {
             ui.systemMode.classList.add('warn');
        }

        ui.activeProfileDisplay.textContent = status.active_profile;
        ui.countExited.textContent = status.run_progress;

        const isRunning = status.mode === 'Running';
        ui.conveyorBelt.classList.toggle('running', isRunning);

        let percentage = 0;
        if (status.target_count > 0) {
            percentage = Math.min((status.run_progress / status.target_count) * 100, 100);
        } else if (status.mode === 'Complete' || status.mode === 'Running') {
            percentage = 100;
        }
        
        ui.progressPercentage.textContent = `${Math.round(percentage)}%`;
        ui.progressDetails.textContent = `${status.run_progress} / ${status.target_count > 0 ? status.target_count : '∞'}`;
        
        const circumference = 2 * Math.PI * 45;
        const offset = circumference - (percentage / 100) * circumference;
        ui.progressCirclePath.style.strokeDasharray = `${circumference} ${circumference}`;
        ui.progressCirclePath.style.strokeDashoffset = offset;
    }

    function updateBadge(element, isActive, activeText, inactiveText) {
        if (!element) return;
        element.textContent = isActive ? activeText : inactiveText;
        element.className = 'status-badge'; 
        const activeClass = (activeText.toLowerCase() === 'on' || activeText.toLowerCase() === 'connected' || activeText.toLowerCase() === 'running') ? 'ok' : activeText.toLowerCase();
        const inactiveClass = inactiveText.toLowerCase();
        element.classList.add(isActive ? activeClass : inactiveClass);
    }

    function createBoxAnimation() {
        const box = document.createElement('div');
        box.className = 'box';
        ui.conveyorBelt.appendChild(box);
        setTimeout(() => box.remove(), animationTime * 1000 + 100);
    }
    
    // --- Event Listeners for Controls ---
    ui.startRunBtn.addEventListener('click', async () => {
        const profileId = ui.profileSelect.value;
        const targetCount = ui.targetCountInput.value;
        const postBatchDelay = ui.postBatchDelayInput.value;

        if (!profileId) {
            alert('Please select an Object Profile first.');
            return;
        }

        // --- THE FIX: Create a single payload and send one atomic request ---
        const payload = {
            object_profile_id: parseInt(profileId),
            target_count: parseInt(targetCount),
            post_batch_delay_sec: parseInt(postBatchDelay)
        };

        try {
            const response = await fetch('/api/v1/orchestration/run/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `Failed to start run: ${response.statusText}`);
            }

            console.log("Successfully commanded the system to start a new run.");

        } catch (error) {
            console.error("Failed to start run:", error);
            alert(`Error starting run: ${error.message}. Check console for details.`);
        }
    });

    ui.stopRunBtn.addEventListener('click', () => {
        fetch('/api/v1/orchestration/run/stop', { method: 'POST' });
    });

    ui.resetAllBtn.addEventListener('click', () => {
        if(confirm('This will stop the process and reset all counts. Are you sure?')) {
            fetch('/api/v1/system/reset-all', { method: 'POST' });
        }
    });
});