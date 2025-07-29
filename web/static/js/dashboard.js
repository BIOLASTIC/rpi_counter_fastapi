document.addEventListener('DOMContentLoaded', function () {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${window.location.host}/ws`;
    let socket;

    // Control elements
    const startBtn = document.getElementById('start-batch-btn');
    const stopBtn = document.getElementById('stop-batch-btn');
    const resetTotalBtn = document.getElementById('reset-total-button');
    const batchSizeInput = document.getElementById('batch-size-input');

    // Display elements
    const totalCountEl = document.getElementById('total-box-count');
    const systemModeEl = document.getElementById('system-mode');
    const batchProgressEl = document.getElementById('batch-progress');
    const batchTargetEl = document.getElementById('batch-target');
    
    function connect() {
        socket = new WebSocket(wsUrl);
        socket.onopen = () => console.log('Dashboard WebSocket connected.');
        socket.onclose = () => setTimeout(connect, 2000);
        socket.onerror = (err) => {
            console.error('WebSocket error on dashboard.', err);
            socket.close();
        };

        socket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            switch (message.type) {
                case 'detection_status':
                    if(totalCountEl) totalCountEl.textContent = message.data.total_count;
                    break;
                case 'orchestration_status':
                    updateOrchestrationStatus(message.data);
                    break;
                case 'system_status':
                    updateSystemStatus(message.data);
                    break;
            }
        };
    }

    function updateOrchestrationStatus(data) {
        if(systemModeEl) systemModeEl.textContent = data.mode.toUpperCase();
        if(batchProgressEl) batchProgressEl.textContent = data.batch_progress;
        if(batchTargetEl) batchTargetEl.textContent = data.batch_target;
    }
    
    function updateSystemStatus(data) {
        // THE FIX: Loop over all potential camera images
        if (data.last_event_images) {
            for (const [cam_id, image_path] of Object.entries(data.last_event_images)) {
                const imgEl = document.getElementById(`event-capture-image-${cam_id}`);
                const linkEl = document.getElementById(`event-capture-link-${cam_id}`);
                if (imgEl && linkEl && image_path && imgEl.src !== image_path) {
                    imgEl.src = image_path;
                    linkEl.href = image_path;
                }
            }
        }
    }

    if (startBtn) {
        startBtn.addEventListener('click', async () => {
            const size = parseInt(batchSizeInput.value, 10);
            if (size > 0) {
                await fetch('/api/v1/orchestration/batch/start', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ size: size })
                });
            }
        });
    }

    if(stopBtn) {
        stopBtn.addEventListener('click', async () => {
            await fetch('/api/v1/orchestration/batch/stop', { method: 'POST' });
        });
    }

    if(resetTotalBtn) {
        resetTotalBtn.addEventListener('click', async () => {
            if (confirm('Are you sure you want to reset the total all-time counter to zero?')) {
                await fetch('/api/v1/detection/reset', { method: 'POST' });
            }
        });
    }

    connect();
});