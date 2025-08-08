document.addEventListener('DOMContentLoaded', function () {
    const tableBody = document.getElementById('history-table-body');
    const filterForm = document.getElementById('filter-form');
    const resetBtn = document.getElementById('reset-filter-btn');
    const productSelect = document.getElementById('filter-product');
    const operatorSelect = document.getElementById('filter-operator');

    async function populateSelect(element, url, nameField, prompt) {
        try {
            const response = await fetch(url);
            const items = await response.json();
            element.innerHTML = `<option value="">All ${prompt}s</option>`;
            items.forEach(item => {
                element.innerHTML += `<option value="${item.id}">${item[nameField]}</option>`;
            });
        } catch (error) {
            console.error(`Failed to load ${prompt}s:`, error);
        }
    }

    async function loadHistory(params = {}) {
        tableBody.innerHTML = '<tr><td colspan="7" class="text-center">Loading...</td></tr>';
        const query = new URLSearchParams(params).toString();
        
        try {
            const response = await fetch(`/api/v1/run-history?${query}`);
            if (!response.ok) throw new Error('Failed to fetch run history');
            const logs = await response.json();

            tableBody.innerHTML = '';
            if (logs.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="7" class="text-center">No run logs found for the selected criteria.</td></tr>';
                return;
            }

            logs.forEach(log => {
                const statusColors = {
                    'Completed': 'bg-success',
                    'Running': 'bg-info text-dark',
                    'Failed': 'bg-danger',
                    'Aborted by User': 'bg-warning text-dark'
                };
                const statusBadge = statusColors[log.status] || 'bg-secondary';
                const snapshot = log.object_profile_snapshot ? JSON.stringify(log.object_profile_snapshot, null, 2) : 'N/A';

                const row = `
                    <tr>
                        <td>${new Date(log.start_timestamp).toLocaleString()}</td>
                        <td>${log.end_timestamp ? new Date(log.end_timestamp).toLocaleString() : 'N/A'}</td>
                        <td><span class="badge ${statusBadge}">${log.status}</span></td>
                        <td>${log.batch_code}</td>
                        <td>${log.product ? log.product.name : 'N/A'}</td>
                        <td>${log.operator ? log.operator.name : 'N/A'}</td>
                        <td><pre class="mb-0"><code>${snapshot}</code></pre></td>
                    </tr>`;
                tableBody.innerHTML += row;
            });
        } catch (error) {
            console.error('Error loading history:', error);
            tableBody.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Error loading run history.</td></tr>`;
        }
    }

    filterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const params = {
            start_date: document.getElementById('filter-start-date').value ? new Date(document.getElementById('filter-start-date').value).toISOString() : '',
            end_date: document.getElementById('filter-end-date').value ? new Date(document.getElementById('filter-end-date').value).toISOString() : '',
            product_id: productSelect.value,
            operator_id: operatorSelect.value
        };
        const cleanedParams = Object.fromEntries(Object.entries(params).filter(([_, v]) => v));
        loadHistory(cleanedParams);
    });

    resetBtn.addEventListener('click', () => {
        filterForm.reset();
        loadHistory();
    });

    // Initial Load
    populateSelect(productSelect, '/api/v1/products', 'name', 'Product');
    populateSelect(operatorSelect, '/api/v1/operators', 'name', 'Operator');
    loadHistory();
});