document.addEventListener('DOMContentLoaded', function() {
    // --- Element Cache ---
    const totalCountEl = document.getElementById('total-box-count');
    const resetTotalButton = document.getElementById('reset-total-button');
    
    // Batch control elements
    const batchSizeInput = document.getElementById('batch-size-input');
    const startBatchBtn = document.getElementById('start-batch-btn');
    const stopBatchBtn = document.getElementById('stop-batch-btn');
    const systemModeEl = document.getElementById('system-mode');
    const batchProgressEl = document.getElementById('batch-progress');
    const batchTargetEl = document.getElementById('batch-target');

    // Image elements
    const eventImageEl = document.getElementById('event-image');
    const eventPlaceholderEl = document.getElementById('event-placeholder');
    const surveillanceImageEl = document.getElementById('surveillance-image');
    const surveillancePlaceholderEl = document.getElementById('surveillance-placeholder');

    const API_BASE = '/api/v1';

    // --- WebSocket Handler ---
    function connectWebSocket() {
        const socket = new WebSocket(`ws://${window.location.host}/ws`);

        socket.onmessage = function(event) {
            const message = JSON.parse(event.data);
            
            if (message.type === 'detection_status' && totalCountEl) {
                totalCountEl.textContent = message.data.total_count;
            }
            if (message.type === 'orchestration_status') {
                updateOrchestrationStatus(message.data);
            }
            if (message.type === 'system_status') {
                updateImage('event', message.data.last_event_image);
                updateImage('surveillance', message.data.last_surveillance_image);
            }
        };

        socket.onclose = function() {
            console.log('WebSocket disconnected. Reconnecting in 3 seconds...');
            setTimeout(connectWebSocket, 3000);
        };
    }

    // --- UI Update Functions ---
    function updateOrchestrationStatus(data) {
        if (!systemModeEl) return; // Guard against missing elements
        systemModeEl.textContent = data.mode.toUpperCase();
        batchProgressEl.textContent = data.batch_progress;
        batchTargetEl.textContent = data.batch_target;

        systemModeEl.classList.remove('bg-success', 'bg-warning', 'bg-secondary');
        if (data.mode === 'Running Batch') {
            systemModeEl.classList.add('bg-success');
        } else if (data.mode === 'Waiting Between Batches') {
            systemModeEl.classList.add('bg-warning');
        } else {
            systemModeEl.classList.add('bg-secondary');
        }
    }
    
    function updateImage(type, path) {
        let imgElement = type === 'event' ? eventImageEl : surveillanceImageEl;
        let placeholderElement = type === 'event' ? eventPlaceholderEl : surveillancePlaceholderEl;
        if (!imgElement || !placeholderElement) return;

        if (path && imgElement.src.includes(path) === false) {
            imgElement.src = path + '?t=' + new Date().getTime();
            imgElement.style.display = 'block';
            placeholderElement.style.display = 'none';
        }
    }

    async function postApiRequest(endpoint, options = {}) {
        try {
            const response = await fetch(`${API_BASE}${endpoint}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, ...options });
            if (!response.ok) { throw new Error((await response.json()).detail || `HTTP error! status: ${response.status}`); }
            return await response.json();
        } catch (error) {
            console.error(`API request to ${endpoint} failed:`, error);
            throw error;
        }
    }

    // --- Event Listeners (DEFINITIVE FIX with defensive checks) ---

    // Check if the element exists before adding a listener
    if (resetTotalButton) {
        resetTotalButton.addEventListener('click', () => {
            postApiRequest('/detection/reset').catch(err => alert(err.message));
        });
    }

    if (startBatchBtn) {
        startBatchBtn.addEventListener('click', () => {
            const size = parseInt(batchSizeInput.value, 10);
            if (size > 0) {
                postApiRequest('/orchestration/batch/start', {
                    body: JSON.stringify({ size: size })
                }).catch(err => alert(`Failed to start batch: ${err.message}`));
            } else {
                alert("Please enter a valid batch size greater than 0.");
            }
        });
    }

    if (stopBatchBtn) {
        stopBatchBtn.addEventListener('click', () => {
            postApiRequest('/orchestration/batch/stop').catch(err => alert(`Failed to stop process: ${err.message}`));
        });
    }

    // --- Initial Kick-off ---
    connectWebSocket();
});