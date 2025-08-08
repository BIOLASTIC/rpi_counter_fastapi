document.addEventListener('DOMContentLoaded', function () {
    // --- WebSocket Setup ---
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
    let socket;

    function connect() {
        socket = new WebSocket(wsUrl);
        socket.onopen = () => console.log("[WebSocket] Connection established.");
        socket.onclose = () => {
            console.warn("[WebSocket] Connection died. Reconnecting in 3 seconds...");
            setTimeout(connect, 3000);
        };
        socket.onerror = (error) => console.error(`[WebSocket] Error: ${error.message}`);
        socket.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                if (message.type === 'full_status') {
                    updateUI(message.data);
                }
            } catch (e) {
                console.warn("Received non-JSON message from WebSocket:", event.data);
            }
        };
    }
    connect();

    // --- Element References ---
    // Production Controls
    const startRunBtn = document.getElementById('start-run-btn');
    const stopRunBtn = document.getElementById('stop-run-btn');
    const resetAllBtn = document.getElementById('reset-all-btn');

    // Pre-Run Modal
    const preRunModal = new bootstrap.Modal(document.getElementById('pre-run-modal'));
    const operatorSelect = document.getElementById('operator-select');
    const batchCodeInput = document.getElementById('batch-code-input');
    const reviewRunBtn = document.getElementById('review-run-btn');
    const goBackBtn = document.getElementById('go-back-btn');
    const startFinalRunBtn = document.getElementById('start-final-run-btn');
    const inputView = document.getElementById('pre-run-input-view');
    const confirmView = document.getElementById('pre-run-confirm-view');

    // Alarm Block
    const alarmBlock = document.getElementById('run-alarm-block');
    const alarmMessageEl = document.getElementById('run-alarm-message');
    const acknowledgeAlarmBtn = document.getElementById('acknowledge-alarm-btn');
    
    // Camera & Manual Control Elements
    const cameraSwitcher = document.getElementById('camera-switcher');
    const liveCameraFeed = document.getElementById('live-camera-feed');
    const liveFeedTitle = document.getElementById('live-feed-title');
    const manualControlToggles = document.querySelectorAll('.manual-control-toggle .toggle-switch input');
    
    // --- Helper Functions ---
    async function apiPost(endpoint, data = null) {
        try {
            const options = {
                method: 'POST',
                headers: data ? { 'Content-Type': 'application/json' } : {},
                body: data ? JSON.stringify(data) : null,
            };
            const response = await fetch(endpoint, options);
            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'API request failed');
            }
            return await response.json();
        } catch (error) {
            alert(`Error: ${error.message}`);
            console.error(`API POST to ${endpoint} failed:`, error);
        }
    }

    // --- New Run Workflow Logic ---
    let runConfig = {}; 
    async function loadOperators() {
        try {
            const response = await fetch('/api/v1/operators');
            const operators = await response.json();
            operatorSelect.innerHTML = '<option value="">-- Select Operator --</option>';
            operators.filter(op => op.status === 'Active').forEach(op => {
                operatorSelect.innerHTML += `<option value="${op.id}">${op.name}</option>`;
            });
        } catch (error) { console.error('Failed to load operators', error); }
    }
    
    startRunBtn.addEventListener('click', () => {
        const profileId = document.getElementById('object-profile-select').value;
        const targetCount = document.getElementById('target-count-input').value;
        const postBatchDelay = document.getElementById('post-batch-delay-input').value;

        if (!profileId) {
            alert('Please select a Recipe first.');
            return;
        }

        runConfig = {
            object_profile_id: parseInt(profileId),
            target_count: parseInt(targetCount),
            post_batch_delay_sec: parseInt(postBatchDelay) || 5,
        };

        inputView.style.display = 'block';
        confirmView.style.display = 'none';
        operatorSelect.value = '';
        batchCodeInput.value = '';
        document.getElementById('pre-run-modal-title').textContent = 'Pre-Run Checklist';
        preRunModal.show();
    });

    reviewRunBtn.addEventListener('click', () => {
        const operatorId = operatorSelect.value;
        const batchCode = batchCodeInput.value.trim();

        if (!operatorId || !batchCode) {
            alert('Please select an operator and enter a batch code.');
            return;
        }

        runConfig.operator_id = parseInt(operatorId);
        runConfig.batch_code = batchCode;

        document.getElementById('confirm-operator').textContent = operatorSelect.options[operatorSelect.selectedIndex].text;
        document.getElementById('confirm-batch-code').textContent = batchCode;
        const profileSelect = document.getElementById('object-profile-select');
        document.getElementById('confirm-recipe').textContent = profileSelect.options[profileSelect.selectedIndex].text;
        document.getElementById('confirm-target').textContent = runConfig.target_count === 0 ? 'Unlimited' : runConfig.target_count;
        
        document.getElementById('pre-run-modal-title').textContent = 'Confirm Run Details';
        inputView.style.display = 'none';
        confirmView.style.display = 'block';
    });

    goBackBtn.addEventListener('click', () => {
        document.getElementById('pre-run-modal-title').textContent = 'Pre-Run Checklist';
        confirmView.style.display = 'none';
        inputView.style.display = 'block';
    });

    startFinalRunBtn.addEventListener('click', () => {
        apiPost('/api/v1/orchestration/run/start', runConfig).then(() => {
            if (preRunModal) preRunModal.hide();
        });
    });
    
    stopRunBtn.addEventListener('click', () => apiPost('/api/v1/orchestration/run/stop'));
    resetAllBtn.addEventListener('click', () => apiPost('/api/v1/system/reset-all'));
    acknowledgeAlarmBtn.addEventListener('click', () => apiPost('/api/v1/orchestration/run/acknowledge-alarm'));

    // --- Camera Switcher Logic ---
    function setupCameraSwitcher() {
        if (!cameraSwitcher) return;
        const firstButton = cameraSwitcher.querySelector('button');
        if (firstButton) {
            firstButton.classList.add('active');
            const initialCameraId = firstButton.dataset.cameraId;
            liveCameraFeed.src = `/api/v1/camera/stream/${initialCameraId}`;
            liveFeedTitle.textContent = `${initialCameraId.toUpperCase()} CAMERA`;
        }

        cameraSwitcher.addEventListener('click', (e) => {
            const button = e.target.closest('button');
            if (!button) return;
            cameraSwitcher.querySelectorAll('button').forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            const cameraId = button.dataset.cameraId;
            liveCameraFeed.src = `/api/v1/camera/stream/${cameraId}`;
            liveFeedTitle.textContent = `${cameraId.toUpperCase()} CAMERA`;
        });
    }

    // --- Manual Control Logic ---
    function setupManualControls() {
        manualControlToggles.forEach(toggle => {
            toggle.addEventListener('change', () => {
                const controlName = toggle.id.replace('control-', '').replace('-toggle', '');
                apiPost(`/api/v1/outputs/toggle/${controlName}`);
            });
        });
    }

    // --- Main UI Update Function ---
    function updateUI(data) {
        if (!data || !data.system || !data.orchestration) {
            console.warn("Incomplete status data received", data);
            return;
        }
        const { system, orchestration } = data;

        // Alarm Handling
        if (orchestration.active_alarm_message) {
            alarmMessageEl.textContent = orchestration.active_alarm_message;
            alarmBlock.style.display = 'flex';
        } else {
            alarmBlock.style.display = 'none';
        }

        // Orchestration Status
        document.getElementById('count-on-belt').textContent = system.in_flight_count;
        document.getElementById('count-exited').textContent = orchestration.run_progress;
        document.getElementById('conveyor-mode').textContent = orchestration.mode.toUpperCase();
        document.getElementById('active-profile-display').textContent = orchestration.active_profile;

        // Progress Circle
        const target = orchestration.target_count;
        const progress = orchestration.run_progress;
        const percentage = (target > 0) ? Math.min(100, Math.round((progress / target) * 100)) : 0;
        const progressPath = document.getElementById('progress-path');
        const circumference = 2 * Math.PI * 45;
        const offset = circumference - (percentage / 100) * circumference;
        if (progressPath) progressPath.style.strokeDashoffset = offset;
        document.getElementById('progress-percentage').textContent = `${percentage}%`;
        document.getElementById('progress-details').textContent = `${progress} / ${target === 0 ? '∞' : target}`;

        // Conveyor Animation
        document.getElementById('conveyor-belt').classList.toggle('running', orchestration.mode === 'Running');

        // System Control Panel (Sensors & Manual Toggles)
        const sensor1 = document.getElementById('status-sensor-1');
        sensor1.textContent = system.sensor_1_status ? 'TRIGGERED' : 'clear';
        sensor1.className = `status-badge ${system.sensor_1_status ? 'warn' : 'clear'}`;
        
        const sensor2 = document.getElementById('status-sensor-2');
        sensor2.textContent = system.sensor_2_status ? 'TRIGGERED' : 'clear';
        sensor2.className = `status-badge ${system.sensor_2_status ? 'warn' : 'clear'}`;

        const ioModule = document.getElementById('status-io-module');
        ioModule.textContent = system.io_module_status;
        ioModule.className = `status-badge ${system.io_module_status === 'ok' ? 'ok' : 'error'}`;

        const toggleStates = {
            'conveyor': system.conveyor_relay_status,
            'gate': system.gate_relay_status,
            'diverter': system.diverter_relay_status,
            'camera_light': system.camera_light_status,
            'buzzer': system.buzzer_status
        };

        for (const [name, isOn] of Object.entries(toggleStates)) {
            const toggle = document.getElementById(`control-${name}-toggle`);
            if (toggle && toggle.checked !== isOn) {
                toggle.checked = isOn;
            }
        }
    }

    // --- Initial Load ---
    loadOperators();
    setupCameraSwitcher();
    setupManualControls();
});