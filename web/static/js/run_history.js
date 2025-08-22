// rpi_counter_fastapi-apinaudio/web/static/js/run_history.js

document.addEventListener('DOMContentLoaded', function () {
    const tableBody = document.getElementById('history-table-body');
    const filterForm = document.getElementById('filter-form');
    const resetBtn = document.getElementById('reset-filter-btn');

    // Modal elements
    const detectionsModal = new bootstrap.Modal(document.getElementById('detections-modal'));
    const modalTitle = document.getElementById('detections-modal-title');
    const modalSubtitle = document.getElementById('detections-modal-subtitle');
    const modalGridContainer = document.getElementById('detections-grid-container');
    const downloadZipBtn = document.getElementById('download-run-zip-btn');

    async function fetchAndRenderHistory() {
        const params = new URLSearchParams(new FormData(filterForm));
        const startDate = document.getElementById('filter-start-date').value;
        const endDate = document.getElementById('filter-end-date').value;

        // Convert local datetime to ISO string for the query
        if (startDate) params.set('start_date', new Date(startDate).toISOString());
        if (endDate) params.set('end_date', new Date(endDate).toISOString());

        try {
            const response = await fetch(`/api/v1/run-history/?${params.toString()}`);
            const runs = await response.json();
            renderTable(runs);
        } catch (error) {
            console.error("Failed to fetch run history:", error);
            tableBody.innerHTML = '<tr><td colspan="8" class="text-center text-danger">Error loading data.</td></tr>';
        }
    }

    function renderTable(runs) {
        if (!runs || runs.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="8" class="text-center">No run history found for the selected filters.</td></tr>';
            return;
        }

        tableBody.innerHTML = runs.map(run => `
            <tr>
                <td>${run.start_timestamp_local || new Date(run.start_timestamp).toLocaleString()}</td>
                <td><span class="badge ${getStatusClass(run.status)}">${run.status}</span></td>
                <td>${run.duration_seconds !== null ? `${run.duration_seconds}s` : 'N/A'}</td>
                <td>${run.batch_code}</td>
                <td>${run.product ? run.product.name : 'N/A'}</td>
                <td>${run.operator ? run.operator.name : 'N/A'}</td>
                <td class="text-end">${run.detected_items_count} / ${run.object_profile_snapshot.target_count || '∞'}</td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary view-detections-btn" data-run-id="${run.id}" data-batch-code="${run.batch_code}">
                        View
                    </button>
                </td>
            </tr>
        `).join('');
    }

    function getStatusClass(status) {
        switch (status) {
            case 'Completed': return 'bg-success';
            case 'Failed': return 'bg-danger';
            case 'Aborted by User': return 'bg-warning text-dark';
            case 'Running': return 'bg-info text-dark';
            default: return 'bg-secondary';
        }
    }

    async function showDetectionsModal(runId, batchCode) {
        modalTitle.textContent = `Detection Events for Batch: ${batchCode}`;
        modalGridContainer.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        downloadZipBtn.href = `/api/v1/run-history/${runId}/download-images`;
        detectionsModal.show();

        try {
            const response = await fetch(`/api/v1/run-history/${runId}/detections`);
            const detections = await response.json();
            renderDetections(detections);
        } catch (error) {
            console.error('Failed to fetch detections:', error);
            modalGridContainer.innerHTML = '<div class="alert alert-danger">Could not load detection events.</div>';
        }
    }

    function renderDetections(detections) {
        if (!detections || detections.length === 0) {
            modalGridContainer.innerHTML = '<p class="text-center text-muted">No detection images were recorded for this run.</p>';
            return;
        }

        modalGridContainer.innerHTML = '';
        const template = document.getElementById('detection-item-template');

        detections.forEach(det => {
            const clone = template.content.cloneNode(true);
            clone.querySelector('.serial-number').textContent = det.serial_number;
            clone.querySelector('.timestamp').textContent = new Date(det.timestamp).toLocaleString();

            if (det.image_path) {
                clone.querySelector('.original-image-link').href = det.image_path;
                clone.querySelector('.original-image').src = det.image_path;
            }
            if (det.annotated_image_path) {
                clone.querySelector('.annotated-image-link').href = det.annotated_image_path;
                clone.querySelector('.annotated-image').src = det.annotated_image_path;
            }

            const qcSummary = det.details?.qc_summary || {};
            const catSummary = det.details?.category_summary || {};
            const validationChecks = det.details?.validation_results?.checks || [];

            const qcStatusEl = clone.querySelector('.details-qc-status');
            qcStatusEl.textContent = qcSummary.overall_status || 'N/A';
            qcStatusEl.className = `details-qc-status status-${qcSummary.overall_status}`;

            clone.querySelector('.details-qc-confidence').textContent = qcSummary.confidence ? `${(qcSummary.confidence * 100).toFixed(1)}%` : '--';
            clone.querySelector('.details-category-name').textContent = catSummary.detected_type || 'N/A';
            clone.querySelector('.details-category-confidence').textContent = catSummary.confidence ? `${(catSummary.confidence * 100).toFixed(1)}%` : '--';

            const validationList = clone.querySelector('.validation-list');
            validationList.innerHTML = '';
            if (validationChecks.length > 0) {
                validationChecks.forEach(check => {
                    const li = document.createElement('li');
                    li.className = 'list-group-item d-flex justify-content-between align-items-center';
                    li.innerHTML = `
                        <span>${check.check_type}: <span class="fw-bold">${check.value}</span></span>
                        <span class="badge ${check.status === 'PASS' ? 'bg-success' : 'bg-danger'}">${check.status}</span>
                    `;
                    validationList.appendChild(li);
                });
            } else {
                validationList.innerHTML = '<li class="list-group-item text-muted small">No geometric validation performed.</li>';
            }
            
            modalGridContainer.appendChild(clone);
        });
    }
    
    async function populateFilters() {
        try {
            const [operatorsRes, productsRes] = await Promise.all([
                fetch('/api/v1/operators/'),
                fetch('/api/v1/products/')
            ]);
            const operators = await operatorsRes.json();
            const products = await productsRes.json();

            const operatorFilter = document.getElementById('filter-operator');
            operatorFilter.innerHTML = '<option value="">All Operators</option>';
            operators.forEach(op => {
                operatorFilter.innerHTML += `<option value="${op.id}">${op.name}</option>`;
            });

            const productFilter = document.getElementById('filter-product');
            productFilter.innerHTML = '<option value="">All Products</option>';
            products.forEach(p => {
                productFilter.innerHTML += `<option value="${p.id}">${p.name}</option>`;
            });
        } catch (error) {
            console.error("Failed to populate filters:", error);
        }
    }

    filterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        fetchAndRenderHistory();
    });

    resetBtn.addEventListener('click', () => {
        filterForm.reset();
        fetchAndRenderHistory();
    });

    tableBody.addEventListener('click', (e) => {
        const button = e.target.closest('.view-detections-btn');
        if (button) {
            showDetectionsModal(button.dataset.runId, button.dataset.batchCode);
        }
    });

    // Initial Load
    populateFilters();
    fetchAndRenderHistory();
});