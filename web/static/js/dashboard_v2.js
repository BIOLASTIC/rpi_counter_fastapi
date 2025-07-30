document.addEventListener('DOMContentLoaded', function () {
    const elements = {
        animationZone: document.getElementById('animation-zone'),
        conveyorBelt: document.getElementById('conveyor-belt'),
        countEntered: document.getElementById('count-entered'),
        countOnBelt: document.getElementById('count-on-belt'),
        countExited: document.getElementById('count-exited'),
        systemMode: document.getElementById('system-mode'),
        progressCirclePath: document.querySelector('.progress-circle__path'),
        progressPercentage: document.getElementById('progress-percentage'),
        progressDetails: document.getElementById('progress-details'),
        startBatchBtn: document.getElementById('start-batch-btn'),
        stopBatchBtn: document.getElementById('stop-batch-btn'),
        saveConfigBtn: document.getElementById('save-config-btn'),
        batchSizeInput: document.getElementById('batch-size-input'),
        delayInput: document.getElementById('delay-input'),
        resetAllBtn: document.getElementById('reset-all-btn'),
    };

    function setupDynamicStyles() {
        const animationTime = elements.animationZone?.dataset.animationTime || '5';
        document.documentElement.style.setProperty('--box-transit-time', `${animationTime}s`);
    }

    const progressCircleRadius = elements.progressCirclePath?.r.baseVal.value || 0;
    const progressCircleCircumference = 2 * Math.PI * progressCircleRadius;
    if (elements.progressCirclePath) {
        elements.progressCirclePath.style.strokeDasharray = `${progressCircleCircumference} ${progressCircleCircumference}`;
    }

    let activeBoxesOnBelt = 0;

    function connectWebSocket() {
        const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const ws = new WebSocket(`${wsProtocol}//${window.location.host}/ws`);
        ws.onopen = () => console.log('WebSocket connection established.');
        ws.onclose = () => { console.log('WebSocket connection closed. Retrying in 3 seconds...'); setTimeout(connectWebSocket, 3000); };
        ws.onerror = (error) => console.error('WebSocket Error:', error);
        ws.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                switch (message.type) {
                    case 'detection_status': updateDetectionStatus(message.data); break;
                    case 'system_status': updateSystemStatus(message.data); break;
                    case 'orchestration_status': updateOrchestrationStatus(message.data); break;
                }
            } catch (e) { console.error('Failed to parse WebSocket message:', e); }
        };
    }

    const updateBadge = (selector, text, state) => {
        const el = document.getElementById(selector);
        if (!el) return;
        el.textContent = text ? text.toUpperCase().replace("_", " ") : '--';
        el.className = 'status-badge';
        if (state) el.classList.add(state);
    };

    function updateDetectionStatus(data) {
        elements.countEntered.textContent = data.entered ?? 0;
        elements.countOnBelt.textContent = data.on_belt ?? 0;
        elements.countExited.textContent = data.exited ?? 0;
        updateBoxAnimation(data.on_belt ?? 0);
    }

    function updateSystemStatus(data) {
        updateBadge('status-sensor-1', data.sensor_1_status ? 'TRIGGERED' : 'CLEAR', data.sensor_1_status ? 'triggered' : 'clear');
        updateBadge('status-sensor-2', data.sensor_2_status ? 'TRIGGERED' : 'CLEAR', data.sensor_2_status ? 'triggered' : 'clear');
        updateBadge('status-conveyor-relay', data.conveyor_relay_status ? 'ON' : 'OFF', data.conveyor_relay_status ? 'on' : 'off');
        updateBadge('status-gate-relay', data.gate_relay_status ? 'ON' : 'OFF', data.gate_relay_status ? 'on' : 'off');
        updateBadge('status-gpio', data.gpio_status, data.gpio_status);
        updateBadge('status-io-module', data.io_module_status, data.io_module_status);
        if (data.camera_statuses) {
            for (const camId in data.camera_statuses) {
                const status = data.camera_statuses[camId];
                updateBadge(`status-camera-${camId}`, status, status);
                const feedImgEl = document.getElementById(`live-camera-feed-${camId}`);
                const feedOverlayEl = document.getElementById(`camera-offline-overlay-${camId}`);
                if (feedImgEl && feedOverlayEl) {
                    if (status === 'connected') {
                        feedOverlayEl.classList.add('hidden');
                        if (feedImgEl.src.includes('placeholder.jpg')) feedImgEl.src = `/api/v1/camera/stream/${camId}`;
                    } else {
                        feedOverlayEl.classList.remove('hidden');
                        feedImgEl.src = '/static/images/placeholder.jpg';
                    }
                }
            }
        }
    }

    function updateOrchestrationStatus(data) {
        const isRunning = data.mode === 'Running Batch';
        updateBadge('system-mode', data.mode, isRunning ? 'on' : 'off');
        if (document.activeElement !== elements.batchSizeInput) {
            elements.batchSizeInput.value = data.batch_target > 0 ? data.batch_target : 50;
        }
        if (document.activeElement !== elements.delayInput) {
            elements.delayInput.value = data.post_batch_delay ?? 5;
        }
        elements.conveyorBelt?.classList.toggle('running', isRunning);
        const progress = (data.batch_target > 0) ? (data.batch_progress ?? 0) / data.batch_target : 0;
        const offset = progressCircleCircumference * (1 - progress);
        if (elements.progressCirclePath) elements.progressCirclePath.style.strokeDashoffset = offset;
        elements.progressPercentage.textContent = `${Math.round(progress * 100)}%`;
        elements.progressDetails.textContent = `${data.batch_progress ?? 0} / ${data.batch_target > 0 ? data.batch_target : 50}`;
    }

    function updateBoxAnimation(boxCount) {
        if (!elements.conveyorBelt) return;
        const existingBoxes = elements.conveyorBelt.getElementsByClassName('box').length;
        if (boxCount === existingBoxes) return;
        while (boxCount > activeBoxesOnBelt) {
            const box = document.createElement('div');
            box.className = 'box';
            elements.conveyorBelt.appendChild(box);
            activeBoxesOnBelt++;
        }
        while (boxCount < activeBoxesOnBelt) {
            const boxToRemove = elements.conveyorBelt.querySelector('.box');
            if (boxToRemove) elements.conveyorBelt.removeChild(boxToRemove);
            activeBoxesOnBelt--;
        }
    }

    async function sendPostRequest(url, body) {
        try {
            const response = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
            if (!response.ok) { const errorData = await response.json(); alert(`Error: ${errorData.detail || 'Failed to perform action'}`); }
        } catch (error) { console.error('API Request Failed:', error); alert('Could not connect to the server.'); }
    }

    elements.startBatchBtn?.addEventListener('click', () => {
        const size = parseInt(elements.batchSizeInput.value, 10);
        if (size > 0) sendPostRequest('/api/v1/orchestration/batch/start', { size });
        else alert('Batch size must be a positive number.');
    });

    elements.stopBatchBtn?.addEventListener('click', () => {
        if (confirm('Are you sure you want to stop the entire process?')) { sendPostRequest('/api/v1/orchestration/batch/stop', {}); }
    });

    elements.saveConfigBtn?.addEventListener('click', () => {
        const batch_size = parseInt(elements.batchSizeInput.value, 10);
        const post_batch_delay = parseInt(elements.delayInput.value, 10);
        if (batch_size > 0 && post_batch_delay >= 0) {
            sendPostRequest('/api/v1/orchestration/batch/config', { batch_size, post_batch_delay });
            alert('Configuration saved!');
        } else { alert('Please enter valid, non-negative numbers for configuration.'); }
    });
    
    elements.resetAllBtn?.addEventListener('click', () => {
        if (confirm('DANGER: This will reset all counters to zero and stop any running process. Are you absolutely sure?')) {
            sendPostRequest('/api/v1/system/reset-all', {});
            alert('Full system reset command sent.');
        }
    });
    
    document.querySelectorAll('.fullscreen-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const camId = e.currentTarget.dataset.camId;
            const container = document.getElementById(`feed-container-${camId}`);
            if (container && !document.fullscreenElement) {
                container.requestFullscreen().catch(err => console.error(`Fullscreen error: ${err.message}`));
            } else if (document.fullscreenElement) {
                document.exitFullscreen();
            }
        });
    });

    setupDynamicStyles();
    connectWebSocket();
});