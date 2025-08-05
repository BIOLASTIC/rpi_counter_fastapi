// /static/js/dashboard_v3.js

document.addEventListener('DOMContentLoaded', function () {
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProtocol}//${window.location.host}/ws`;
    let socket;

    // --- THIS IS THE DEFINITIVE FIX ---
    // The selector for the camera light toggle has been corrected to include the underscore.
    const elements = {
        animationZone: document.getElementById('animation-zone'),
        conveyorBelt: document.getElementById('conveyor-belt'),
        countOnBelt: document.getElementById('count-on-belt'),
        countExited: document.getElementById('count-exited'),
        conveyorMode: document.getElementById('conveyor-mode'),
        progressPath: document.getElementById('progress-path'),
        progressPercentage: document.getElementById('progress-percentage'),
        progressDetails: document.getElementById('progress-details'),
        activeProfileDisplay: document.getElementById('active-profile-display'),
        liveCameraFeed: document.getElementById('live-camera-feed'),
        liveFeedTitle: document.getElementById('live-feed-title'),
        startRunBtn: document.getElementById('start-run-btn'),
        stopRunBtn: document.getElementById('stop-run-btn'),
        resetAllBtn: document.getElementById('reset-all-btn'),
        profileSelect: document.getElementById('object-profile-select'),
        targetCountInput: document.getElementById('target-count-input'),
        postBatchDelayInput: document.getElementById('post-batch-delay-input'),
        statusSensor1: document.getElementById('status-sensor-1'),
        statusSensor2: document.getElementById('status-sensor-2'),
        statusIoModule: document.getElementById('status-io-module'),
        controlConveyorToggle: document.getElementById('control-conveyor-toggle'),
        controlGateToggle: document.getElementById('control-gate-toggle'),
        controlDiverterToggle: document.getElementById('control-diverter-toggle'),
        controlCamlightToggle: document.getElementById('control-camera_light-toggle'), // <-- CORRECTED ID
    };
    // --- END OF FIX ---
    
    const progressCircleRadius = elements.progressPath.r.baseVal.value;
    const progressCircumference = 2 * Math.PI * progressCircleRadius;
    elements.progressPath.style.strokeDasharray = `${progressCircumference} ${progressCircumference}`;
    elements.progressPath.style.strokeDashoffset = progressCircumference;

    function connect() {
        socket = new WebSocket(wsUrl);

        socket.onopen = () => console.log('WebSocket connection established.');
        socket.onclose = () => {
            console.log('WebSocket connection closed. Reconnecting in 3 seconds...');
            setTimeout(connect, 3000);
        };
        socket.onerror = (error) => console.error('WebSocket error:', error);
        
        socket.onmessage = (event) => {
            try {
                const message = JSON.parse(event.data);
                if (message.type === 'full_status' && message.data) {
                    if (message.data.system) {
                        updateSystemStatus(message.data.system);
                    }
                    if (message.data.orchestration) {
                        updateOrchestrationStatus(message.data.orchestration);
                    }
                }
            } catch (e) {
                console.error('Error parsing WebSocket message:', e);
                console.warn('Received message data:', event.data);
            }
        };
    }

    function updateSystemStatus(data) {
        updateStatusBadge(elements.statusSensor1, data.sensor_1_status, 'triggered', 'clear');
        updateStatusBadge(elements.statusSensor2, data.sensor_2_status, 'triggered', 'clear');
        updateStatusBadge(elements.statusIoModule, data.io_module_status === 'ok', 'ok', 'error', data.io_module_status);
        
        elements.controlConveyorToggle.checked = data.conveyor_relay_status;
        elements.controlGateToggle.checked = data.gate_relay_status;
        elements.controlDiverterToggle.checked = data.diverter_relay_status;
        elements.controlCamlightToggle.checked = data.camera_light_status;

        elements.countOnBelt.textContent = data.in_flight_count;

        if (data.camera_statuses && Object.keys(data.camera_statuses).length > 0) {
            const firstCamId = Object.keys(data.camera_statuses)[0];
            elements.liveFeedTitle.textContent = `${firstCamId.toUpperCase()} CAMERA`;
            elements.liveCameraFeed.src = `/api/v1/camera/stream/${firstCamId}?t=${new Date().getTime()}`;
        }
    }

    function updateOrchestrationStatus(data) {
        const isRunning = data.mode === "Running";
        const target = data.target_count;
        const progress = data.run_progress;
        
        elements.countExited.textContent = progress;

        let percentage = 0;
        if (target > 0) {
            percentage = Math.min((progress / target) * 100, 100);
            elements.progressDetails.textContent = `${progress} / ${target}`;
        } else {
            elements.progressDetails.textContent = `${progress} / ∞`;
        }
        const offset = progressCircumference - (percentage / 100) * progressCircumference;
        elements.progressPath.style.strokeDashoffset = offset;
        elements.progressPercentage.textContent = `${Math.round(percentage)}%`;

        elements.activeProfileDisplay.textContent = data.active_profile || 'None';
        elements.activeProfileDisplay.style.backgroundColor = data.active_profile !== 'None' ? 'var(--accent-blue)' : 'var(--text-secondary)';
        
        if (isRunning) {
            elements.conveyorBelt.classList.add('running');
            elements.conveyorMode.textContent = "RUNNING";
        } else {
            elements.conveyorBelt.classList.remove('running');
            elements.conveyorMode.textContent = data.mode.toUpperCase();
        }
    }
    
    function updateStatusBadge(element, is_ok, ok_text, fail_text, value = null) {
        if (!element) return;
        const text = value ? value : (is_ok ? ok_text : fail_text);
        const ok_class = ok_text.toLowerCase();
        const fail_class = fail_text.toLowerCase();
        
        element.textContent = text;
        element.classList.toggle(ok_class, is_ok);
        element.classList.toggle(fail_class, !is_ok);
        element.classList.remove(is_ok ? fail_class : ok_class);
    }
    
    async function apiPost(endpoint, body = null) {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
        };

        if (body) {
            requestOptions.body = JSON.stringify(body);
        }

        try {
            const response = await fetch(`/api/v1${endpoint}`, requestOptions);
            const data = await response.json(); 

            if (!response.ok) {
                alert(`Error: ${data.detail || response.statusText}`);
                throw new Error(data.detail || `Request failed with status ${response.status}`);
            }
            
            return data;
        } catch (error) {
            console.error(`API POST Error to ${endpoint}:`, error);
            if (!error.message.startsWith('Request failed')) {
                 alert(`Network Error: ${error.message}`);
            }
        }
    }

    elements.startRunBtn.addEventListener('click', () => {
        const profileId = elements.profileSelect.value;
        if (!profileId) {
            alert('Please select an object profile first.');
            return;
        }
        const payload = {
            object_profile_id: parseInt(profileId, 10),
            target_count: parseInt(elements.targetCountInput.value, 10),
            post_batch_delay_sec: parseInt(elements.postBatchDelayInput.value, 10),
        };
        apiPost('/orchestration/run/start', payload);
    });

    elements.stopRunBtn.addEventListener('click', () => apiPost('/orchestration/run/stop'));
    elements.resetAllBtn.addEventListener('click', () => apiPost('/system/reset-all'));

    document.querySelectorAll('.manual-control-toggle input[type="checkbox"]').forEach(toggle => {
        toggle.addEventListener('change', () => {
            const name = toggle.id.split('-')[1];
            apiPost(`/outputs/toggle/${name}`);
        });
    });

    connect();
});