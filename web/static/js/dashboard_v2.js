document.addEventListener('DOMContentLoaded', function () {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
    let socket;

    // --- DOM Element Cache ---
    const DOMElements = {
        // Run Status
        systemMode: document.getElementById('system-mode'),
        activeProfile: document.getElementById('active-profile-display'),
        progressPath: document.querySelector('.progress-circle__path'),
        progressPercentage: document.getElementById('progress-percentage'),
        progressDetails: document.getElementById('progress-details'),
        
        // Counts
        countOnBelt: document.getElementById('count-on-belt'),
        countExited: document.getElementById('count-exited'),

        // Hardware Status
        statusSensor1: document.getElementById('status-sensor-1'),
        statusSensor2: document.getElementById('status-sensor-2'),
        statusConveyorRelay: document.getElementById('status-conveyor-relay'),
        statusGateRelay: document.getElementById('status-gate-relay'),
        statusDiverterRelay: document.getElementById('status-diverter-relay'),
        statusIoModule: document.getElementById('status-io-module'),
        statusCameraLight: document.getElementById('status-camera-light'),
        
        // Controls
        startRunBtn: document.getElementById('start-run-btn'),
        stopRunBtn: document.getElementById('stop-run-btn'),
        resetAllBtn: document.getElementById('reset-all-btn'),
        profileSelect: document.getElementById('object-profile-select'),
        targetCountInput: document.getElementById('target-count-input'),
        postBatchDelayInput: document.getElementById('post-batch-delay-input'),
        // NEW: AI Toggle Button
        aiToggleBtn: document.getElementById('ai-toggle-btn'),

        // Conveyor Animation
        conveyorBelt: document.getElementById('conveyor-belt'),
        animationZone: document.getElementById('animation-zone'),

        // Overlays
        aiOfflineOverlay: document.getElementById('ai-offline-overlay-usb'),
        liveAiFeed: document.getElementById('live-ai-feed-usb'),
    };
    
    document.querySelectorAll('[id^="status-camera-"]').forEach(el => {
        const camId = el.id.replace('status-camera-', '');
        DOMElements[`statusCamera-${camId}`] = el;
    });

    // --- WebSocket Handling ---
    function connect() {
        socket = new WebSocket(wsUrl);
        socket.onopen = () => console.log('WebSocket connection established');
        socket.onclose = () => {
            console.log('WebSocket connection died. Reconnecting in 3s...');
            setTimeout(connect, 3000);
        };
        socket.onerror = (error) => console.error('WebSocket Error:', error);
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
            }
        } catch (e) {
            console.warn('Received non-JSON message from WebSocket:', event.data);
        }
    }

    // --- UI Update Functions ---
    function updateSystemStatus(data) {
        if (!data) return;
        updateStatusBadge(DOMElements.statusSensor1, data.sensor_1_status, 'triggered', 'clear');
        updateStatusBadge(DOMElements.statusSensor2, data.sensor_2_status, 'triggered', 'clear');
        updateStatusBadge(DOMElements.statusConveyorRelay, data.conveyor_relay_status, 'on', 'off');
        updateStatusBadge(DOMElements.statusGateRelay, data.gate_relay_status, 'on', 'off');
        updateStatusBadge(DOMElements.statusDiverterRelay, data.diverter_relay_status, 'on', 'off');
        updateStatusBadge(DOMElements.statusIoModule, data.io_module_status === 'ok', 'ok', 'error', data.io_module_status);
        updateStatusBadge(DOMElements.statusCameraLight, data.camera_light_status, 'on', 'off');

        DOMElements.countOnBelt.textContent = data.in_flight_count || '0';

        if (data.camera_statuses) {
            Object.entries(data.camera_statuses).forEach(([camId, status]) => {
                const el = DOMElements[`statusCamera-${camId}`];
                if (el) updateStatusBadge(el, status === 'connected', 'connected', 'disconnected', status);
            });
        }
        
        // --- AI Service Status Update ---
        const isAiOnline = data.ai_service_status === 'online';
        const isAiEnabled = data.ai_service_enabled;
        
        // Update the main overlay for the AI feed
        DOMElements.aiOfflineOverlay.classList.toggle('hidden', isAiOnline);
        if (!isAiOnline) {
             DOMElements.aiOfflineOverlay.querySelector('span').textContent = 'SERVICE OFFLINE';
        }

        // Update the AI toggle button's appearance
        if (DOMElements.aiToggleBtn) {
            const btnText = DOMElements.aiToggleBtn.querySelector('span');
            if (isAiEnabled) {
                DOMElements.aiToggleBtn.classList.remove('btn-outline-danger');
                DOMElements.aiToggleBtn.classList.add('btn-outline-info');
                if (btnText) btnText.textContent = 'AI Detection is ON';
            } else {
                DOMElements.aiToggleBtn.classList.remove('btn-outline-info');
                DOMElements.aiToggleBtn.classList.add('btn-outline-danger');
                if (btnText) btnText.textContent = 'AI Detection is OFF';
            }
        }
        
        // Make the AI feed visually greyed out if disabled but the service is online
        DOMElements.liveAiFeed.style.filter = isAiEnabled ? 'none' : 'grayscale(100%) opacity(0.6)';

    }

    function updateOrchestrationStatus(data) {
        if (!data) return;
        updateStatusBadge(DOMElements.systemMode, true, data.mode.toLowerCase().replace(/[\s()]/g, '-'), '', data.mode);
        DOMElements.activeProfile.textContent = data.active_profile || 'None';
        DOMElements.countExited.textContent = data.run_progress || '0';

        const isRunning = data.mode === 'Running';
        DOMElements.conveyorBelt.classList.toggle('running', isRunning);

        const target = data.target_count;
        const progress = data.run_progress;
        let percentage = 0;
        if (target > 0) {
            percentage = Math.min((progress / target) * 100, 100);
        }
        
        const circumference = 2 * Math.PI * 45;
        const offset = circumference - (percentage / 100) * circumference;
        DOMElements.progressPath.style.strokeDasharray = circumference;
        DOMElements.progressPath.style.strokeDashoffset = offset;
        
        DOMElements.progressPercentage.textContent = `${Math.round(percentage)}%`;
        DOMElements.progressDetails.textContent = `${progress} / ${target > 0 ? target : '∞'}`;
        
        if (isRunning && progress > (parseInt(DOMElements.countExited.dataset.lastCount, 10) || 0)) {
            spawnBoxAnimation();
        }
        DOMElements.countExited.dataset.lastCount = progress;
    }

    function updateStatusBadge(element, isActive, activeClass, inactiveClass, text) {
        if (!element) return;
        element.classList.toggle(activeClass, isActive);
        element.classList.toggle(inactiveClass, !isActive);
        element.textContent = text || (isActive ? activeClass.toUpperCase() : inactiveClass.toUpperCase());
    }
    
    function spawnBoxAnimation() {
        const box = document.createElement('div');
        box.className = 'box';
        DOMElements.conveyorBelt.appendChild(box);
        
        const transitTime = parseFloat(DOMElements.animationZone.dataset.animationTime) * 1000;
        setTimeout(() => box.remove(), transitTime);
    }

    async function postAPI(endpoint, body = {}) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            if (!response.ok) {
                const error = await response.json();
                alert(`Error: ${error.detail || response.statusText}`);
            }
            return response.ok;
        } catch (error) {
            alert(`Network Error: ${error}`);
            return false;
        }
    }

    // --- Event Listeners ---
    DOMElements.startRunBtn.addEventListener('click', () => {
        const profileId = DOMElements.profileSelect.value;
        const targetCount = DOMElements.targetCountInput.value;
        const postBatchDelay = DOMElements.postBatchDelayInput.value;
        if (!profileId) {
            alert('Please select an Object Profile before starting a run.');
            return;
        }
        const payload = {
            object_profile_id: parseInt(profileId, 10),
            target_count: parseInt(targetCount, 10),
            post_batch_delay_sec: parseInt(postBatchDelay, 10)
        };
        postAPI('/api/v1/orchestration/run/start', payload);
    });

    DOMElements.stopRunBtn.addEventListener('click', () => {
        postAPI('/api/v1/orchestration/run/stop');
    });
    
    DOMElements.resetAllBtn.addEventListener('click', () => {
        if(confirm('This will stop all hardware and reset all counts. Are you sure?')) {
            postAPI('/api/v1/system/reset-all');
        }
    });

    // NEW: Event listener for the AI toggle button
    DOMElements.aiToggleBtn.addEventListener('click', () => {
        postAPI('/api/v1/system/ai/toggle');
    });

    document.querySelectorAll('.manual-toggle-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const outputName = btn.dataset.outputName;
            if (outputName) {
                postAPI(`/api/v1/outputs/toggle/${outputName}`);
            }
        });
    });

    // --- Initial Load ---
    connect();
});