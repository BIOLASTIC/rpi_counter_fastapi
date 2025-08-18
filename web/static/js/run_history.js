// rpi_counter_fastapi-dev2/web/static/js/run_history.js

document.addEventListener('DOMContentLoaded', function () {
    const tableBody = document.getElementById('history-table-body');
    const filterForm = document.getElementById('filter-form');
    const resetBtn = document.getElementById('reset-filter-btn');
    const detectionsModal = new bootstrap.Modal(document.getElementById('detections-modal'));
    const detectionsContainer = document.getElementById('detections-grid-container');
    const modalTitle = document.getElementById('detections-modal-title');
    const downloadZipBtn = document.getElementById('download-run-zip-btn');
    const detectionTemplate = document.getElementById('detection-item-template');

    let products = [];
    let operators = [];

    async function fetchData(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Fetch error:', error);
            return [];
        }
    }

    async function populateFilters() {
        [products, operators] = await Promise.all([
            fetchData('/api/v1/products/'),
            fetchData('/api/v1/operators/')
        ]);
        
        const productFilter = document.getElementById('filter-product');
        productFilter.innerHTML = '<option value="">All Products</option>';
        products.forEach(p => productFilter.add(new Option(p.name, p.id)));

        const operatorFilter = document.getElementById('filter-operator');
        operatorFilter.innerHTML = '<option value="">All Operators</option>';
        operators.forEach(o => operatorFilter.add(new Option(o.name, o.id)));
    }

    async function loadHistory(params = {}) {
        tableBody.innerHTML = '<tr><td colspan="8" class="text-center">Loading...</td></tr>';
        const query = new URLSearchParams(params).toString();
        const runs = await fetchData(`/api/v1/run-history/?${query}`);

        tableBody.innerHTML = '';
        if (runs.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="8" class="text-center">No runs found for the selected criteria.</td></tr>';
            return;
        }

        runs.forEach(run => {
            const row = tableBody.insertRow();
            const targetCount = run.object_profile_snapshot?.target_count || 0;
            
            row.innerHTML = `
                <td>${new Date(run.start_timestamp).toLocaleString()}</td>
                <td><span class="badge bg-${getStatusColor(run.status)}">${run.status}</span></td>
                <td>${run.duration_seconds !== null ? `${run.duration_seconds}s` : '--'}</td>
                <td>${run.batch_code}</td>
                <td>${run.product?.name || 'N/A'}</td>
                <td>${run.operator?.name || 'N/A'}</td>
                <td class="text-end">${run.detected_items_count} / ${targetCount === 0 ? '∞' : targetCount}</td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary view-detections-btn" data-run-id="${run.id}" data-batch-code="${run.batch_code}">View Detections</button>
                </td>
            `;
        });
    }

    function getStatusColor(status) {
        switch (status) {
            case 'Completed': return 'success';
            case 'Failed': return 'danger';
            case 'Aborted by User': return 'warning';
            case 'Running': return 'info';
            default: return 'secondary';
        }
    }

    async function displayDetections(runId, batchCode) {
        modalTitle.textContent = `Detection Events for Run #${runId} (${batchCode})`;
        detectionsContainer.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"></div></div>';
        downloadZipBtn.href = `/api/v1/run-history/${runId}/download-images`;
        detectionsModal.show();
        
        const detections = await fetchData(`/api/v1/run-history/${runId}/detections`);
        detectionsContainer.innerHTML = '';
        
        if (detections.length === 0) {
            detectionsContainer.innerHTML = '<p class="text-center text-muted">No detection events with images were recorded for this run.</p>';
            return;
        }
        
        detections.forEach(det => {
            const item = detectionTemplate.content.cloneNode(true);
            
            item.querySelector('.serial-number').textContent = det.serial_number;
            item.querySelector('.timestamp').textContent = new Date(det.timestamp).toLocaleString();
            item.querySelector('.original-image').src = det.image_path || '/static/images/placeholder.jpg';
            item.querySelector('.annotated-image').src = det.annotated_image_path || det.image_path || '/static/images/placeholder.jpg';
            
            // --- THIS IS THE FIX ---
            // Populate the text details from the 'results' object
            const details = {
                qc: item.querySelector('.details-qc'),
                category: item.querySelector('.details-category'),
                size: item.querySelector('.details-size'),
                defects: item.querySelector('.details-defects'),
            };

            const idResults = det.results ? det.results.identification_results || {} : {};
            const qc = idResults.qc;
            details.qc.textContent = qc ? qc.overall_status : 'N/A';
            const category = idResults.category;
            details.category.textContent = category ? `${category.detected_product_type} (${(category.confidence * 100).toFixed(1)}%)` : 'N/A';
            const size = idResults.size;
            details.size.textContent = (size && size.detected_product_size) ? size.detected_product_size : 'N/A';
            const defects = idResults.defects && idResults.defects.defects ? idResults.defects.defects : [];
            details.defects.textContent = defects.length > 0 ? `${defects.length} Found` : 'None Detected';
            // --- END OF FIX ---

            detectionsContainer.appendChild(item);
        });
    }

    tableBody.addEventListener('click', function (e) {
        if (e.target && e.target.classList.contains('view-detections-btn')) {
            const runId = e.target.dataset.runId;
            const batchCode = e.target.dataset.batchCode;
            displayDetections(runId, batchCode);
        }
    });

    filterForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const params = {
            start_date: document.getElementById('filter-start-date').value,
            end_date: document.getElementById('filter-end-date').value,
            product_id: document.getElementById('filter-product').value,
            operator_id: document.getElementById('filter-operator').value,
            batch_code: document.getElementById('filter-batch-code').value,
        };
        // Remove empty params
        Object.keys(params).forEach(key => params[key] === '' && delete params[key]);
        loadHistory(params);
    });

    resetBtn.addEventListener('click', function () {
        filterForm.reset();
        loadHistory();
    });

    // Initial Load
    populateFilters();
    loadHistory();
});