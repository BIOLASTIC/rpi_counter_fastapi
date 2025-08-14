// rpi_counter_fastapi-dev2/web/static/js/run_history.js

document.addEventListener('DOMContentLoaded', () => {
    // --- Elements ---
    const tableBody = document.getElementById('history-table-body');
    const filterForm = document.getElementById('filter-form');
    const resetBtn = document.getElementById('reset-filter-btn');
    const productFilter = document.getElementById('filter-product');
    const operatorFilter = document.getElementById('filter-operator');

    const modal = new bootstrap.Modal(document.getElementById('detections-modal'));
    const modalTitle = document.getElementById('detections-modal-title');
    const modalSubtitle = document.getElementById('detections-modal-subtitle');
    const modalBody = document.getElementById('detections-modal-body-content');
    const downloadZipBtn = document.getElementById('download-run-zip-btn');

    // --- NEW: Helper function to format seconds into HH:MM:SS ---
    const formatDuration = (totalSeconds) => {
        if (totalSeconds === null || isNaN(totalSeconds) || totalSeconds < 0) {
            return 'N/A';
        }
        const hours = Math.floor(totalSeconds / 3600).toString().padStart(2, '0');
        const minutes = Math.floor((totalSeconds % 3600) / 60).toString().padStart(2, '0');
        const seconds = Math.floor(totalSeconds % 60).toString().padStart(2, '0');
        return `${hours}:${minutes}:${seconds}`;
    };
    
    const getStatusBadge = (status) => {
        const C = {
            "Running": "bg-primary",
            "Completed": "bg-success",
            "Failed": "bg-danger",
            "Aborted by User": "bg-warning text-dark"
        };
        return `<span class="badge ${C[status] || 'bg-secondary'}">${status}</span>`;
    };

    // --- MODIFIED: The render function now populates the new columns ---
    const renderHistory = (runs) => {
        if (!runs || runs.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="8" class="text-center">No run history found for the selected filters.</td></tr>`;
            return;
        }

        tableBody.innerHTML = runs.map(run => {
            // Safely get target count from the snapshot
            const targetCount = run.object_profile_snapshot?.target_count || 0;
            const targetDisplay = targetCount > 0 ? targetCount : '∞';
            
            const localStartTime = new Date(run.start_timestamp + 'Z').toLocaleString();
            
            return `
                <tr>
                    <td>${localStartTime}</td>
                    <td>${getStatusBadge(run.status)}</td>
                    <td>${formatDuration(run.duration_seconds)}</td>
                    <td>${run.batch_code}</td>
                    <td>${run.product?.name || '<i class="text-muted">N/A</i>'}</td>
                    <td>${run.operator?.name || '<i class="text-muted">N/A</i>'}</td>
                    <td class="text-end fw-bold">${run.detected_items_count} / ${targetDisplay}</td>
                    <td class="text-end">
                        <button class="btn btn-sm btn-outline-info view-detections-btn" data-run-id="${run.id}" data-batch-code="${run.batch_code}">
                            <i class="bi bi-images"></i> View Images
                        </button>
                    </td>
                </tr>
            `;
        }).join('');
    };

    // ... (no changes to the rest of the file) ...

    const fetchHistory = async () => {
        const params = new URLSearchParams();
        const startDate = document.getElementById('filter-start-date').value;
        const endDate = document.getElementById('filter-end-date').value;

        if (startDate) params.append('start_date', new Date(startDate).toISOString());
        if (endDate) params.append('end_date', new Date(endDate).toISOString());
        if (productFilter.value) params.append('product_id', productFilter.value);
        if (operatorFilter.value) params.append('operator_id', operatorFilter.value);
        if (document.getElementById('filter-batch-code').value) {
            params.append('batch_code', document.getElementById('filter-batch-code').value);
        }

        tableBody.innerHTML = `<tr><td colspan="8" class="text-center">Loading...</td></tr>`;
        try {
            const response = await fetch(`/api/v1/run-history/?${params.toString()}`);
            const runs = await response.json();
            renderHistory(runs);
        } catch (error) {
            console.error("Failed to fetch run history:", error);
            tableBody.innerHTML = `<tr><td colspan="8" class="text-center text-danger">Failed to load data.</td></tr>`;
        }
    };

    const populateFilters = async () => {
        try {
            const [products, operators] = await Promise.all([
                fetch('/api/v1/products/').then(res => res.json()),
                fetch('/api/v1/operators/').then(res => res.json())
            ]);
            productFilter.innerHTML = '<option value="">All Products</option>' + products.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
            operatorFilter.innerHTML = '<option value="">All Operators</option>' + operators.map(o => `<option value="${o.id}">${o.name}</option>`).join('');
        } catch (error) {
            console.error("Failed to populate filters:", error);
        }
    };
    
    const viewDetections = async (runId, batchCode) => {
        modalTitle.textContent = `Detections for Run #${runId} (${batchCode})`;
        modalBody.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"></div><p>Loading images...</p></div>';
        downloadZipBtn.href = `/api/v1/run-history/${runId}/download-images`;
        modal.show();

        try {
            const response = await fetch(`/api/v1/run-history/${runId}/detections`);
            const detections = await response.json();
            if(detections.length === 0) {
                modalBody.innerHTML = '<p class="text-center text-muted">No images were captured for this run.</p>';
                return;
            }

            modalBody.innerHTML = `<div class="row g-2">` + detections.map(d => {
                const imgPath = d.image_path ? d.image_path : '/static/images/placeholder.jpg';
                const localTime = new Date(d.timestamp + 'Z').toLocaleTimeString();
                return `
                    <div class="col-md-3 col-sm-6">
                        <div class="card">
                            <a href="${imgPath}" target="_blank">
                                <img src="${imgPath}" class="card-img-top" alt="Detection image" style="aspect-ratio: 4/3; object-fit: cover;">
                            </a>
                            <div class="card-footer text-muted small">${localTime}</div>
                        </div>
                    </div>
                `;
            }).join('') + `</div>`;

        } catch (error) {
            console.error('Failed to load detection images:', error);
            modalBody.innerHTML = '<p class="text-center text-danger">Failed to load images.</p>';
        }
    };

    filterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        fetchHistory();
    });

    resetBtn.addEventListener('click', () => {
        filterForm.reset();
        fetchHistory();
    });

    tableBody.addEventListener('click', (e) => {
        const viewBtn = e.target.closest('.view-detections-btn');
        if (viewBtn) {
            viewDetections(viewBtn.dataset.runId, viewBtn.dataset.batchCode);
        }
    });

    // Initial Load
    populateFilters();
    fetchHistory();
});