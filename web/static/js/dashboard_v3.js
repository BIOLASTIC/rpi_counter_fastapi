document.addEventListener('DOMContentLoaded', () => {
    const socket = new WebSocket(`ws://${window.location.host}/ws`);
    socket.onopen = () => console.log("WebSocket connected.");
    socket.onclose = () => console.log("WebSocket closed.");
    socket.onerror = (error) => console.error("WebSocket Error:", error);

    const elements = {
        progressPath: document.getElementById('progress-path'),
        progressPercentage: document.getElementById('progress-percentage'),
        progressDetails: document.getElementById('progress-details'),
        activeProfile: document.getElementById('active-profile-display'),
        runDetailBatch: document.getElementById('run-detail-batch'),
        runDetailOperator: document.getElementById('run-detail-operator'),
        countOnBelt: document.getElementById('count-on-belt'),
        countProcessed: document.getElementById('count-processed'),
        conveyorMode: document.getElementById('conveyor-mode'),
        conveyorBelt: document.getElementById('conveyor-belt'),
        liveCameraFeed: document.getElementById('live-camera-feed'),
        aiAnnotatedFeed: document.getElementById('ai-annotated-feed'),
        cameraSelectBtns: document.querySelectorAll('.camera-select-btn'),
        aiDetailsQcStatus: document.getElementById('ai-details-qc-status'),
        aiDetailsReason: document.getElementById('ai-details-reason'),
        aiDetailsCategory: document.getElementById('ai-details-category-name'),
        statusSensor1: document.getElementById('status-sensor-1'),
        statusSensor2: document.getElementById('status-sensor-2'),
        statusIoModule: document.getElementById('status-io-module'),
        manualControlToggles: document.querySelectorAll('.manual-control-toggle input[type="checkbox"]'),
        alarmBlock: document.getElementById('run-alarm-block'),
        alarmMessage: document.getElementById('run-alarm-message'),
        ackAlarmBtn: document.getElementById('acknowledge-alarm-btn'),
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
        confirmOperator: document.getElementById('confirm-operator'),
        confirmBatchCode: document.getElementById('confirm-batch-code'),
        confirmRecipe: document.getElementById('confirm-recipe'),
        confirmTarget: document.getElementById('confirm-target'),
        preRunInputView: document.getElementById('pre-run-input-view'),
        preRunConfirmView: document.getElementById('pre-run-confirm-view'),
    };

    const CIRCLE_CIRCUMFERENCE = 2 * Math.PI * 45;
    elements.progressPath.style.strokeDasharray = CIRCLE_CIRCUMFERENCE;
    let activeCameraId = elements.cameraSelectBtns[0]?.dataset.cameraId || 'rpi';

    socket.onmessage = (event) => {
        const msg = JSON.parse(event.data);
        switch (msg.type) {
            case 'full_status':
                updateFullStatus(msg.data);
                break;
            case 'qc_update':
                updateQcPanel(msg.data);
                break;
            case 'new_item_detected':
                // Use the count from the full_status for consistency, but trigger animation here
                animateProduct(msg.data.serial_number);
                break;
        }
    };

    function updateFullStatus(data) {
        if (!data) return;
        if (data.system) {
            const sys = data.system;
            updateBadge(elements.statusSensor1, sys.sensor_1_status, 'TRIGGERED', 'CLEAR');
            updateBadge(elements.statusSensor2, sys.sensor_2_status, 'TRIGGERED', 'CLEAR');
            updateBadge(elements.statusIoModule, sys.io_module_status === 'ok', 'OK', 'ERROR');
            elements.countOnBelt.textContent = sys.in_flight_count || 0;
            elements.manualControlToggles.forEach(toggle => {
                const name = toggle.dataset.controlName;
                toggle.checked = sys[`${name}_relay_status`] || sys[`${name}_status`] || false;
            });
        }
        if (data.orchestration) {
            const orc = data.orchestration;
            elements.conveyorMode.textContent = orc.mode || 'N/A';
            elements.activeProfile.textContent = orc.active_profile || 'None';
            elements.runDetailBatch.textContent = orc.batch_code || 'N/A';
            elements.runDetailOperator.textContent = orc.operator_name || 'N/A';
            elements.countProcessed.textContent = orc.run_progress || 0;
            const target = orc.target_count || 0;
            const progress = (target > 0) ? (orc.run_progress / target) * 100 : 0;
            elements.progressPercentage.textContent = `${Math.round(progress)}%`;
            elements.progressDetails.textContent = `${orc.run_progress} / ${target > 0 ? target : '∞'}`;
            const offset = CIRCLE_CIRCUMFERENCE * (1 - (progress / 100));
            elements.progressPath.style.strokeDashoffset = Math.max(0, offset);
            elements.alarmBlock.style.display = orc.active_alarm_message ? 'grid' : 'none';
            elements.alarmMessage.textContent = orc.active_alarm_message || '';
        }
    }

    function updateQcPanel(data) {
        elements.aiAnnotatedFeed.src = data.annotated_path ? `${data.annotated_path}?t=${new Date().getTime()}` : '/static/images/placeholder.jpg';
        const summary = data.results || {};
        const status = summary.overall_status || 'PENDING';
        elements.aiDetailsQcStatus.textContent = status;
        updateBadge(elements.aiDetailsQcStatus, status === 'ACCEPT', 'ACCEPT', 'REJECT');
        elements.aiDetailsReason.textContent = summary.reject_reason || '--';
        elements.aiDetailsCategory.textContent = summary.primary_detection?.type || '--';
    }
    
    function updateBadge(element, isSuccess, successText = 'ON', failText = 'OFF') {
        element.textContent = isSuccess ? successText : failText;
        element.classList.toggle('bg-success', isSuccess);
        element.classList.toggle('bg-danger', !isSuccess);
        element.classList.toggle('text-dark', isSuccess);
    }
    
    function animateProduct(serialNumber) {
        const productDiv = document.createElement('div');
        productDiv.className = 'conveyor-product';
        productDiv.id = `product-${serialNumber}`;
        productDiv.innerHTML = '<i class="bi bi-box-seam"></i>';
        elements.conveyorBelt.appendChild(productDiv);
        setTimeout(() => productDiv.style.right = '100%', 10);
        productDiv.addEventListener('transitionend', () => productDiv.remove());
    }

    async function apiPost(endpoint, body = {}) {
        try {
            const response = await fetch(endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            if (!response.ok) {
                let errorDetail = 'API request failed';
                try { errorDetail = (await response.json()).detail; } 
                catch (e) { errorDetail = await response.text(); }
                throw new Error(errorDetail);
            }
            return response.json();
        } catch (error) {
            console.error(`Error with ${endpoint}:`, error);
            showToast('API Error', error.message, 'bg-danger');
        }
    }

    async function loadOperators() {
        try {
            const operators = await (await fetch('/api/v1/operators/')).json();
            elements.operatorSelect.innerHTML = '<option value="">-- Select Operator --</option>';
            operators.forEach(op => {
                const option = new Option(op.name, op.id);
                elements.operatorSelect.appendChild(option);
            });
        } catch (error) { console.error('Failed to load operators:', error); }
    }

    function switchLiveCamera(camId) {
        activeCameraId = camId;
        elements.liveCameraFeed.src = `/api/v1/camera/stream/${camId}`;
        elements.cameraSelectBtns.forEach(btn => btn.classList.toggle('active', btn.dataset.cameraId === camId));
    }

    elements.startRunBtn.addEventListener('click', () => {
        if (!elements.profileSelect.value) { showToast('Error', 'Please select a recipe first.', 'bg-danger'); return; }
        elements.preRunInputView.style.display = 'block';
        elements.preRunConfirmView.style.display = 'none';
        elements.preRunModal.show();
    });

    elements.reviewRunBtn.addEventListener('click', () => {
        if (!elements.operatorSelect.value || !elements.batchCodeInput.value) { showToast('Error', 'Operator and Batch Code are required.', 'bg-danger'); return; }
        elements.confirmOperator.textContent = elements.operatorSelect.options[elements.operatorSelect.selectedIndex].text;
        elements.confirmBatchCode.textContent = elements.batchCodeInput.value;
        elements.confirmRecipe.textContent = elements.profileSelect.options[elements.profileSelect.selectedIndex].text;
        elements.confirmTarget.textContent = elements.targetCountInput.value > 0 ? elements.targetCountInput.value : 'Unlimited';
        elements.preRunInputView.style.display = 'none';
        elements.preRunConfirmView.style.display = 'block';
    });

    elements.goBackBtn.addEventListener('click', () => {
        elements.preRunInputView.style.display = 'block';
        elements.preRunConfirmView.style.display = 'none';
    });

    elements.startFinalRunBtn.addEventListener('click', async () => {
        const payload = {
            object_profile_id: parseInt(elements.profileSelect.value),
            target_count: parseInt(elements.targetCountInput.value),
            post_batch_delay_sec: parseInt(elements.postBatchDelayInput.value),
            batch_code: elements.batchCodeInput.value,
            operator_id: parseInt(elements.operatorSelect.value)
        };
        await apiPost('/api/v1/orchestration/run/start', payload);
        elements.preRunModal.hide();
    });

    elements.stopRunBtn.addEventListener('click', () => apiPost('/api/v1/orchestration/run/stop'));
    elements.resetAllBtn.addEventListener('click', () => apiPost('/api/v1/system/reset-all'));
    elements.ackAlarmBtn.addEventListener('click', () => apiPost('/api/v1/orchestration/run/acknowledge-alarm'));
    elements.manualControlToggles.forEach(toggle => toggle.addEventListener('change', () => apiPost(`/api/v1/outputs/toggle/${toggle.dataset.controlName}`)));
    elements.cameraSelectBtns.forEach(btn => btn.addEventListener('click', () => switchLiveCamera(btn.dataset.cameraId)));

    loadOperators();
    if (activeCameraId) switchLiveCamera(activeCameraId);
});