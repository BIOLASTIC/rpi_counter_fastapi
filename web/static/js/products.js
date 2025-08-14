// rpi_counter_fastapi-dev2/web/static/js/products.js

// API Helper
const api = {
    get: (url) => fetch(`/api/v1${url}`).then(res => res.ok ? res.json() : Promise.reject(res)),
    post: (url, data) => fetch(`/api/v1${url}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }).then(res => res.ok ? res.json() : Promise.reject(res)),
    put: (url, data) => fetch(`/api/v1${url}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }).then(res => res.ok ? res.json() : Promise.reject(res)),
    del: (url) => fetch(`/api/v1${url}`, { method: 'DELETE' }).then(res => res.ok || Promise.reject(res)),
};

document.addEventListener('DOMContentLoaded', () => {
    // --- Elements ---
    const tableBody = document.getElementById('products-table-body');
    const modalEl = document.getElementById('product-modal');
    const productModal = new bootstrap.Modal(modalEl);
    const productForm = document.getElementById('product-form');
    const modalTitle = document.getElementById('product-modal-title');
    const addProductBtn = document.getElementById('add-product-btn');

    // --- State ---
    let products = [];

    // --- Render Function ---
    const renderProducts = () => {
        if (!tableBody) return;
        if (products.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="8" class="text-center">No products found.</td></tr>';
            return;
        }
        tableBody.innerHTML = products.map(p => `
            <tr>
                <td>${p.name}</td>
                <td>${p.category || '<i class="text-muted">N/A</i>'}</td>
                <td>${p.size || '<i class="text-muted">N/A</i>'}</td>
                <td><span class="badge ${p.status === 'Active' ? 'bg-success' : 'bg-secondary'}">${p.status}</span></td>
                <td>${p.version}</td>
                <td>${p.description || ''}</td>
                <td>${p.min_sensor_block_time_ms || ''} / ${p.max_sensor_block_time_ms || ''}</td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary edit-btn" data-id="${p.id}"><i class="bi bi-pencil"></i></button>
                    <button class="btn btn-sm btn-outline-danger delete-btn" data-id="${p.id}"><i class="bi bi-trash"></i></button>
                </td>
            </tr>
        `).join('');
    };

    // --- Data Loading ---
    const loadProducts = async () => {
        try {
            products = await api.get('/products/');
            renderProducts();
        } catch (error) {
            console.error('Failed to load products:', error);
            if (tableBody) tableBody.innerHTML = '<tr><td colspan="8" class="text-center text-danger">Error loading products.</td></tr>';
        }
    };

    // --- Event Handlers ---
    const handleEditClick = (id) => {
        const product = products.find(p => p.id == id);
        if (!product) return;

        modalTitle.textContent = `Edit Product: ${product.name}`;
        productForm.reset();
        document.getElementById('product-id').value = product.id;
        document.getElementById('product-name').value = product.name;
        document.getElementById('product-version').value = product.version;
        document.getElementById('product-category').value = product.category || '';
        document.getElementById('product-size').value = product.size || '';
        document.getElementById('product-description').value = product.description || '';
        document.getElementById('product-status').value = product.status;
        document.getElementById('product-ai-model').value = product.ai_model_path || '';
        document.getElementById('product-min-block-time').value = product.min_sensor_block_time_ms || '';
        document.getElementById('product-max-block-time').value = product.max_sensor_block_time_ms || '';
        productModal.show();
    };

    const handleDeleteClick = async (id) => {
        if (!confirm('Are you sure you want to delete this product? It cannot be undone.')) return;

        try {
            await api.del(`/products/${id}`);
            loadProducts();
        } catch (error) {
            const errData = await error.json().catch(() => ({ detail: 'Could not delete product. It may be in use by an Object Profile.' }));
            alert(`Error: ${errData.detail}`);
        }
    };

    addProductBtn.addEventListener('click', () => {
        modalTitle.textContent = 'Add New Product';
        productForm.reset();
        document.getElementById('product-id').value = '';
        productModal.show();
    });

    tableBody.addEventListener('click', e => {
        const editBtn = e.target.closest('.edit-btn');
        const deleteBtn = e.target.closest('.delete-btn');
        if (editBtn) handleEditClick(editBtn.dataset.id);
        if (deleteBtn) handleDeleteClick(deleteBtn.dataset.id);
    });

    productForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('product-id').value;
        const data = {
            name: document.getElementById('product-name').value,
            version: document.getElementById('product-version').value,
            category: document.getElementById('product-category').value || null,
            size: document.getElementById('product-size').value || null,
            description: document.getElementById('product-description').value || null,
            status: document.getElementById('product-status').value,
            ai_model_path: document.getElementById('product-ai-model').value || null,
            min_sensor_block_time_ms: document.getElementById('product-min-block-time').value ? parseInt(document.getElementById('product-min-block-time').value) : null,
            max_sensor_block_time_ms: document.getElementById('product-max-block-time').value ? parseInt(document.getElementById('product-max-block-time').value) : null,
        };

        try {
            const promise = id ? api.put(`/products/${id}`, data) : api.post('/products/', data);
            await promise;
            productModal.hide();
            loadProducts();
        } catch (error) {
            const errData = await error.json().catch(() => ({ detail: 'An unknown error occurred.' }));
            alert(`Error: ${errData.detail}`);
        }
    });

    // --- Initial Load ---
    loadProducts();
});