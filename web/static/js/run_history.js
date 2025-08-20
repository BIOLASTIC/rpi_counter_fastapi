// rpi_counter_fastapi-apintrigation/web/static/js/run_history.js

document.addEventListener('DOMContentLoaded', function() {
    const historyTableBody = document.getElementById('history-table-body');
    const filterForm = document.getElementById('filter-form');
    const resetFilterBtn = document.getElementById('reset-filter-btn');
    const productFilter = document.getElementById('filter-product');
    const operatorFilter = document.getElementById('filter-operator');

    const detectionsModal = new bootstrap.Modal(document.getElementById('detections-modal'));
    const detectionsGridContainer = document.getElementById('detections-grid-container');
    const modalTitle = document.getElementById('detections-modal-title');
    const downloadZipBtn = document.getElementById('download-run-zip-btn');
    const detectionItemTemplate = document.getElementById('detection-item-template');

    // Helper to safely access nested properties in the JSON response
    const get = (path, obj) => path.reduce((xs, x) => (xs && xs[x] != null) ? xs[x] : null, obj);

    async function populateFilters() {
        try {
            const [productsRes, operatorsRes] = await Promise.all([
                fetch('/api/v1/products/'),
                fetch('/api/v1/operators/')
            ]);
            const products = await productsRes.json();
            const operators = await operatorsRes.json();

            productFilter.innerHTML = '<option value="">All Products</option>';
            products.forEach(p => {
                productFilter.insertAdjacentHTML('beforeend', `<option value="${p.id}">${p.name}</option>`);
            });

            operatorFilter.innerHTML = '<option value="">All Operators</option>';
            operators.forEach(o => {
                operatorFilter.insertAdjacentHTML('beforeend', `<option value="${o.id}">${o.name}</option>`);
            });
        } catch (error) {
            console.error('Failed to populate filters:', error);
        }
    }

    async function fetchAndRenderHistory(params = {}) {
        historyTableBody.innerHTML = '<tr><td colspan="8" class="text-center">Loading...</td></tr>';
        const query = new URLSearchParams(params).toString();
        try {
            const response = await fetch(`/api/v1/run-history/?${query}`);
            if (!response.ok) throw new Error('Failed to fetch run history');
            const runs = await response.json();
            renderHistory(runs);
        } catch (error) {
            console.error('Error fetching run history:', error);
            historyTableBody.innerHTML = '<tr><td colspan="8" class="text-center text-danger">Failed to load run history.</td></tr>';
        }
    }

    function renderHistory(runs) {
        historyTableBody.innerHTML = '';
        if (runs.length === 0) {
            historyTableBody.innerHTML = '<tr><td colspan="8" class="text-center">No runs found for the selected filters.</td></tr>';
            return;
        }

        runs.forEach(run => {
            const startTime = new Date(run.start_timestamp).toLocaleString();
            const statusBadge = `<span class="badge bg-${getStatusColor(run.status)}">${run.status}</span>`;
            const duration = run.duration_seconds ? `${run.duration_seconds}s` : 'N/A';
            const target = run.object_profile_snapshot?.target_count > 0 ? run.object_profile_snapshot.target_count : '∞';

            const row = `
                <tr>
                    <td>${startTime}</td>
                    <td>${statusBadge}</td>
                    <td>${duration}</td>
                    <td>${run.batch_code}</td>
                    <td>${run.product?.name || 'N/A'}</td>
                    <td>${run.operator?.name || 'N/A'}</td>
                    <td class="text-end">${run.detected_items_count} / ${target}</td>
                    <td class="text-end">
                        <button class="btn btn-sm btn-outline-primary view-detections-btn" data-run-id="${run.id}" data-batch-code="${run.batch_code}">
                            <i class="bi bi-images"></i> View
                        </button>
                    </td>
                </tr>
            `;
            historyTableBody.insertAdjacentHTML('beforeend', row);
        });
    }

    async function openDetectionsModal(runId, batchCode) {
        modalTitle.textContent = `Detections for Run #${runId} (${batchCode})`;
        detectionsGridContainer.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        downloadZipBtn.href = `/api/v1/run-history/${runId}/download-images`;
        detectionsModal.show();

        try {
            const response = await fetch(`/api/v1/run-history/${runId}/detections`);
            if (!response.ok) throw new Error('Failed to load detection events.');
            const detections = await response.json();

            detectionsGridContainer.innerHTML = '';
            if (detections.length === 0) {
                detectionsGridContainer.innerHTML = '<p class="text-center text-muted">No detection events were recorded for this run.</p>';
                return;
            }

            detections.forEach(det => {
                const itemClone = detectionItemTemplate.content.cloneNode(true);
                const details = det.details || {};

                itemClone.querySelector('.serial-number').textContent = det.serial_number;
                itemClone.querySelector('.timestamp').textContent = new Date(det.timestamp).toLocaleString();
                
                const originalImg = itemClone.querySelector('.original-image');
                originalImg.src = det.image_path || '/static/images/placeholder.jpg';
                itemClone.querySelector('.original-image-link').href = det.image_path || '#';

                const annotatedImg = itemClone.querySelector('.annotated-image');
                annotatedImg.src = det.annotated_image_path || det.image_path || '/static/images/placeholder.jpg';
                itemClone.querySelector('.annotated-image-link').href = det.annotated_image_path || '#';

                // Populate Summary
                const qcStatus = get(['qc_summary', 'overall_status'], details) || 'N/A';
                const qcStatusEl = itemClone.querySelector('.details-qc-status');
                qcStatusEl.textContent = qcStatus;
                qcStatusEl.className = `details-qc-status status-${qcStatus}`;

                const qcConfidence = get(['qc_summary', 'confidence'], details);
                itemClone.querySelector('.details-qc-confidence').textContent = qcConfidence ? `${(qcConfidence * 100).toFixed(1)}%` : 'N/A';

                const categoryName = get(['category_summary', 'detected_type'], details) || 'N/A';
                itemClone.querySelector('.details-category-name').textContent = categoryName;
                
                const categoryConfidence = get(['category_summary', 'confidence'], details);
                itemClone.querySelector('.details-category-confidence').textContent = categoryConfidence ? `${(categoryConfidence * 100).toFixed(1)}%` : 'N/A';
                
                // Populate Validation List
                const validationList = itemClone.querySelector('.validation-list');
                validationList.innerHTML = ''; // Clear default
                const validationChecks = get(['validation_results', 'checks'], details);
                if (validationChecks && validationChecks.length > 0) {
                    validationChecks.forEach(check => {
                        const isPass = check.status === 'PASS';
                        const icon = isPass ? '<i class="bi bi-check-circle-fill text-success"></i>' : '<i class="bi bi-x-circle-fill text-danger"></i>';
                        const listItem = `
                            <li class="list-group-item d-flex justify-content-between align-items-center">
                                <div>${icon} ${check.check_type}</div>
                                <span class="badge ${isPass ? 'bg-success' : 'bg-danger'}">${check.value}</span>
                            </li>`;
                        validationList.insertAdjacentHTML('beforeend', listItem);
                    });
                } else {
                     validationList.innerHTML = '<li class="list-group-item text-muted small">No geometric checks ran.</li>';
                }

                detectionsGridContainer.appendChild(itemClone);
            });

        } catch (error) {
            console.error(error);
            detectionsGridContainer.innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
        }
    }

    function getStatusColor(status) {
        switch (status) {
            case 'Completed': return 'success';
            case 'Failed': return 'danger';
            case 'Aborted by User': return 'warning';
            case 'Running': return 'primary';
            default: return 'secondary';
        }
    }

    filterForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const params = {
            start_date: document.getElementById('filter-start-date').value,
            end_date: document.getElementById('filter-end-date').value,
            product_id: productFilter.value,
            operator_id: operatorFilter.value,
            batch_code: document.getElementById('filter-batch-code').value.trim()
        };
        // Remove empty params
        Object.keys(params).forEach(key => params[key] === '' && delete params[key]);
        fetchAndRenderHistory(params);
    });

    resetFilterBtn.addEventListener('click', () => {
        filterForm.reset();
        fetchAndRenderHistory();
    });

    historyTableBody.addEventListener('click', (e) => {
        const viewBtn = e.target.closest('.view-detections-btn');
        if (viewBtn) {
            openDetectionsModal(viewBtn.dataset.runId, viewBtn.dataset.batchCode);
        }
    });

    // Initial Load
    populateFilters();
    fetchAndRenderHistory();
});