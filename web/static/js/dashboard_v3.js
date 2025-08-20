// rpi_counter_fastapi-apintrigation/web/static/js/dashboard_v3.js

document.addEventListener('DOMContentLoaded', function () {
    // --- STATE MANAGEMENT ---
    let countdownInterval = null; // Holds the interval ID for the batch pause timer
    let activeCameraId = null;

    // --- DOM ELEMENT SELECTORS ---
    // Status Displays
    const countOnBeltEl = document.getElementById('count-on-belt');
    const countExitedEl = document.getElementById('count-exited');
    const conveyorModeEl = document.getElementById('conveyor-mode');
    const conveyorBeltEl = document.getElementById('conveyor-belt');
    const progressPath = document.getElementById('progress-path');
    const progressPercentageEl = document.getElementById('progress-percentage');
    const progressDetailsEl = document.getElementById('progress-details');
    const activeProfileDisplay = document.getElementById('active-profile-display');
    const runDetailBatch = document.getElementById('run-detail-batch');
    const runDetailOperator = document.getElementById('run-detail-operator');

    // Alarm & Countdown Blocks
    const alarmBlock = document.getElementById('run-alarm-block');
    const alarmMessageEl = document.getElementById('run-alarm-message');
    const countdownCard = document.getElementById('countdown-timer-card');
    const countdownTimerEl = document.getElementById('countdown-timer');

    // Control Buttons
    const startRunBtn = document.getElementById('start-run-btn');
    const stopRunBtn = document.getElementById('stop-run-btn');
    const resetAllBtn = document.getElementById('reset-all-btn');
    const acknowledgeAlarmBtn = document.getElementById('acknowledge-alarm-btn');

    // Form Inputs
    const profileSelect = document.getElementById('object-profile-select');
    const targetCountInput = document.getElementById('target-count-input');
    const postBatchDelayInput = document.getElementById('post-batch-delay-input');

    // Pre-Run Modal Elements
    const preRunModal = new bootstrap.Modal(document.getElementById('pre-run-modal'));
    const operatorSelect = document.getElementById('operator-select');
    const batchCodeInput = document.getElementById('batch-code-input');
    const reviewRunBtn = document.getElementById('review-run-btn');
    const goBackBtn = document.getElementById('go-back-btn');
    const startFinalRunBtn = document.getElementById('start-final-run-btn');
    const inputView = document.getElementById('pre-run-input-view');
    const confirmView = document.getElementById('pre-run-confirm-view');

    // Camera & AI Elements
    const cameraSwitcher = document.getElementById('camera-switcher');
    const liveCameraFeed = document.getElementById('live-camera-feed');
    const liveFeedTitle = document.getElementById('live-feed-title');
    const aiFeedCanvas = document.getElementById('ai-feed-canvas');
    const aiDetailsSection = document.getElementById('ai-details-section');
    const aiDetailsQCStatus = document.getElementById('ai-details-qc-status');
    const aiDetailsQCConfidence = document.getElementById('ai-details-qc-confidence');
    const aiDetailsCategoryName = document.getElementById('ai-details-category-name');
    const aiDetailsCategoryConfidence = document.getElementById('ai-details-category-confidence');
    const aiValidationList = document.getElementById('ai-validation-list');


    // --- UTILITY FUNCTIONS ---
    async function postAPI(endpoint, body) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body)
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'API request failed');
            }
            return await response.json();
        } catch (error) {
            console.error(`Error posting to ${endpoint}:`, error);
            alert(`Error: ${error.message}`);
        }
    }

    // --- INITIALIZATION ---
    function initialize() {
        setupWebSocket();
        loadInitialData();
        attachEventListeners();
        setupCameraSwitcher();
    }

    async function loadInitialData() {
        try {
            const [operatorsRes, profilesRes] = await Promise.all([
                fetch('/api/v1/operators/'),
                fetch('/api/v1/profiles/object') // Assuming this is the correct endpoint
            ]);
            
            const operators = await operatorsRes.json();
            operatorSelect.innerHTML = '<option value="">-- Select Operator --</option>';
            operators.forEach(op => {
                if (op.status === 'Active') {
                    const option = new Option(op.name, op.id);
                    operatorSelect.appendChild(option);
                }
            });

            // The object profiles are already loaded via the HTML template, so no need to fetch again.
        } catch (error) {
            console.error("Failed to load initial data:", error);
        }
    }

    function setupCameraSwitcher() {
        const buttons = cameraSwitcher.querySelectorAll('.camera-select-btn');
        buttons.forEach(btn => {
            btn.addEventListener('click', () => {
                const camId = btn.dataset.cameraId;
                setActiveCamera(camId);
                buttons.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
            });
        });

        // Activate the first camera by default
        if (buttons.length > 0) {
            buttons[0].click();
        }
    }

    function setActiveCamera(camId) {
        activeCameraId = camId;
        liveCameraFeed.src = `/api/v1/camera/stream/${camId}`;
        liveFeedTitle.textContent = `LIVE - ${camId.toUpperCase()}`;
    }

    // --- WEBSOCKET HANDLING ---
    function setupWebSocket() {
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
        const socket = new WebSocket(wsUrl);

        socket.onopen = () => console.log("[WebSocket] Connection established.");
        socket.onclose = () => {
            console.error("[WebSocket] Connection died. Attempting to reconnect in 3 seconds...");
            setTimeout(setupWebSocket, 3000);
        };
        socket.onerror = (error) => console.error(`[WebSocket] Error: ${error.message}`);
        socket.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                handleWebSocketMessage(data);
            } catch (e) {
                console.warn("Received non-JSON message:", event.data);
            }
        };
    }

    function handleWebSocketMessage(data) {
        if (data.type === 'full_status') {
            const { system, orchestration } = data.data;
            updateSystemStatus(system);
            updateOrchestrationStatus(orchestration);
        } else if (data.type === 'qc_update') {
            updateCameraFeeds(data.data);
            updateAIDetails(data.data);
        }
    }

    // --- UI UPDATE FUNCTIONS ---
    function updateSystemStatus(system) {
        countOnBeltEl.textContent = system.in_flight_count;

        // Update manual toggle switches based on their actual state
        document.querySelectorAll('.manual-control-toggle input').forEach(toggle => {
            const controlName = toggle.dataset.controlName;
            const statusKey = `${controlName}_relay_status`;
            if (statusKey in system) {
                toggle.checked = system[statusKey];
            }
        });
    }

    function updateOrchestrationStatus(orchestration) {
        conveyorModeEl.textContent = orchestration.mode.toUpperCase();
        countExitedEl.textContent = orchestration.run_progress;
        
        // Toggle conveyor animation
        const isRunning = orchestration.mode === 'Running' || orchestration.mode === 'Post-Run Delay';
        conveyorBeltEl.classList.toggle('running', isRunning);

        // Update run details
        activeProfileDisplay.textContent = orchestration.active_profile || 'None';
        runDetailBatch.textContent = orchestration.batch_code || 'N/A';
        runDetailOperator.textContent = orchestration.operator_name || 'N/A';

        // Update UI components based on state
        updateRunStatusProgress(orchestration);
        updateAlarmBlock(orchestration);
        updateCountdownTimer(orchestration);
    }

    function updateRunStatusProgress(orchestration) {
        const { run_progress, target_count } = orchestration;
        const percentage = (target_count > 0) ? (run_progress / target_count) * 100 : 0;
        const circumference = 2 * Math.PI * 45; // r=45
        const offset = circumference - (percentage / 100) * circumference;
        
        progressPath.style.strokeDasharray = `${circumference} ${circumference}`;
        progressPath.style.strokeDashoffset = offset;
        progressPercentageEl.textContent = `${Math.min(100, Math.round(percentage))}%`;
        progressDetailsEl.textContent = `${run_progress} / ${target_count === 0 ? '∞' : target_count}`;
    }

    function updateAlarmBlock(orchestration) {
        if (orchestration.active_alarm_message) {
            alarmMessageEl.textContent = orchestration.active_alarm_message;
            alarmBlock.style.display = 'flex';
        } else {
            alarmBlock.style.display = 'none';
        }
    }

    function updateCountdownTimer(orchestration) {
        if (orchestration.mode === 'Paused (Between Batches)' && orchestration.pause_start_time) {
            countdownCard.style.display = 'block';
            if (countdownInterval) clearInterval(countdownInterval); // Prevent duplicates

            const startTime = new Date(orchestration.pause_start_time).getTime();
            const durationMs = orchestration.post_batch_delay_sec * 1000;
            const endTime = startTime + durationMs;

            countdownInterval = setInterval(() => {
                const remaining = Math.max(0, endTime - Date.now());
                if (remaining === 0) {
                    countdownTimerEl.textContent = "00:00";
                    clearInterval(countdownInterval);
                    countdownInterval = null; 
                } else {
                    const seconds = Math.floor((remaining / 1000) % 60).toString().padStart(2, '0');
                    const minutes = Math.floor(remaining / (1000 * 60)).toString().padStart(2, '0');
                    countdownTimerEl.textContent = `${minutes}:${seconds}`;
                }
            }, 500);
        } else {
            countdownCard.style.display = 'none';
            if (countdownInterval) {
                clearInterval(countdownInterval);
                countdownInterval = null;
            }
        }
    }
    
    function updateCameraFeeds(qcData) {
        // We only care about the annotated image for the AI feed
        const ctx = aiFeedCanvas.getContext('2d');
        const img = new Image();
        img.onload = () => {
            aiFeedCanvas.width = img.width;
            aiFeedCanvas.height = img.height;
            ctx.drawImage(img, 0, 0);
        };
        img.src = qcData.annotated_path;
    }

    function updateAIDetails(qcData) {
        aiDetailsSection.style.display = 'block';
        const qcSummary = qcData.results.qc_summary || {};
        const catSummary = qcData.results.category_summary || {};
        const validation = qcData.results.validation_results || { checks: [] };

        aiDetailsQCStatus.textContent = qcSummary.overall_status || 'N/A';
        aiDetailsQCStatus.className = `status-${qcSummary.overall_status}`;
        aiDetailsQCConfidence.textContent = qcSummary.confidence ? `${(qcSummary.confidence * 100).toFixed(1)}%` : '--';

        aiDetailsCategoryName.textContent = catSummary.detected_type || 'N/A';
        aiDetailsCategoryConfidence.textContent = catSummary.confidence ? `${(catSummary.confidence * 100).toFixed(1)}%` : '--';

        aiValidationList.innerHTML = '';
        if (validation.checks.length > 0) {
            validation.checks.forEach(check => {
                const li = document.createElement('li');
                li.className = 'list-group-item d-flex justify-content-between align-items-center';
                li.innerHTML = `
                    <span>${check.check_type}: <span class="fw-bold">${check.value}</span></span>
                    <span class="badge ${check.status === 'PASS' ? 'bg-success' : 'bg-danger'}">${check.status}</span>
                `;
                aiValidationList.appendChild(li);
            });
        } else {
            aiValidationList.innerHTML = '<li class="list-group-item text-muted">No geometric validation enabled.</li>';
        }
    }


    // --- EVENT LISTENERS ---
    function attachEventListeners() {
        startRunBtn.addEventListener('click', handleStartRunClick);
        stopRunBtn.addEventListener('click', () => postAPI('/api/v1/orchestration/run/stop', {}));
        resetAllBtn.addEventListener('click', () => postAPI('/api/v1/system/reset-all', {}));
        acknowledgeAlarmBtn.addEventListener('click', () => postAPI('/api/v1/orchestration/run/acknowledge-alarm', {}));
        
        document.querySelectorAll('.manual-control-toggle input').forEach(toggle => {
            toggle.addEventListener('change', (e) => {
                postAPI(`/api/v1/outputs/toggle/${e.target.dataset.controlName}`, {});
            });
        });

        // Modal Listeners
        reviewRunBtn.addEventListener('click', handleReviewRun);
        goBackBtn.addEventListener('click', () => {
            confirmView.style.display = 'none';
            inputView.style.display = 'block';
        });
        startFinalRunBtn.addEventListener('click', handleFinalStart);
    }

    function handleStartRunClick() {
        if (!profileSelect.value) {
            alert("Please select an Object Profile (Recipe) before starting a run.");
            return;
        }
        // Reset modal to initial state
        inputView.style.display = 'block';
        confirmView.style.display = 'none';
        batchCodeInput.value = '';
        operatorSelect.selectedIndex = 0;
        preRunModal.show();
    }
    
    function handleReviewRun() {
        if (!operatorSelect.value || !batchCodeInput.value) {
            alert("Operator and Batch Code are required.");
            return;
        }
        document.getElementById('confirm-operator').textContent = operatorSelect.options[operatorSelect.selectedIndex].text;
        document.getElementById('confirm-batch-code').textContent = batchCodeInput.value;
        document.getElementById('confirm-recipe').textContent = profileSelect.options[profileSelect.selectedIndex].text;
        document.getElementById('confirm-target').textContent = targetCountInput.value === '0' ? 'Continuous (∞)' : targetCountInput.value;

        inputView.style.display = 'none';
        confirmView.style.display = 'block';
    }

    function handleFinalStart() {
        const payload = {
            object_profile_id: parseInt(profileSelect.value),
            target_count: parseInt(targetCountInput.value),
            post_batch_delay_sec: parseInt(postBatchDelayInput.value),
            batch_code: batchCodeInput.value,
            operator_id: parseInt(operatorSelect.value)
        };
        
        postAPI('/api/v1/orchestration/run/start', payload);
        preRunModal.hide();
    }

    // --- KICK IT OFF ---
    initialize();
});