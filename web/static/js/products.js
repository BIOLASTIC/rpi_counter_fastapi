// rpi_counter_fastapi-dev2/web/static/js/products.js

document.addEventListener('DOMContentLoaded', function() {
    const addProductBtn = document.getElementById('add-product-btn');
    const productModal = new bootstrap.Modal(document.getElementById('product-modal'));
    const productForm = document.getElementById('product-form');
    const modalTitle = document.getElementById('product-modal-title');
    const tableBody = document.getElementById('products-table-body');
    let editingProductId = null;

    const fetchProducts = async () => {
        try {
            const response = await fetch('/api/v1/products/');
            if (!response.ok) throw new Error('Failed to fetch products');
            const products = await response.json();
            renderTable(products);
        } catch (error) {
            console.error('Error fetching products:', error);
            tableBody.innerHTML = '<tr><td colspan="8" class="text-center text-danger">Failed to load products.</td></tr>';
        }
    };

    const renderTable = (products) => {
        tableBody.innerHTML = '';
        if (products.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="8" class="text-center">No products found.</td></tr>';
            return;
        }
        products.forEach(p => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${p.name}</td>
                <td>${p.category || ''}</td>
                <td>${p.size || ''}</td>
                <td><span class="badge ${p.status === 'Active' ? 'bg-success' : 'bg-secondary'}">${p.status}</span></td>
                <td>${p.version}</td>
                <td>${p.description || ''}</td>
                <td>${p.min_sensor_block_time_ms || 'N/A'} / ${p.max_sensor_block_time_ms || 'N/A'}</td>
                <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary edit-btn" data-id="${p.id}"><i class="bi bi-pencil-fill"></i></button>
                    <button class="btn btn-sm btn-outline-danger delete-btn" data-id="${p.id}"><i class="bi bi-trash-fill"></i></button>
                </td>
            `;
            tableBody.appendChild(row);
        });
    };

    const openModalForEdit = async (id) => {
        editingProductId = id;
        modalTitle.textContent = 'Edit Product';
        try {
            const response = await fetch(`/api/v1/products/${id}`);
            if (!response.ok) throw new Error('Failed to fetch product details');
            const product = await response.json();
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
            document.getElementById('verify-category').checked = product.verify_category;
            document.getElementById('verify-size').checked = product.verify_size;
            document.getElementById('verify-defects').checked = product.verify_defects;
            document.getElementById('verify-ticks').checked = product.verify_ticks;
            productModal.show();
        } catch (error) {
            console.error('Error preparing edit modal:', error);
            alert('Could not load product data.');
        }
    };

    addProductBtn.addEventListener('click', () => {
        editingProductId = null;
        modalTitle.textContent = 'Add New Product';
        productForm.reset();
        document.getElementById('product-id').value = '';
        productModal.show();
    });

    tableBody.addEventListener('click', (e) => {
        const editBtn = e.target.closest('.edit-btn');
        const deleteBtn = e.target.closest('.delete-btn');
        if (editBtn) {
            openModalForEdit(editBtn.dataset.id);
        } else if (deleteBtn) {
            if (confirm('Are you sure you want to delete this product?')) {
                deleteProduct(deleteBtn.dataset.id);
            }
        }
    });

    productForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const payload = {
            name: document.getElementById('product-name').value,
            version: document.getElementById('product-version').value,
            category: document.getElementById('product-category').value,
            size: document.getElementById('product-size').value,
            description: document.getElementById('product-description').value,
            status: document.getElementById('product-status').value,
            ai_model_path: document.getElementById('product-ai-model').value,
            min_sensor_block_time_ms: document.getElementById('product-min-block-time').value || null,
            max_sensor_block_time_ms: document.getElementById('product-max-block-time').value || null,
            verify_category: document.getElementById('verify-category').checked,
            verify_size: document.getElementById('verify-size').checked,
            verify_defects: document.getElementById('verify-defects').checked,
            verify_ticks: document.getElementById('verify-ticks').checked
        };

        const url = editingProductId ? `/api/v1/products/${editingProductId}` : '/api/v1/products/';
        const method = editingProductId ? 'PUT' : 'POST';

        try {
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to save product');
            }
            productModal.hide();
            fetchProducts();
        } catch (error) {
            console.error('Error saving product:', error);
            alert(`Error: ${error.message}`);
        }
    });

    const deleteProduct = async (id) => {
        try {
            const response = await fetch(`/api/v1/products/${id}`, { method: 'DELETE' });
            if (!response.ok) {
                 const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to delete product');
            }
            fetchProducts();
        } catch (error) {
            console.error('Error deleting product:', error);
            alert(`Error: ${error.message}`);
        }
    };

    fetchProducts();
});