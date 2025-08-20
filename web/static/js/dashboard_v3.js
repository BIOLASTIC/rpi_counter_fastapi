// rpi_counter_fastapi-apintrigation/web/static/js/dashboard_v3.js

document.addEventListener('DOMContentLoaded', function () {
    // WebSocket
    let socket;
    let currentCameraId = null;

    // Element Cache
    const elements = {
        countOnBelt: document.getElementById('count-on-belt'),
        countExited: document.getElementById('count-exited'),
        conveyorMode: document.getElementById('conveyor-mode'),
        conveyorBelt: document.getElementById('conveyor-belt'),
        animationZone: document.getElementById('animation-zone'),
        startRunBtn: document.getElementById('start-run-btn'),
        stopRunBtn: document.getElementById('stop-run-btn'),
        resetAllBtn: document.getElementById('reset-all-btn'),
        profileSelect: document.getElementById('object-profile-select'),
        targetCountInput: document.getElementById('target-count-input'),
        postBatchDelayInput: document.getElementById('post-batch-delay-input'),
        preRunModal: new bootstrap.Modal(document.getElementById('pre-run-modal')),
        operatorSelect: document.getElementById('operator-select'),
        batchCodeInput: document.getElementById('batch-code-input'),
        reviewRunBtn: document.getElementById('review-run-btn'),
        goBackBtn: document.getElementById('go-back-btn'),
        startFinalRunBtn: document.getElementById('start-final-run-btn'),
        preRunInputView: document.getElementById('pre-run-input-view'),
        preRunConfirmView: document.getElementById('pre-run-confirm-view'),
        confirmOperator: document.getElementById('confirm-operator'),
        confirmBatchCode: document.getElementById('confirm-batch-code'),
        confirmRecipe: document.getElementById('confirm-recipe'),
        confirmTarget: document.getElementById('confirm-target'),
        progressPath: document.getElementById('progress-path'),
        progressPercentage: document.getElementById('progress-percentage'),
        progressDetails: document.getElementById('progress-details'),
        activeProfileDisplay: document.getElementById('active-profile-display'),
        runDetailBatch: document.getElementById('run-detail-batch'),
        runDetailOperator: document.getElementById('run-detail-operator'),
        runAlarmBlock: document.getElementById('run-alarm-block'),
        runAlarmMessage: document.getElementById('run-alarm-message'),
        acknowledgeAlarmBtn: document.getElementById('acknowledge-alarm-btn'),
        liveCameraFeed: document.getElementById('live-camera-feed'),
        aiFeedCanvas: document.getElementById('ai-feed-canvas'),
        aiDetailsSection: document.getElementById('ai-details-section'),
        aiDetailsQcStatus: document.getElementById('ai-details-qc-status'),
        aiDetailsQcConfidence: document.getElementById('ai-details-qc-confidence'),
        aiDetailsCategoryName: document.getElementById('ai-details-category-name'),
        aiDetailsCategoryConfidence: document.getElementById('ai-details-category-confidence'),
        aiValidationList: document.getElementById('ai-validation-list'),
        cameraSwitcher: document.getElementById('camera-switcher'),
        liveFeedTitle: document.getElementById('live-feed-title'),
        manualControlToggles: document.querySelectorAll('.manual-control-toggle input'),
    };

    const aiFeedCtx = elements.aiFeedCanvas.getContext('2d');
    let aiFeedImage = new Image();

    // Helper to safely access nested properties
    const get = (path, obj) => path.reduce((xs, x) => (xs && xs[x] != null) ? xs[x] : null, obj);

    // Maps the control name from the data-attribute to the key in the system status JSON
    const controlNameToStatusKey = {
        'conveyor': 'conveyor_relay_status',
        'gate': 'gate_relay_status',
        'diverter': 'diverter_relay_status',
        'camera_light': 'camera_light_status',
        'buzzer': 'buzzer_status'
    };

    function initWebSocket() {
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
        socket = new WebSocket(wsUrl);
        socket.onopen = () => console.log("[WebSocket] Connection established.");
        socket.onclose = () => console.error('[WebSocket] Connection died.');
        socket.onerror = (error) => console.error(`[WebSocket] Error: ${error.message}`);
        socket.onmessage = handleWebSocketMessage;
    }

    function handleWebSocketMessage(event) {
        const data = JSON.parse(event.data);
        if (data.type === 'full_status') {
            updateDashboard(data.data);
        } else if (data.type === 'qc_update') {
            const qcData = data.data;
            aiFeedImage.src = qcData.annotated_path + '?t=' + new Date().getTime();
            
            const results = qcData.results;
            if (results) {
                const qcSummary = results.qc_summary || {};
                const qcStatus = qcSummary.overall_status || '--';
                elements.aiDetailsQcStatus.textContent = qcStatus;
                elements.aiDetailsQcStatus.className = `detail-value status-${qcStatus}`;
                elements.aiDetailsQcConfidence.textContent = qcSummary.confidence ? `${(qcSummary.confidence * 100).toFixed(1)}%` : '--';

                const catSummary = results.category_summary || {};
                elements.aiDetailsCategoryName.textContent = catSummary.detected_type || '--';
                elements.aiDetailsCategoryConfidence.textContent = catSummary.confidence ? `${(catSummary.confidence * 100).toFixed(1)}%` : '--';

                const validation = results.validation_results || {};
                elements.aiValidationList.innerHTML = '';
                if (validation.checks && validation.checks.length > 0) {
                    validation.checks.forEach(check => {
                        const isPass = check.status === 'PASS';
                        const icon = isPass ? '<i class="bi bi-check-circle-fill text-success"></i>' : '<i class="bi bi-x-circle-fill text-danger"></i>';
                        const listItem = `<li class="list-group-item d-flex justify-content-between align-items-center small"><div>${icon} ${check.check_type}</div><span class="badge ${isPass ? 'bg-success' : 'bg-danger'}">${check.value}</span></li>`;
                        elements.aiValidationList.insertAdjacentHTML('beforeend', listItem);
                    });
                } else {
                    elements.aiValidationList.innerHTML = '<li class="list-group-item small text-muted">No geometric checks configured.</li>';
                }
                elements.aiDetailsSection.style.display = 'block';
            }
        }
    }

    function updateDashboard(data) {
        const { system, orchestration } = data;
        
        elements.countOnBelt.textContent = system.in_flight_count;
        elements.countExited.textContent = orchestration.run_progress;
        elements.conveyorMode.textContent = orchestration.mode;
        elements.conveyorBelt.classList.toggle('running', orchestration.mode === 'Running');

        updateProgressCircle(orchestration.run_progress, orchestration.target_count);
        
        elements.activeProfileDisplay.textContent = orchestration.active_profile || 'None';
        elements.runDetailBatch.textContent = orchestration.batch_code || 'N/A';
        elements.runDetailOperator.textContent = orchestration.operator_name || 'N/A';

        if (orchestration.active_alarm_message) {
            elements.runAlarmMessage.textContent = orchestration.active_alarm_message;
            elements.runAlarmBlock.style.display = 'flex';
        } else {
            elements.runAlarmBlock.style.display = 'none';
        }

        // --- THIS IS THE FIX: Update manual control toggles from WebSocket data ---
        elements.manualControlToggles.forEach(toggle => {
            const controlName = toggle.dataset.controlName;
            const statusKey = controlNameToStatusKey[controlName];
            if (statusKey && system.hasOwnProperty(statusKey)) {
                const isChecked = system[statusKey];
                // Only update the DOM if the state is different to avoid flicker and fighting user input
                if (toggle.checked !== isChecked) {
                    toggle.checked = isChecked;
                }
            }
        });
        // --- END OF FIX ---
    }

    function updateProgressCircle(current, target) {
        const percentage = (target > 0) ? Math.min(100, (current / target) * 100) : 0;
        elements.progressPercentage.textContent = `${Math.floor(percentage)}%`;
        elements.progressDetails.textContent = `${current} / ${target > 0 ? target : '∞'}`;
        const circumference = 2 * Math.PI * 45;
        const offset = circumference - (percentage / 100) * circumference;
        elements.progressPath.style.strokeDasharray = `${circumference} ${circumference}`;
        elements.progressPath.style.strokeDashoffset = offset;
    }
    
    async function populateOperatorSelect() {
        try {
            const response = await fetch('/api/v1/operators/');
            const operators = await response.json();
            elements.operatorSelect.innerHTML = '<option value="">-- Select Operator --</option>';
            operators.filter(o => o.status === 'Active').forEach(op => {
                elements.operatorSelect.insertAdjacentHTML('beforeend', `<option value="${op.id}">${op.name}</option>`);
            });
        } catch (error) {
            console.error("Failed to load operators:", error);
        }
    }

    async function sendPostRequest(url, body) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: body ? JSON.stringify(body) : null
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP Error ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            alert(`Error: ${error.message}`);
            console.error(error);
        }
    }
    
    // --- ALL EVENT LISTENERS ---
    elements.startRunBtn.addEventListener('click', () => {
        if (!elements.profileSelect.value) {
            alert('Please select an Object Profile (Recipe) first.');
            return;
        }
        elements.preRunInputView.style.display = 'block';
        elements.preRunConfirmView.style.display = 'none';
        populateOperatorSelect();
        elements.preRunModal.show();
    });

    elements.reviewRunBtn.addEventListener('click', () => {
        if (!elements.operatorSelect.value || !elements.batchCodeInput.value) {
            alert('Please select an operator and enter a batch code.');
            return;
        }
        elements.confirmOperator.textContent = elements.operatorSelect.options[elements.operatorSelect.selectedIndex].text;
        elements.confirmBatchCode.textContent = elements.batchCodeInput.value;
        elements.confirmRecipe.textContent = elements.profileSelect.options[elements.profileSelect.selectedIndex].text;
        const target = elements.targetCountInput.value;
        elements.confirmTarget.textContent = target === '0' ? 'Continuous' : target;
        elements.preRunInputView.style.display = 'none';
        elements.preRunConfirmView.style.display = 'block';
    });

    elements.goBackBtn.addEventListener('click', () => {
        elements.preRunInputView.style.display = 'block';
        elements.preRunConfirmView.style.display = 'none';
    });
    
    elements.startFinalRunBtn.addEventListener('click', async () => {
        const payload = {
            object_profile_id: parseInt(elements.profileSelect.value, 10),
            target_count: parseInt(elements.targetCountInput.value, 10),
            post_batch_delay_sec: parseInt(elements.postBatchDelayInput.value, 10),
            batch_code: elements.batchCodeInput.value,
            operator_id: parseInt(elements.operatorSelect.value, 10),
        };
        await sendPostRequest('/api/v1/orchestration/run/start', payload);
        elements.preRunModal.hide();
    });

    elements.stopRunBtn.addEventListener('click', () => sendPostRequest('/api/v1/orchestration/run/stop'));
    elements.resetAllBtn.addEventListener('click', () => sendPostRequest('/api/v1/system/reset-all'));
    elements.acknowledgeAlarmBtn.addEventListener('click', () => sendPostRequest('/api/v1/orchestration/run/acknowledge-alarm'));

    // --- THIS IS THE CORRECTED EVENT LISTENER for toggles ---
    elements.manualControlToggles.forEach(toggle => {
        toggle.addEventListener('change', function() {
            const name = this.dataset.controlName; // Use the robust data-attribute
            if(name) {
                sendPostRequest(`/api/v1/outputs/toggle/${name}`);
            }
        });
    });

    elements.cameraSwitcher.addEventListener('click', e => {
        if (e.target.classList.contains('camera-select-btn')) {
            const newCamId = e.target.dataset.cameraId;
            if (newCamId !== currentCameraId) {
                switchCamera(newCamId);
            }
        }
    });
    
    function switchCamera(camId) {
        currentCameraId = camId;
        elements.liveCameraFeed.src = `/api/v1/camera/stream/${camId}`;
        elements.liveFeedTitle.textContent = `LIVE - ${camId.toUpperCase()}`;
        document.querySelectorAll('.camera-select-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.cameraId === camId);
        });
    }

    aiFeedImage.onload = () => {
        elements.aiFeedCanvas.width = aiFeedImage.naturalWidth;
        elements.aiFeedCanvas.height = aiFeedImage.naturalHeight;
        aiFeedCtx.drawImage(aiFeedImage, 0, 0);
    };

    // --- INITIAL SETUP ---
    const firstCameraBtn = document.querySelector('.camera-select-btn');
    if (firstCameraBtn) {
        switchCamera(firstCameraBtn.dataset.cameraId);
    }
    initWebSocket();
});