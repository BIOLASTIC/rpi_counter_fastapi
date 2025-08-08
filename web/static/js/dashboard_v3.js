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
    const startRunBtn = document.getElementById('start-run-btn');
    const stopRunBtn = document.getElementById('stop-run-btn');
    const resetAllBtn = document.getElementById('reset-all-btn');

    // PHASE 4: Pre-Run Modal Elements
    const preRunModal = new bootstrap.Modal(document.getElementById('pre-run-modal'));
    const operatorSelect = document.getElementById('operator-select');
    const batchCodeInput = document.getElementById('batch-code-input');
    const reviewRunBtn = document.getElementById('review-run-btn');
    const goBackBtn = document.getElementById('go-back-btn');
    const startFinalRunBtn = document.getElementById('start-final-run-btn');
    const inputView = document.getElementById('pre-run-input-view');
    const confirmView = document.getElementById('pre-run-confirm-view');

    // PHASE 4: Alarm Block Elements
    const alarmBlock = document.getElementById('run-alarm-block');
    const alarmMessageEl = document.getElementById('run-alarm-message');
    const acknowledgeAlarmBtn = document.getElementById('acknowledge-alarm-btn');
    
    // --- Helper Functions ---
    async function apiPost(endpoint) {
        try {
            const response = await fetch(endpoint, { method: 'POST' });
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

    // --- PHASE 4: New Run Workflow Logic ---
    let runConfig = {}; // Store selections between modal views

    // 1. Populate Operators on Load
    async function loadOperators() {
        try {
            const response = await fetch('/api/v1/operators');
            const operators = await response.json();
            operatorSelect.innerHTML = '<option value="">-- Select Operator --</option>';
            operators.filter(op => op.status === 'Active').forEach(op => {
                operatorSelect.innerHTML += `<option value="${op.id}">${op.name}</option>`;
            });
        } catch (error) {
            console.error('Failed to load operators', error);
        }
    }
    loadOperators();
    
    // 2. Main "Load & Start Run" button now opens the modal
    startRunBtn.addEventListener('click', () => {
        const profileId = document.getElementById('object-profile-select').value;
        const targetCount = document.getElementById('target-count-input').value;

        if (!profileId) {
            alert('Please select a Recipe first.');
            return;
        }

        runConfig = {
            object_profile_id: parseInt(profileId),
            target_count: parseInt(targetCount),
            post_batch_delay_sec: 5 // Or get from an input if you add one
        };

        // Reset and show the modal's input view
        inputView.style.display = 'block';
        confirmView.style.display = 'none';
        operatorSelect.value = '';
        batchCodeInput.value = '';
        document.getElementById('pre-run-modal-title').textContent = 'Pre-Run Checklist';
        preRunModal.show();
    });

    // 3. "Review Run" button switches to the confirmation view
    reviewRunBtn.addEventListener('click', () => {
        const operatorId = operatorSelect.value;
        const batchCode = batchCodeInput.value.trim();

        if (!operatorId || !batchCode) {
            alert('Please select an operator and enter a batch code.');
            return;
        }

        runConfig.operator_id = parseInt(operatorId);
        runConfig.batch_code = batchCode;

        // Populate confirmation view
        document.getElementById('confirm-operator').textContent = operatorSelect.options[operatorSelect.selectedIndex].text;
        document.getElementById('confirm-batch-code').textContent = batchCode;
        const profileSelect = document.getElementById('object-profile-select');
        document.getElementById('confirm-recipe').textContent = profileSelect.options[profileSelect.selectedIndex].text;
        document.getElementById('confirm-target').textContent = runConfig.target_count === 0 ? 'Unlimited' : runConfig.target_count;
        
        // Switch views
        document.getElementById('pre-run-modal-title').textContent = 'Confirm Run Details';
        inputView.style.display = 'none';
        confirmView.style.display = 'block';
    });

    // 4. "Go Back" button switches back to the input view
    goBackBtn.addEventListener('click', () => {
        document.getElementById('pre-run-modal-title').textContent = 'Pre-Run Checklist';
        confirmView.style.display = 'none';
        inputView.style.display = 'block';
    });

    // 5. "START FINAL RUN" button sends the API request
    startFinalRunBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/v1/orchestration/run/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(runConfig)
            });
            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.detail || 'Failed to start run');
            }
            preRunModal.hide();
        } catch (error) {
            alert(`Error starting run: ${error.message}`);
        }
    });

    // --- Other Controls ---
    stopRunBtn.addEventListener('click', () => apiPost('/api/v1/orchestration/run/stop'));
    resetAllBtn.addEventListener('click', () => apiPost('/api/v1/system/reset-all'));
    
    // --- PHASE 4: Acknowledge Alarm ---
    acknowledgeAlarmBtn.addEventListener('click', () => apiPost('/api/v1/orchestration/run/acknowledge-alarm'));

    // --- UI Update Function ---
    function updateUI(data) {
        const { system, orchestration } = data;

        // PHASE 4: Handle alarms
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
        const percentage = (target > 0 && progress > 0) ? Math.round((progress / target) * 100) : 0;
        
        const progressPath = document.getElementById('progress-path');
        const circumference = 2 * Math.PI * 45; // 2 * pi * radius
        const offset = circumference - (percentage / 100) * circumference;
        progressPath.style.strokeDashoffset = offset;
        
        document.getElementById('progress-percentage').textContent = `${percentage}%`;
        document.getElementById('progress-details').textContent = `${progress} / ${target === 0 ? '∞' : target}`;

        // Conveyor Animation
        const conveyorBelt = document.getElementById('conveyor-belt');
        conveyorBelt.classList.toggle('running', orchestration.mode === 'Running');
    }
});