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
        aiFeedCanvas: document.getElementById('ai-feed-canvas'), // <-- CHANGED
        aiFeedCtx: document.getElementById('ai-feed-canvas').getContext('2d'), // <-- NEW
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
    };

    let lastExitedCount = -1;
    let selectedCameraId = elements.cameraSwitcher?.querySelector('.camera-select-btn')?.dataset.cameraId || 'rpi';

    // --- WebSocket Handling ---
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
    
    // --- THIS IS THE NEW, ROBUST AI FEED HANDLER ---
    function updateAiFeed(data) {
        if (!data || !data.original_path) return;
        const { annotated_path, original_path, results } = data;
        
        const imageToLoad = (annotated_path && annotated_path !== original_path) ? annotated_path : original_path;
        
        const img = new Image();
        img.crossOrigin = "anonymous"; // Handle potential CORS if ever needed
        img.onload = () => {
            // Match canvas size to image aspect ratio
            const canvas = elements.aiFeedCanvas;
            const ctx = elements.aiFeedCtx;
            const aspectRatio = img.naturalWidth / img.naturalHeight;
            canvas.width = canvas.clientWidth;
            canvas.height = canvas.clientWidth / aspectRatio;

            ctx.clearRect(0, 0, canvas.width, canvas.height);
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

            if (results) {
                drawAnnotations(results, canvas.width / img.naturalWidth);
                updateAiDetails(results);
            } else {
                // Draw "No Annotation" text directly on canvas
                ctx.fillStyle = 'rgba(0, 0, 0, 0.6)';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                ctx.fillStyle = 'white';
                ctx.font = 'bold 24px sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('No Annotation Available', canvas.width / 2, canvas.height / 2);
                elements.aiDetailsSection.style.display = 'none';
            }
        };
        img.src = `${imageToLoad}?t=${new Date().getTime()}`; // Cache buster
    }

    // --- NEW: Annotation drawing logic ported from qc_testing.js ---
    function drawAnnotations(results, scale) {
        const idResults = results.identification_results;
        if (!idResults) return;
        const ctx = elements.aiFeedCtx;

        const drawBoundingBox = (boxData, label, color, thickness, labelInside = false) => {
            if (!boxData) return;
            const x = boxData.x * scale;
            const y = boxData.y * scale;
            const w = boxData.width * scale;
            const h = boxData.height * scale;
            
            ctx.strokeStyle = color;
            ctx.lineWidth = thickness;
            ctx.strokeRect(x, y, w, h);

            const fontScale = 1.0;
            const font = `bold ${16 * fontScale}px sans-serif`;
            ctx.font = font;
            const textMetrics = ctx.measureText(label);
            const textWidth = textMetrics.width;
            const textHeight = 16 * fontScale;

            if (labelInside) {
                const textY = y + textHeight + 5;
                ctx.fillStyle = color;
                ctx.fillRect(x, y, textWidth + 10, textHeight + 10);
                ctx.fillStyle = 'white';
                ctx.fillText(label, x + 5, textY);
            } else {
                const textY = y - 5;
                const bgY = y - textHeight - 10;
                ctx.fillStyle = color;
                ctx.fillRect(x, bgY, textWidth + 10, textHeight + 10);
                ctx.fillStyle = 'white';
                ctx.fillText(label, x + 5, textY);
            }
        };

        const qcCheck = idResults.qc;
        if (qcCheck && qcCheck.overall_status) {
            drawBoundingBox(qcCheck.bounding_box, `Status: ${qcCheck.overall_status}`, qcCheck.overall_status === 'ACCEPT' ? 'lime' : 'red', 5, true);
        }
        const categoryCheck = idResults.category;
        if (categoryCheck && categoryCheck.detected_product_type) {
            drawBoundingBox(categoryCheck.bounding_box, `Type: ${categoryCheck.detected_product_type}`, 'blue', 3, false);
        }
        const defects = (idResults.defects && idResults.defects.defects) ? idResults.defects.defects : [];
        defects.forEach(defect => {
            drawBoundingBox(defect.bounding_box, `Defect: ${defect.defect_type}`, 'yellow', 2, false);
        });
    }

    // --- NEW: Update text summary section ---
    function updateAiDetails(results) {
        if (!results) {
            elements.aiDetailsSection.style.display = 'none';
            return;
        }
        const idResults = results.identification_results || {};
        const qc = idResults.qc;
        elements.aiDetailsQc.textContent = qc ? qc.overall_status : 'N/A';
        elements.aiDetailsQc.className = qc ? `detail-value status-${qc.overall_status.toLowerCase()}` : 'detail-value';
        const category = idResults.category;
        elements.aiDetailsCategory.textContent = category ? `${category.detected_product_type} (${(category.confidence * 100).toFixed(1)}%)` : 'N/A';
        const size = idResults.size;
        elements.aiDetailsSize.textContent = (size && size.detected_product_size) ? size.detected_product_size : 'N/A';
        const defects = idResults.defects && idResults.defects.defects ? idResults.defects.defects : [];
        elements.aiDetailsDefects.textContent = defects.length > 0 ? `${defects.length} Found` : 'None Detected';
        elements.aiDetailsSection.style.display = 'block';
    }

    // --- All other existing functions remain unchanged ---
    function updateDashboard(data) {
        const { system, orchestration } = data;
        elements.countExited.textContent = orchestration.run_progress;
        elements.countOnBelt.textContent = system.in_flight_count;
        elements.conveyorMode.textContent = orchestration.mode;
        const isRunning = orchestration.mode === 'Running';
        elements.conveyorBelt.classList.toggle('running', isRunning);
        if (orchestration.run_progress > lastExitedCount && isRunning) triggerBoxAnimation();
        lastExitedCount = orchestration.run_progress;
        updateProgressCircle(orchestration.run_progress, orchestration.target_count);
        elements.activeProfileDisplay.textContent = orchestration.active_profile || 'None';
        elements.runDetailBatch.textContent = orchestration.batch_code || 'N/A';
        elements.runDetailOperator.textContent = orchestration.operator_name || 'N/A';
        updateAlarm(orchestration.active_alarm_message);
        updateSystemToggles(system);
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

    function updateSystemToggles(system) {
        document.querySelectorAll('.control-toggle').forEach(toggle => {
            const key = toggle.id.replace('control-', '').replace('-toggle', '');
            if (system && typeof system[`${key}_relay_status`] !== 'undefined') {
                toggle.checked = system[`${key}_relay_status`];
            }
        });
    }

    async function sendApiRequest(endpoint, method = 'POST', body = null) {
        try {
            const options = { method, headers: { 'Content-Type': 'application/json' } };
            if (body) options.body = JSON.stringify(body);
            const response = await fetch(`/api/v1${endpoint}`, options);
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'API request failed');
            }
            return await response.json();
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    }

    function setupEventListeners() {
        elements.startRunBtn.addEventListener('click', () => {
            if (!elements.objectProfileSelect.value) {
                alert('Please select an Object Profile (Recipe) before starting.');
                return;
            }
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
        document.querySelectorAll('.control-toggle').forEach(toggle => {
            toggle.addEventListener('change', (e) => sendApiRequest(`/outputs/toggle/${e.target.id.replace('control-','').replace('-toggle','')}`));
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

    connect();
    setupEventListeners();
    updateCameraFeedSource();
    elements.cameraSwitcher?.querySelector('.camera-select-btn')?.classList.add('active');
});