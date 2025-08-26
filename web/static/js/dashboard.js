document.addEventListener('DOMContentLoaded', function () {
    // --- Element Cache ---
    const elements = {
        runStatus: document.getElementById('run-status'),
        processedCount: document.getElementById('processed-count'),
        targetCount: document.getElementById('target-count'),
        progressBarFill: document.getElementById('progress-bar-fill'),
        progressBarText: document.getElementById('progress-bar-text'),
        recipeName: document.getElementById('recipe-name'),
        batchCode: document.getElementById('batch-code'),
        operatorName: document.getElementById('operator-name'),
        inFlightCount: document.getElementById('in-flight-count'),
        qcImage: document.getElementById('qc-image'),
        qcStatus: document.getElementById('qc-status'),
        qcDetailsList: document.getElementById('qc-details-list'),
        conveyorBelt: document.getElementById('conveyor-belt')
    };

    // --- WebSocket Connection ---
    const socket = new WebSocket(`ws://${window.location.host}/ws`);

    socket.onopen = () => console.log("Dashboard WebSocket: Connection established.");
    socket.onclose = () => console.log("Dashboard WebSocket: Connection closed.");
    socket.onerror = (error) => console.error("Dashboard WebSocket Error:", error);

    socket.onmessage = function (event) {
        try {
            const message = JSON.parse(event.data);
            switch (message.type) {
                case 'full_status':
                    updateDashboard(message.data);
                    break;
                case 'qc_update':
                    updateQcPanel(message.data);
                    break;
                case 'new_item_detected':
                    animateProduct(message.data.serial_number);
                    break;
            }
        } catch (e) {
            console.error("Failed to parse WebSocket message:", e);
        }
    };

    // --- Update Functions ---

    function updateDashboard(data) {
        if (!data) return;

        // Update Orchestration Panel
        if (data.orchestration) {
            const orc = data.orchestration;
            elements.runStatus.textContent = orc.mode || 'N/A';
            updateStatusColor(elements.runStatus, orc.mode);
            
            elements.processedCount.textContent = orc.run_progress || 0;
            elements.targetCount.textContent = `/ ${orc.target_count || 0}`;
            elements.recipeName.textContent = orc.active_profile || 'None';
            elements.batchCode.textContent = orc.batch_code || 'N/A';
            elements.operatorName.textContent = orc.operator_name || 'N/A';

            const progress = (orc.target_count > 0) 
                ? (orc.run_progress / orc.target_count) * 100 
                : 0;
            elements.progressBarFill.style.width = `${Math.min(progress, 100)}%`;
            elements.progressBarText.textContent = `${Math.round(progress)}%`;
        }

        // Update System Stats
        if (data.system) {
            elements.inFlightCount.textContent = data.system.in_flight_count || 0;
        }
    }

    function updateStatusColor(element, status) {
        element.classList.remove('text-success', 'text-warning', 'text-danger', 'text-secondary');
        switch (status) {
            case 'Running':
                element.classList.add('text-success');
                break;
            case 'Paused (Between Batches)':
            case 'Post-Run Delay':
                element.classList.add('text-warning');
                break;
            case 'Stopped':
                element.classList.add('text-danger');
                break;
            default:
                element.classList.add('text-secondary');
                break;
        }
    }

    function updateQcPanel(data) {
        elements.qcImage.src = data.annotated_path || '/static/images/placeholder.jpg';
        
        const summary = data.results || {};
        const status = summary.overall_status || 'PENDING';
        elements.qcStatus.textContent = status;
        updateStatusColor(elements.qcStatus, status === 'ACCEPT' ? 'Running' : 'Stopped');

        elements.qcDetailsList.innerHTML = ''; // Clear previous details
        const details = [
            { label: 'Reason', value: summary.reject_reason },
            { label: 'Detected Type', value: summary.primary_detection?.type },
            { label: 'Confidence', value: summary.primary_detection?.confidence },
            { label: 'Total Objects', value: summary.detection_count }
        ];

        details.forEach(item => {
            if (item.value !== null && item.value !== undefined) {
                const li = document.createElement('li');
                li.className = 'list-group-item bg-dark text-white';
                li.innerHTML = `<strong>${item.label}:</strong> ${item.value}`;
                elements.qcDetailsList.appendChild(li);
            }
        });
    }

    function animateProduct(serialNumber) {
        const productDiv = document.createElement('div');
        productDiv.className = 'conveyor-product';
        productDiv.id = `product-${serialNumber}`;
        productDiv.innerHTML = '<i class="fas fa-box"></i>';
        
        elements.conveyorBelt.appendChild(productDiv);

        // This small delay forces the browser to apply the initial CSS state
        // before applying the final state, which is what triggers the transition.
        setTimeout(() => {
            productDiv.style.right = '100%';
        }, 10);

        // Clean up the element from the DOM after the animation completes
        productDiv.addEventListener('transitionend', () => {
            productDiv.remove();
        });
    }
});