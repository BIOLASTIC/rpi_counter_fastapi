document.addEventListener("DOMContentLoaded", function () {
    const historyTableBody = document.getElementById("history-table-body");
    const filterForm = document.getElementById("filter-form");
    const resetFilterBtn = document.getElementById("reset-filter-btn");
    const productFilter = document.getElementById("filter-product");
    const operatorFilter = document.getElementById("filter-operator");
    const batchCodeFilter = document.getElementById("filter-batch-code");

    // Modal elements
    const detectionsModal = new bootstrap.Modal(document.getElementById('detections-modal'));
    const detectionsModalTitle = document.getElementById('detections-modal-title');
    const detectionsModalSubtitle = document.getElementById('detections-modal-subtitle');
    const detectionsModalBody = document.getElementById('detections-modal-body-content');
    const downloadZipBtn = document.getElementById('download-run-zip-btn');

    const API_BASE = "/api/v1";

    async function fetchAndPopulateFilters() {
        try {
            const [productsRes, operatorsRes] = await Promise.all([
                fetch(`${API_BASE}/products/`),
                fetch(`${API_BASE}/operators/`)
            ]);
            const products = await productsRes.json();
            const operators = await operatorsRes.json();

            productFilter.innerHTML = '<option value="">All Products</option>' + products.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
            operatorFilter.innerHTML = '<option value="">All Operators</option>' + operators.map(o => `<option value="${o.id}">${o.name}</option>`).join('');
        } catch (error) {
            console.error("Failed to populate filters:", error);
        }
    }

    async function fetchRunHistory(params = {}) {
        historyTableBody.innerHTML = `<tr><td colspan="7" class="text-center">Loading...</td></tr>`;
        const urlParams = new URLSearchParams(params);
        try {
            const response = await fetch(`${API_BASE}/run-history/?${urlParams}`);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const runs = await response.json();
            renderTable(runs);
        } catch (error) {
            console.error("Failed to fetch run history:", error);
            historyTableBody.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Failed to load data.</td></tr>`;
        }
    }

    function renderTable(runs) {
        if (!runs || runs.length === 0) {
            historyTableBody.innerHTML = `<tr><td colspan="7" class="text-center">No run history found matching criteria.</td></tr>`;
            return;
        }

        historyTableBody.innerHTML = runs.map(run => `
            <tr id="run-${run.id}">
                <td>${new Date(run.start_timestamp).toLocaleString()}</td>
                <td><span class="badge bg-${getStatusColor(run.status)}">${run.status}</span></td>
                <td>${run.batch_code}</td>
                <td>${run.product ? run.product.name : 'N/A'}</td>
                <td>${run.operator ? run.operator.name : 'N/A'}</td>
                <td><pre class="small p-1 bg-light border rounded">${JSON.stringify(run.object_profile_snapshot, null, 2)}</pre></td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary view-detections-btn" data-run-id="${run.id}" data-batch-code="${run.batch_code}">
                        <i class="bi bi-images"></i> View Images
                    </button>
                </td>
            </tr>
        `).join('');
    }

    function getStatusColor(status) {
        switch (status) {
            case 'Completed': return 'success';
            case 'Running': return 'info';
            case 'Aborted by User': return 'warning';
            case 'Failed': return 'danger';
            default: return 'secondary';
        }
    }

    filterForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const startDate = document.getElementById('filter-start-date').value;
        const endDate = document.getElementById('filter-end-date').value;
        const params = {
            start_date: startDate ? new Date(startDate).toISOString() : '',
            end_date: endDate ? new Date(endDate).toISOString() : '',
            product_id: productFilter.value,
            operator_id: operatorFilter.value,
            batch_code: batchCodeFilter.value,
        };
        const cleanedParams = Object.fromEntries(Object.entries(params).filter(([_, v]) => v != null && v !== ''));
        fetchRunHistory(cleanedParams);
    });

    resetFilterBtn.addEventListener("click", () => {
        filterForm.reset();
        fetchRunHistory();
    });

    historyTableBody.addEventListener('click', async (event) => {
        const target = event.target.closest('.view-detections-btn');
        if (target) {
            const runId = target.dataset.runId;
            const batchCode = target.dataset.batchCode;
            await openDetectionsModal(runId, batchCode);
        }
    });

    async function openDetectionsModal(runId, batchCode) {
        detectionsModalTitle.textContent = `Detection Events for Run: ${batchCode}`;
        detectionsModalBody.innerHTML = `<div class="text-center"><div class="spinner-border" role="status"></div><p>Loading images...</p></div>`;
        downloadZipBtn.href = `${API_BASE}/run-history/${runId}/download-images`;
        detectionsModal.show();

        try {
            const response = await fetch(`${API_BASE}/run-history/${runId}/detections`);
            if (!response.ok) throw new Error(`Failed to fetch detections. Status: ${response.status}`);
            
            const detections = await response.json();
            
            detectionsModalSubtitle.textContent = `${detections.length} image(s) captured during this run.`;

            if (detections.length === 0) {
                detectionsModalBody.innerHTML = `<div class="alert alert-warning">No detection events with images were logged for this run.</div>`;
                downloadZipBtn.classList.add('disabled');
                return;
            }

            downloadZipBtn.classList.remove('disabled');

            let galleryHTML = '<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3">';
            detections.forEach(det => {
                const placeholder = '/static/images/placeholder.jpg';
                galleryHTML += `
                    <div class="col">
                        <div class="card h-100">
                            <a href="${det.image_path || placeholder}" target="_blank">
                                <img src="${det.image_path || placeholder}" class="card-img-top" alt="Detection Image" loading="lazy" style="aspect-ratio: 16/9; object-fit: cover;">
                            </a>
                            <div class="card-footer text-muted small">
                                ${new Date(det.timestamp).toLocaleString()}
                            </div>
                        </div>
                    </div>
                `;
            });
            galleryHTML += '</div>';
            detectionsModalBody.innerHTML = galleryHTML;

        } catch (error) {
            console.error("Error loading detections:", error);
            detectionsModalBody.innerHTML = `<div class="alert alert-danger">Error: Could not load detection images.</div>`;
        }
    }
    
    // Check for a hash in the URL on page load to auto-open a modal
    if(window.location.hash) {
        const runId = window.location.hash.replace('#run-', '');
        // We need the batch code, so we wait for the table to render first
        // This is a bit of a hack, but works for this purpose
        setTimeout(() => {
            const targetButton = document.querySelector(`.view-detections-btn[data-run-id='${runId}']`);
            if (targetButton) {
                openDetectionsModal(runId, targetButton.dataset.batchCode);
            }
        }, 1500); // wait 1.5s for initial data to load
    }


    fetchAndPopulateFilters();
    fetchRunHistory();
});