// /static/js/dashboard_v3.js

document.addEventListener('DOMContentLoaded', function () {
    // --- Application State ---
    let appState = {
        system: {},
        orchestration: {},
        ui: {
            activeCameraId: document.querySelector('.camera-select-btn')?.dataset.cameraId || null,
            countdownInterval: null,
            preRunModal: new bootstrap.Modal(document.getElementById('pre-run-modal')),
        }
    };

    // --- DOM Element Cache ---
    const ui = new Map(
        Array.from(document.querySelectorAll('[id]')).map(el => [el.id, el])
    );

    // --- WebSocket Connection Manager ---
    function setupWebSocket() {
        console.log("Attempting to connect WebSocket...");
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
        const socket = new WebSocket(wsUrl);

        socket.onopen = () => console.log("[WebSocket] Connection established.");
        socket.onclose = () => {
            console.error('[WebSocket] Connection died. Reconnecting in 5s...');
            setTimeout(setupWebSocket, 5000);
        };
        socket.onerror = (error) => {
            console.error(`[WebSocket] Error: ${error.message}`);
            socket.close();
        };
        socket.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                if (message.type === 'full_status') {
                    appState.system = message.data.system || appState.system;
                    appState.orchestration = message.data.orchestration || appState.orchestration;
                    updateFullUI();
                }
            } catch (e) {
                console.warn("Received non-JSON message from WebSocket:", event.data);
            }
        };
    }

    // --- Main UI Update Function ---
    function updateFullUI() {
        updateSystemStatusUI(appState.system);
        updateOrchestrationStatusUI(appState.orchestration);
    }

    // --- UI Update Sub-routines ---
    function updateSystemStatusUI(system) {
        if (!system) return;

        updateToggleSwitch('conveyor', system.conveyor_relay_status);
        updateToggleSwitch('gate', system.gate_relay_status);
        updateToggleSwitch('diverter', system.diverter_relay_status);
        updateToggleSwitch('led_green', system.led_green_status);
        updateToggleSwitch('led_red', system.led_red_status);
        updateToggleSwitch('camera_light', system.camera_light_status);
        updateToggleSwitch('camera_light_two', system.camera_light_two_status);
        updateToggleSwitch('buzzer', system.buzzer_status);

        updateBadge('status-sensor-1', system.sensor_1_status ? 'BLOCKED' : 'CLEAR', system.sensor_1_status ? 'error' : 'ok');
        updateBadge('status-sensor-2', system.sensor_2_status ? 'BLOCKED' : 'CLEAR', system.sensor_2_status ? 'error' : 'ok');
        updateBadge('status-io-module', system.io_module_status, system.io_module_status === 'ok' ? 'ok' : 'error');
        
        ui.get('count-on-belt').textContent = system.in_flight_count;
    }

    function updateOrchestrationStatusUI(orch) {
        if (!orch) return;
        ui.get('count-exited').textContent = orch.run_progress;
        ui.get('conveyor-mode').textContent = orch.mode.toUpperCase();
        ui.get('conveyor-belt').classList.toggle('running', orch.mode === 'Running');
        ui.get('active-profile-display').textContent = orch.active_profile || 'None';
        ui.get('run-detail-batch').textContent = orch.batch_code || 'N/A';
        ui.get('run-detail-operator').textContent = orch.operator_name || 'N/A';
        updateProgressCircle(orch.run_progress, orch.target_count);
        handleAlarm(orch.active_alarm_message);
        handleCountdown(orch.mode, orch.pause_start_time, orch.post_batch_delay_sec);
    }
    
    // --- UI Helper Functions ---
    function updateToggleSwitch(name, isActive) {
        const toggle = document.querySelector(`input[data-control-name="${name}"]`);
        if (toggle && toggle.checked !== isActive) {
            toggle.checked = isActive;
        }
    }

    function updateBadge(elementId, text, statusClass) {
        const badge = ui.get(elementId);
        if (badge) {
            badge.textContent = text ? text.toUpperCase() : '--';
            badge.className = 'status-badge';
            if (statusClass) badge.classList.add(statusClass);
        }
    }

    function updateProgressCircle(current, target) {
        const percentage = (target > 0) ? Math.min(100, (current / target) * 100) : 0;
        const circumference = 2 * Math.PI * 45;
        const offset = circumference - (percentage / 100) * circumference;
        const path = ui.get('progress-path');
        if(path) {
            path.style.strokeDasharray = `${circumference} ${circumference}`;
            path.style.strokeDashoffset = offset;
        }
        ui.get('progress-percentage').textContent = `${Math.round(percentage)}%`;
        ui.get('progress-details').textContent = `${current} / ${target > 0 ? target : '∞'}`;
    }
    
    function handleAlarm(message) {
        const block = ui.get('run-alarm-block');
        if (block) {
            block.style.display = message ? 'flex' : 'none';
            ui.get('run-alarm-message').textContent = message || '';
        }
    }

    function handleCountdown(mode, startTimeStr, delaySec) {
        const card = ui.get('countdown-timer-card');
        if (mode === 'Paused (Between Batches)' && startTimeStr) {
            card.style.display = 'block';
            if (!appState.ui.countdownInterval) {
                const endTime = new Date(new Date(startTimeStr).getTime() + delaySec * 1000);
                appState.ui.countdownInterval = setInterval(() => {
                    const remaining = endTime - new Date();
                    if (remaining <= 0) {
                        clearInterval(appState.ui.countdownInterval);
                        appState.ui.countdownInterval = null;
                        ui.get('countdown-timer').textContent = '00:00';
                        card.style.display = 'none';
                    } else {
                        const minutes = String(Math.floor((remaining / 1000) / 60)).padStart(2, '0');
                        const seconds = String(Math.floor((remaining / 1000) % 60)).padStart(2, '0');
                        ui.get('countdown-timer').textContent = `${minutes}:${seconds}`;
                    }
                }, 1000);
            }
        } else {
            if (appState.ui.countdownInterval) {
                clearInterval(appState.ui.countdownInterval);
                appState.ui.countdownInterval = null;
            }
            card.style.display = 'none';
        }
    }
    
    // --- Event Listeners ---
    document.querySelectorAll('.manual-control-toggle input[type="checkbox"]').forEach(toggle => {
        toggle.addEventListener('click', function(event) {
            event.preventDefault(); 
            const controlName = this.dataset.controlName;
            fetch(`/api/v1/outputs/toggle/${controlName}`, { method: 'POST' })
                .catch(error => console.error(`Error toggling ${controlName}:`, error));
        });
    });

    ui.get('acknowledge-alarm-btn')?.addEventListener('click', () => {
        fetch('/api/v1/orchestration/run/acknowledge-alarm', { method: 'POST' });
    });

    ui.get('start-run-btn')?.addEventListener('click', () => {
        populateOperatorSelect();
        ui.get('pre-run-input-view').style.display = 'block';
        ui.get('pre-run-confirm-view').style.display = 'none';
        appState.ui.preRunModal.show();
    });

    ui.get('review-run-btn')?.addEventListener('click', function() {
        const operatorSelect = ui.get('operator-select');
        const batchCodeInput = ui.get('batch-code-input');
        if (!operatorSelect.value || !batchCodeInput.value) {
            alert('Operator and Batch Code are required.');
            return;
        }
        document.getElementById('confirm-operator').textContent = operatorSelect.options[operatorSelect.selectedIndex].text;
        document.getElementById('confirm-batch-code').textContent = batchCodeInput.value;
        document.getElementById('confirm-recipe').textContent = ui.get('object-profile-select').options[ui.get('object-profile-select').selectedIndex].text;
        document.getElementById('confirm-target').textContent = ui.get('target-count-input').value > 0 ? ui.get('target-count-input').value : 'Continuous';
        ui.get('pre-run-input-view').style.display = 'none';
        ui.get('pre-run-confirm-view').style.display = 'block';
    });

    ui.get('go-back-btn')?.addEventListener('click', () => {
        ui.get('pre-run-input-view').style.display = 'block';
        ui.get('pre-run-confirm-view').style.display = 'none';
    });

    ui.get('start-final-run-btn')?.addEventListener('click', startRun);

    ui.get('stop-run-btn')?.addEventListener('click', () => {
        fetch('/api/v1/orchestration/run/stop', { method: 'POST' });
    });

    ui.get('reset-all-btn')?.addEventListener('click', () => {
        if (confirm('Are you sure you want to perform a full system reset? This will stop all hardware and clear the current run state.')) {
            fetch('/api/v1/system/reset-all', { method: 'POST' });
        }
    });

    ui.get('camera-switcher')?.addEventListener('click', (e) => {
        if (e.target.classList.contains('camera-select-btn')) {
            switchCamera(e.target.dataset.cameraId);
        }
    });
    
    // --- API & Helper Functions ---
    async function populateOperatorSelect() {
        try {
            const response = await fetch('/api/v1/operators/');
            const operators = await response.json();
            const operatorSelect = ui.get('operator-select');
            operatorSelect.innerHTML = '<option value="">-- Select Operator --</option>';
            operators.filter(op => op.status === 'Active').forEach(op => {
                operatorSelect.add(new Option(op.name, op.id));
            });
        } catch (error) {
            console.error('Failed to load operators:', error);
        }
    }

    async function startRun() {
        const payload = {
            object_profile_id: parseInt(ui.get('object-profile-select').value, 10),
            target_count: parseInt(ui.get('target-count-input').value, 10),
            post_batch_delay_sec: parseInt(ui.get('post-batch-delay-input').value, 10),
            batch_code: ui.get('batch-code-input').value,
            operator_id: parseInt(ui.get('operator-select').value, 10),
        };
        
        try {
            const response = await fetch('/api/v1/orchestration/run/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload),
            });
            if (!response.ok) {
                const errorData = await response.json();
                alert(`Failed to start run: ${errorData.detail}`);
            }
        } catch (error) {
            alert(`An error occurred: ${error.message}`);
        }
        appState.ui.preRunModal.hide();
    }

    function switchCamera(camId) {
        appState.ui.activeCameraId = camId;
        ui.get('live-camera-feed').src = `/api/v1/camera/stream/${camId}?t=${new Date().getTime()}`;
        ui.get('live-feed-title').textContent = `LIVE - ${camId.toUpperCase()}`;
        document.querySelectorAll('.camera-select-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.cameraId === camId);
        });
    }

    // --- Initial Load ---
    setupWebSocket();
    if (appState.ui.activeCameraId) {
        switchCamera(appState.ui.activeCameraId);
    }
});