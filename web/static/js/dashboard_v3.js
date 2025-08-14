// rpi_counter_fastapi-dev2/web/static/js/dashboard_v3.js

document.addEventListener('DOMContentLoaded', () => {
    // --- Elements ---
    const conveyorMode = document.getElementById('conveyor-mode');
    const onBeltCount = document.getElementById('count-on-belt');
    const exitedCount = document.getElementById('count-exited');
    const progressPath = document.getElementById('progress-path');
    const progressText = document.getElementById('progress-percentage');
    const progressDetails = document.getElementById('progress-details');
    const activeProfileDisplay = document.getElementById('active-profile-display');
    const alarmBlock = document.getElementById('run-alarm-block');
    const alarmMessage = document.getElementById('run-alarm-message');
    const liveCameraFeed = document.getElementById('live-camera-feed');
    const liveFeedTitle = document.getElementById('live-feed-title');
    const cameraSelectBtns = document.querySelectorAll('.camera-select-btn');

    // --- NEW: Run Detail Elements ---
    const runDetailBatch = document.getElementById('run-detail-batch');
    const runDetailOperator = document.getElementById('run-detail-operator');

    // --- Control Elements ---
    const startRunBtn = document.getElementById('start-run-btn');
    const stopRunBtn = document.getElementById('stop-run-btn');
    const resetAllBtn = document.getElementById('reset-all-btn');
    const acknowledgeAlarmBtn = document.getElementById('acknowledge-alarm-btn');
    const profileSelect = document.getElementById('object-profile-select');
    const targetCountInput = document.getElementById('target-count-input');
    const postBatchDelayInput = document.getElementById('post-batch-delay-input');
    const manualToggles = document.querySelectorAll('.manual-control-toggle input[type="checkbox"]');
    
    // --- Pre-Run Modal Elements ---
    const preRunModal = new bootstrap.Modal(document.getElementById('pre-run-modal'));
    const operatorSelect = document.getElementById('operator-select');
    const batchCodeInput = document.getElementById('batch-code-input');
    const reviewRunBtn = document.getElementById('review-run-btn');
    const goBackBtn = document.getElementById('go-back-btn');
    const startFinalRunBtn = document.getElementById('start-final-run-btn');
    const preRunInputView = document.getElementById('pre-run-input-view');
    const preRunConfirmView = document.getElementById('pre-run-confirm-view');

    // --- Animation & State Elements ---
    const conveyorBelt = document.getElementById('conveyor-belt');
    const animationZone = document.getElementById('animation-zone');
    const animationTime = (parseFloat(animationZone.dataset.animationTime) || 5) * 1000;
    let lastInFlightCount = 0;

    // --- WebSocket Setup ---
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
    let socket;

    function connect() {
        socket = new WebSocket(wsUrl);
        socket.onopen = () => console.log('WebSocket connection established.');
        socket.onclose = () => {
            console.log('WebSocket disconnected. Retrying in 3 seconds...');
            setTimeout(connect, 3000);
        };
        socket.onerror = (error) => console.error('WebSocket error:', error);
        socket.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                if (message.type === 'full_status') {
                    updateSystemStatus(message.data.system);
                    updateOrchestrationStatus(message.data.orchestration);
                }
            } catch (e) {
                console.warn('Received non-JSON message:', event.data);
            }
        };
    }

    // --- Update Functions ---
    const updateSystemStatus = (status) => {
        if (!status) return;
        updateBadge('status-sensor-1', status.sensor_1_status, { on: 'triggered', off: 'clear' });
        updateBadge('status-sensor-2', status.sensor_2_status, { on: 'triggered', off: 'clear' });
        updateBadge('status-io-module', status.io_module_status === 'ok', { on: 'ok', off: 'error' });
        
        manualToggles.forEach(toggle => {
            const key = toggle.id.replace('control-', '').replace('-toggle', '');
            toggle.checked = status[`${key}_status`] || status[`${key}_relay_status`] || false;
        });

        onBeltCount.textContent = status.in_flight_count;
        conveyorBelt.classList.toggle('running', status.conveyor_relay_status);

        if (status.in_flight_count > lastInFlightCount) {
            triggerBoxAnimation();
        }
        lastInFlightCount = status.in_flight_count;
    };

    const updateOrchestrationStatus = (status) => {
        if (!status) return;

        conveyorMode.textContent = status.mode;
        exitedCount.textContent = status.run_progress;
        
        const target = status.target_count;
        const progress = status.run_progress;
        const percentage = (target > 0) ? Math.min(100, (progress / target) * 100) : 0;
        
        progressText.textContent = `${Math.round(percentage)}%`;
        progressDetails.textContent = `${progress} / ${target > 0 ? target : '∞'}`;
        const circumference = 2 * Math.PI * 45;
        const offset = circumference - (percentage / 100) * circumference;
        progressPath.style.strokeDashoffset = offset;

        activeProfileDisplay.textContent = status.active_profile;
        activeProfileDisplay.className = `badge ${status.active_profile !== 'None' ? 'bg-info' : 'bg-secondary'}`;
        
        if (status.active_alarm_message) {
            alarmMessage.textContent = status.active_alarm_message;
            alarmBlock.style.display = 'flex';
        } else {
            alarmBlock.style.display = 'none';
        }

        // --- NEW: Update the new detail fields ---
        runDetailBatch.textContent = status.batch_code || 'N/A';
        runDetailOperator.textContent = status.operator_name || 'N/A';
        // --- END NEW ---
    };

    const updateBadge = (id, condition, states = { on: 'ON', off: 'OFF' }) => {
        const el = document.getElementById(id);
        if (!el) return;
        el.textContent = (condition ? states.on : states.off).toUpperCase();
        el.className = `status-badge ${condition ? 'ok' : 'error'}`;
    };

    const triggerBoxAnimation = () => {
        const box = document.createElement('div');
        box.className = 'box';
        conveyorBelt.appendChild(box);
        box.style.animation = `move-box ${animationTime / 1000}s linear forwards`;
        setTimeout(() => box.remove(), animationTime);
    };

    const apiPost = (endpoint, data = {}) => {
        return fetch(`/api/v1${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
    };
    
    // --- Event Listeners (no changes in this section) ---
    startRunBtn.addEventListener('click', async () => {
        if (!profileSelect.value) return alert('Please select an Object Profile (Recipe) first.');
        try {
            const operators = await (await fetch('/api/v1/operators/')).json();
            operatorSelect.innerHTML = '<option value="">-- Select Operator --</option>' + operators
                .filter(op => op.status === 'Active')
                .map(op => `<option value="${op.id}">${op.name}</option>`).join('');
            preRunInputView.style.display = 'block';
            preRunConfirmView.style.display = 'none';
            batchCodeInput.value = `B${new Date().toISOString().slice(0,10).replace(/-/g,"")}-${Date.now().toString().slice(-5)}`;
            preRunModal.show();
        } catch (e) {
            alert('Could not load operators. Please check the Operator Master.');
        }
    });

    reviewRunBtn.addEventListener('click', () => {
        if (!operatorSelect.value || !batchCodeInput.value) return alert('Operator and Batch Code are required.');
        document.getElementById('confirm-operator').textContent = operatorSelect.options[operatorSelect.selectedIndex].text;
        document.getElementById('confirm-batch-code').textContent = batchCodeInput.value;
        document.getElementById('confirm-recipe').textContent = profileSelect.options[profileSelect.selectedIndex].text;
        document.getElementById('confirm-target').textContent = targetCountInput.value;
        preRunInputView.style.display = 'none';
        preRunConfirmView.style.display = 'block';
    });

    goBackBtn.addEventListener('click', () => {
        preRunInputView.style.display = 'block';
        preRunConfirmView.style.display = 'none';
    });

    startFinalRunBtn.addEventListener('click', async () => {
        const payload = {
            object_profile_id: parseInt(profileSelect.value),
            target_count: parseInt(targetCountInput.value),
            post_batch_delay_sec: parseInt(postBatchDelayInput.value),
            operator_id: parseInt(operatorSelect.value),
            batch_code: batchCodeInput.value
        };
        const response = await apiPost('/orchestration/run/start', payload);
        if (!response.ok) {
            const error = await response.json();
            alert(`Failed to start run: ${error.detail}`);
        }
        preRunModal.hide();
    });

    stopRunBtn.addEventListener('click', () => apiPost('/orchestration/run/stop'));
    resetAllBtn.addEventListener('click', () => {
        if (confirm('This will stop all hardware and reset system state. Are you sure?')) apiPost('/system/reset-all');
    });
    acknowledgeAlarmBtn.addEventListener('click', () => apiPost('/orchestration/run/acknowledge-alarm'));

    manualToggles.forEach(toggle => {
        toggle.addEventListener('change', (e) => {
            const name = e.target.id.replace('control-', '').replace('-toggle', '');
            apiPost(`/outputs/toggle/${name}`);
        });
    });

    cameraSelectBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const camId = e.target.dataset.cameraId;
            liveCameraFeed.src = `/api/v1/camera/stream/${camId}?t=${new Date().getTime()}`;
            liveFeedTitle.textContent = `LIVE CAMERA (${camId.toUpperCase()})`;
        });
    });

    if (cameraSelectBtns.length > 0) cameraSelectBtns[0].click();
    
    // --- Initial Connection ---
    connect();
});