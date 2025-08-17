// rpi_counter_fastapi-dev2/web/static/js/run_history.js

document.addEventListener('DOMContentLoaded', function () {
    const historyTableBody = document.getElementById('history-table-body');
    const filterForm = document.getElementById('filter-form');
    const resetFilterBtn = document.getElementById('reset-filter-btn');
    const detectionsModal = new bootstrap.Modal(document.getElementById('detections-modal'));
    const modalTitle = document.getElementById('detections-modal-title');
    const modalSubtitle = document.getElementById('detections-modal-subtitle');
    const modalBodyContent = document.getElementById('detections-grid-container');
    const downloadZipBtn = document.getElementById('download-run-zip-btn');

    const fetchRunHistory = async (params = {}) => {
        const query = new URLSearchParams(params).toString();
        try {
            const response = await fetch(`/api/v1/run-history/?${query}`);
            if (!response.ok) throw new Error('Failed to fetch run history');
            const runs = await response.json();
            renderHistoryTable(runs);
        } catch (error) {
            console.error('Error fetching run history:', error);
            historyTableBody.innerHTML = `<tr><td colspan="8" class="text-center text-danger">Failed to load run history.</td></tr>`;
        }
    };

    const renderHistoryTable = (runs) => {
        historyTableBody.innerHTML = '';
        if (runs.length === 0) {
            historyTableBody.innerHTML = `<tr><td colspan="8" class="text-center">No runs found for the selected criteria.</td></tr>`;
            return;
        }
        runs.forEach(run => {
            const row = document.createElement('tr');
            const target = run.object_profile_snapshot?.target_count || 0;
            const statusColor = {
                'Completed': 'bg-success',
                'Running': 'bg-primary',
                'Failed': 'bg-danger',
                'Aborted by User': 'bg-warning text-dark'
            }[run.status] || 'bg-secondary';

            row.innerHTML = `
                <td>${new Date(run.start_timestamp).toLocaleString()}</td>
                <td><span class="badge ${statusColor}">${run.status}</span></td>
                <td>${run.duration_seconds !== null ? `${run.duration_seconds}s` : 'N/A'}</td>
                <td>${run.batch_code}</td>
                <td>${run.product?.name || 'N/A'}</td>
                <td>${run.operator?.name || 'N/A'}</td>
                <td class="text-end">${run.detected_items_count} / ${target === 0 ? '∞' : target}</td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-info view-detections-btn" data-run-id="${run.id}" data-batch-code="${run.batch_code}">
                        View Images
                    </button>
                </td>
            `;
            historyTableBody.appendChild(row);
        });
    };

    historyTableBody.addEventListener('click', (e) => {
        const viewBtn = e.target.closest('.view-detections-btn');
        if (viewBtn) {
            const runId = viewBtn.dataset.runId;
            const batchCode = viewBtn.dataset.batchCode;
            openDetectionsModal(runId, batchCode);
        }
    });

    const openDetectionsModal = async (runId, batchCode) => {
        modalTitle.textContent = `Detection Events for Run #${runId} (${batchCode})`;
        modalBodyContent.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        downloadZipBtn.href = `/api/v1/run-history/${runId}/download-images`;
        detectionsModal.show();

        try {
            const response = await fetch(`/api/v1/run-history/${runId}/detections`);
            if (!response.ok) throw new Error('Failed to fetch detections.');
            const detections = await response.json();
            
            modalBodyContent.innerHTML = '';
            if (detections.length === 0) {
                modalBodyContent.innerHTML = '<p class="text-center">No images were captured for this run.</p>';
                downloadZipBtn.classList.add('disabled');
                return;
            }
            
            downloadZipBtn.classList.remove('disabled');

            detections.forEach(det => {
                const itemHtml = `
                    <div class="card mb-3">
                        <div class="card-header small text-muted">
                            <strong>Serial Number:</strong> ${det.serial_number} | <strong>Timestamp:</strong> ${new Date(det.timestamp).toLocaleString()}
                        </div>
                        <div class="card-body">
                            <div class="row g-3">
                                <div class="col-md-6">
                                    <h6 class="text-center">Original Image</h6>
                                    <a href="${det.image_path}" target="_blank">
                                        <img src="${det.image_path}" class="img-fluid rounded border" alt="Original capture">
                                    </a>
                                </div>
                                <div class="col-md-6">
                                    <h6 class="text-center">Annotated AI Result</h6>
                                    ${det.annotated_image_path ? `
                                        <a href="${det.annotated_image_path}" target="_blank">
                                            <img src="${det.annotated_image_path}" class="img-fluid rounded border" alt="Annotated result">
                                        </a>
                                    ` : `
                                        <div class="d-flex align-items-center justify-content-center h-100 bg-light-subtle border rounded" style="min-height: 200px;">
                                            <p class="text-muted">No annotation available.</p>
                                        </div>
                                    `}
                                </div>
                            </div>
                        </div>
                    </div>
                `;
                modalBodyContent.insertAdjacentHTML('beforeend', itemHtml);
            });

        } catch (error) {
            console.error('Error in openDetectionsModal:', error);
            modalBodyContent.innerHTML = '<p class="text-center text-danger">Failed to load detection images.</p>';
        }
    };
    
    filterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const params = {
            start_date: document.getElementById('filter-start-date').value,
            end_date: document.getElementById('filter-end-date').value,
            product_id: document.getElementById('filter-product').value,
            operator_id: document.getElementById('filter-operator').value,
            batch_code: document.getElementById('filter-batch-code').value,
        };
        Object.keys(params).forEach(key => {
            if (!params[key]) delete params[key];
        });
        fetchRunHistory(params);
    });

    resetFilterBtn.addEventListener('click', () => {
        filterForm.reset();
        fetchRunHistory();
    });

    const populateFilters = async () => {
        try {
            const [productsRes, operatorsRes] = await Promise.all([
                fetch('/api/v1/products/'),
                fetch('/api/v1/operators/')
            ]);
            const products = await productsRes.json();
            const operators = await operatorsRes.json();
            
            const productSelect = document.getElementById('filter-product');
            productSelect.innerHTML = '<option value="">All Products</option>';
            products.forEach(p => productSelect.innerHTML += `<option value="${p.id}">${p.name}</option>`);

            const operatorSelect = document.getElementById('filter-operator');
            operatorSelect.innerHTML = '<option value="">All Operators</option>';
            operators.forEach(o => operatorSelect.innerHTML += `<option value="${o.id}">${o.name}</option>`);

        } catch (error) {
            console.error("Failed to populate filters:", error);
        }
    };

    fetchRunHistory();
    populateFilters();
});