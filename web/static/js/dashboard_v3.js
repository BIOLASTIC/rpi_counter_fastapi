// /static/js/dashboard_v3.js

document.addEventListener('DOMContentLoaded', function () {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
    let socket;

    // --- DOM Element Cache ---
    const elements = {
        // Main Dashboard & Animation
        countExited: document.getElementById('count-exited'),
        countOnBelt: document.getElementById('count-on-belt'),
        conveyorMode: document.getElementById('conveyor-mode'),
        conveyorBelt: document.getElementById('conveyor-belt'),
        animationZone: document.getElementById('animation-zone'),
        // Run Status & Details
        progressPath: document.getElementById('progress-path'),
        progressPercentage: document.getElementById('progress-percentage'),
        progressDetails: document.getElementById('progress-details'),
        activeProfileDisplay: document.getElementById('active-profile-display'),
        runDetailBatch: document.getElementById('run-detail-batch'),
        runDetailOperator: document.getElementById('run-detail-operator'),
        // Camera & AI Feeds
        liveCameraFeed: document.getElementById('live-camera-feed'),
        aiFeedCanvas: document.getElementById('ai-feed-canvas'),
        aiFeedCtx: document.getElementById('ai-feed-canvas').getContext('2d'),
        liveFeedTitle: document.getElementById('live-feed-title'),
        cameraSwitcher: document.getElementById('camera-switcher'),
        // AI Text Summary
        aiDetailsSection: document.getElementById('ai-details-section'),
        aiDetailsQc: document.getElementById('ai-details-qc'),
        aiDetailsCategory: document.getElementById('ai-details-category'),
        aiDetailsSize: document.getElementById('ai-details-size'),
        aiDetailsDefects: document.getElementById('ai-details-defects'),
        // Alarm
        runAlarmBlock: document.getElementById('run-alarm-block'),
        runAlarmMessage: document.getElementById('run-alarm-message'),
        // Modals & Controls
        preRunModal: new bootstrap.Modal(document.getElementById('pre-run-modal')),
        startRunBtn: document.getElementById('start-run-btn'),
        stopRunBtn: document.getElementById('stop-run-btn'),
        resetAllBtn: document.getElementById('reset-all-btn'),
        acknowledgeAlarmBtn: document.getElementById('acknowledge-alarm-btn'),
        objectProfileSelect: document.getElementById('object-profile-select'),
        targetCountInput: document.getElementById('target-count-input'),
        postBatchDelayInput: document.getElementById('post-batch-delay-input'),
        operatorSelect: document.getElementById('operator-select'),
        batchCodeInput: document.getElementById('batch-code-input'),
        reviewRunBtn: document.getElementById('review-run-btn'),
        goBackBtn: document.getElementById('go-back-btn'),
        startFinalRunBtn: document.getElementById('start-final-run-btn'),
        confirmOperator: document.getElementById('confirm-operator'),
        confirmBatchCode: document.getElementById('confirm-batch-code'),
        confirmRecipe: document.getElementById('confirm-recipe'),
        confirmTarget: document.getElementById('confirm-target'),
        preRunInputView: document.getElementById('pre-run-input-view'),
        preRunConfirmView: document.getElementById('pre-run-confirm-view'),
        statusIoModule: document.getElementById('status-io-module'),
        statusSensor1: document.getElementById('status-sensor-1'),
        statusSensor2: document.getElementById('status-sensor-2'),
    };

    // --- THIS IS THE FIX (Part 1) ---
    // Use 'lastInFlightCount' as the trigger instead of the processed count.
    let lastInFlightCount = 0;
    // --- END OF FIX ---
    let selectedCameraId = elements.cameraSwitcher?.querySelector('.camera-select-btn')?.dataset.cameraId || 'rpi';

    function connect() {
        socket = new WebSocket(wsUrl);
        socket.onopen = () => console.log("[WebSocket] Connection established.");
        socket.onclose = (event) => { setTimeout(connect, 1000); };
        socket.onerror = (error) => console.error(`[WebSocket] Error: ${error.message}`);
        socket.onmessage = handleWebSocketMessage;
    }

    function handleWebSocketMessage(event) {
        try {
            const message = JSON.parse(event.data);
            if (message.type === 'full_status') {
                updateDashboard(message.data);
            } else if (message.type === 'qc_update') {
                updateAiFeed(message.data);
            }
        } catch (e) {
            console.warn("Received non-JSON message:", event.data);
        }
    }
    
    function updateAiFeed(data) {
        if (!data || !data.original_path) return;
        const { annotated_path, original_path, results } = data;
        const imageToLoad = (annotated_path && annotated_path !== original_path) ? annotated_path : original_path;
        const img = new Image();
        img.crossOrigin = "anonymous";
        img.onload = () => {
            const canvas = elements.aiFeedCanvas;
            const ctx = elements.aiFeedCtx;
            const aspectRatio = img.naturalWidth / img.naturalHeight;
            canvas.width = canvas.clientWidth;
            canvas.height = canvas.clientWidth / aspectRatio;
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
            updateAiDetails(results);
            if (annotated_path === original_path) {
                ctx.fillStyle = 'rgba(0, 0, 0, 0.6)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = 'white';
                ctx.font = 'bold 24px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('No Annotation Available', canvas.width / 2, canvas.height / 2);
            }
        };
        img.src = `${imageToLoad}?t=${new Date().getTime()}`;
    }

    function updateAiDetails(results) {
        if (!results) {
            elements.aiDetailsSection.style.display = 'none';
            return;
        }
        const idResults = results.identification_results || {};
        const qc = idResults.qc;
        if (qc && qc.overall_status) {
            let qcText = qc.overall_status;
            if (qc.rejection_reason) {
                qcText += ` (${qc.rejection_reason})`;
            }
            elements.aiDetailsQc.textContent = qcText;
            elements.aiDetailsQc.className = `detail-value status-${qc.overall_status.toLowerCase()}`;
        } else {
            elements.aiDetailsQc.textContent = 'N/A';
            elements.aiDetailsQc.className = 'detail-value';
        }
        const category = idResults.category;
        elements.aiDetailsCategory.textContent = category && category.detected_product_type ? `${category.detected_product_type} (${(category.confidence * 100).toFixed(1)}%)` : 'N/A';
        const size = idResults.size;
        elements.aiDetailsSize.textContent = (size && size.detected_product_size) ? size.detected_product_size : 'N/A';
        const defects = idResults.defects && idResults.defects.defects ? idResults.defects.defects : [];
        elements.aiDetailsDefects.textContent = defects.length > 0 ? `${defects.length} Found` : 'None Detected';
        elements.aiDetailsSection.style.display = 'block';
    }

    function updateDashboard(data) {
        const { system, orchestration } = data;
        elements.countExited.textContent = orchestration.run_progress;
        elements.countOnBelt.textContent = system.in_flight_count;
        elements.conveyorMode.textContent = orchestration.mode;
        const isRunning = orchestration.mode !== 'Stopped';
        elements.conveyorBelt.classList.toggle('running', isRunning);

        // --- THIS IS THE FIX (Part 2) ---
        // The animation is now triggered by the increase of the in-flight count.
        const currentInFlightCount = system.in_flight_count;
        if (currentInFlightCount > lastInFlightCount) {
            triggerBoxAnimation();
        }
        lastInFlightCount = currentInFlightCount;
        // The old trigger based on 'run_progress' has been removed.
        // --- END OF FIX ---

        updateProgressCircle(orchestration.run_progress, orchestration.target_count);
        elements.activeProfileDisplay.textContent = orchestration.active_profile || 'None';
        elements.runDetailBatch.textContent = orchestration.batch_code || 'N/A';
        elements.runDetailOperator.textContent = orchestration.operator_name || 'N/A';
        updateAlarm(orchestration.active_alarm_message);
        updateSystemToggles(system, isRunning);
        updateStatusBadge(elements.statusIoModule, system.io_module_status);
        updateStatusBadge(elements.statusSensor1, system.sensor_1_status, {true: 'TRIGGERED', false: 'CLEAR'});
        updateStatusBadge(elements.statusSensor2, system.sensor_2_status, {true: 'TRIGGERED', false: 'CLEAR'});
    }
    
    function triggerBoxAnimation() {
        const box = document.createElement('div');
        box.className = 'box';
        const animationTime = elements.animationZone.dataset.animationTime || 5;
        box.style.animation = `move-box ${animationTime}s linear forwards`;
        elements.animationZone.appendChild(box);
        setTimeout(() => box.remove(), animationTime * 1000);
    }

    function updateProgressCircle(current, target) {
        const percentage = (target > 0) ? Math.min(100, (current / target) * 100) : 0;
        const circumference = 2 * Math.PI * 45;
        const offset = circumference - (percentage / 100) * circumference;
        elements.progressPath.style.strokeDashoffset = offset;
        elements.progressPercentage.textContent = `${Math.round(percentage)}%`;
        elements.progressDetails.textContent = `${current} / ${(target === 0) ? '∞' : target}`;
    }

    function updateAlarm(alarmMessage) {
        elements.runAlarmBlock.style.display = alarmMessage ? 'flex' : 'none';
        elements.runAlarmMessage.textContent = alarmMessage || '';
    }

    function updateStatusBadge(element, status, textMap = {}) {
        if (!element) return;
        if (typeof status === 'boolean') {
            element.textContent = textMap[status] || (status ? 'ON' : 'OFF');
            element.className = `status-badge ${status ? 'warn' : 'clear'}`;
        } else {
            element.textContent = status || '--';
            element.className = 'status-badge';
            if (status === 'ok') element.classList.add('ok');
            else if (status) element.classList.add('error');
        }
    }

    function updateSystemToggles(system, isRunning) {
        document.querySelectorAll('.manual-control-toggle').forEach(container => {
            const toggle = container.querySelector('input[type="checkbox"]');
            if (!toggle) return;
            const key = toggle.id.replace('control-', '').replace('-toggle', '');
            const statusKey = `${key}_relay_status`;
            if (system && typeof system[statusKey] !== 'undefined') {
                toggle.checked = system[statusKey];
            }
            toggle.disabled = isRunning;
            if (isRunning) {
                container.setAttribute('data-bs-toggle', 'tooltip');
                container.setAttribute('data-bs-title', 'Controls locked during active run');
                bootstrap.Tooltip.getOrCreateInstance(container).enable();
            } else {
                bootstrap.Tooltip.getOrCreateInstance(container).disable();
                container.removeAttribute('data-bs-toggle');
                container.removeAttribute('data-bs-title');
            }
        });
    }

    async function sendApiRequest(endpoint, method = 'POST', body = null) {
        try {
            console.log(`Sending API request: ${method} ${endpoint}`);
            const options = { method, headers: { 'Content-Type': 'application/json' } };
            if (body) options.body = JSON.stringify(body);
            const response = await fetch(`/api/v1${endpoint}`, options);
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'API request failed');
            }
            return await response.json();
        } catch (error) {
            console.error(`API Error for ${endpoint}:`, error);
            alert(`Error: ${error.message}`);
        }
    }

    function setupEventListeners() {
        elements.startRunBtn.addEventListener('click', () => {
            if (!elements.objectProfileSelect.value) return alert('Please select an Object Profile (Recipe) before starting.');
            elements.preRunInputView.style.display = 'block';
            elements.preRunConfirmView.style.display = 'none';
            loadOperators();
            elements.preRunModal.show();
        });
        elements.reviewRunBtn.addEventListener('click', () => {
            if (!elements.operatorSelect.value || !elements.batchCodeInput.value) return alert('Please select an operator and enter a batch code.');
            elements.confirmOperator.textContent = elements.operatorSelect.options[elements.operatorSelect.selectedIndex].text;
            elements.confirmBatchCode.textContent = elements.batchCodeInput.value;
            elements.confirmRecipe.textContent = elements.objectProfileSelect.options[elements.objectProfileSelect.selectedIndex].text;
            elements.confirmTarget.textContent = elements.targetCountInput.value === '0' ? 'Unlimited' : elements.targetCountInput.value;
            elements.preRunInputView.style.display = 'none';
            elements.preRunConfirmView.style.display = 'block';
        });
        elements.goBackBtn.addEventListener('click', () => {
            elements.preRunInputView.style.display = 'block';
            elements.preRunConfirmView.style.display = 'none';
        });
        elements.startFinalRunBtn.addEventListener('click', async () => {
            const payload = {
                object_profile_id: parseInt(elements.objectProfileSelect.value),
                target_count: parseInt(elements.targetCountInput.value),
                post_batch_delay_sec: parseInt(elements.postBatchDelayInput.value),
                operator_id: parseInt(elements.operatorSelect.value),
                batch_code: elements.batchCodeInput.value
            };
            await sendApiRequest('/orchestration/run/start', 'POST', payload);
            elements.preRunModal.hide();
        });
        elements.stopRunBtn.addEventListener('click', () => sendApiRequest('/orchestration/run/stop'));
        elements.resetAllBtn.addEventListener('click', () => sendApiRequest('/system/reset-all'));
        elements.acknowledgeAlarmBtn.addEventListener('click', () => sendApiRequest('/orchestration/run/acknowledge-alarm'));
        
        document.querySelectorAll('.manual-control-toggle input[type="checkbox"]').forEach(toggle => {
            toggle.addEventListener('change', (e) => {
                const name = e.target.id.replace('control-', '').replace('-toggle', '');
                sendApiRequest(`/outputs/toggle/${name}`);
            });
        });
        
        elements.cameraSwitcher?.addEventListener('click', (e) => {
            if (e.target.classList.contains('camera-select-btn')) {
                selectedCameraId = e.target.dataset.cameraId;
                updateCameraFeedSource();
                document.querySelectorAll('.camera-select-btn').forEach(btn => btn.classList.remove('active'));
                e.target.classList.add('active');
            }
        });
    }

    async function loadOperators() {
        const response = await fetch('/api/v1/operators/');
        const operators = await response.json();
        elements.operatorSelect.innerHTML = '<option value="">-- Select Operator --</option>';
        operators.forEach(op => {
            if (op.status === 'Active') elements.operatorSelect.innerHTML += `<option value="${op.id}">${op.name}</option>`;
        });
    }

    function updateCameraFeedSource() {
        elements.liveCameraFeed.src = `/api/v1/camera/stream/${selectedCameraId}?t=${new Date().getTime()}`;
        elements.liveFeedTitle.textContent = `LIVE CAMERA (${selectedCameraId.toUpperCase()})`;
    }

    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    connect();
    setupEventListeners();
    updateCameraFeedSource();
    elements.cameraSwitcher?.querySelector('.camera-select-btn')?.classList.add('active');
});