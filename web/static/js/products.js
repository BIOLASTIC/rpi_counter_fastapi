// rpi_counter_fastapi-apintrigation/web/static/js/products.js

document.addEventListener('DOMContentLoaded', function() {
    const addProductBtn = document.getElementById('add-product-btn');
    const productModal = new bootstrap.Modal(document.getElementById('product-modal'));
    const productForm = document.getElementById('product-form');
    const productModalTitle = document.getElementById('product-modal-title');
    const productsTableBody = document.getElementById('products-table-body');
    
    let currentProductId = null;

    async function fetchProducts() {
        try {
            const response = await fetch('/api/v1/products/');
            if (!response.ok) throw new Error('Failed to fetch products');
            const products = await response.json();
            renderProducts(products);
        } catch (error) {
            console.error('Error fetching products:', error);
            productsTableBody.innerHTML = '<tr><td colspan="8" class="text-center text-danger">Failed to load products.</td></tr>';
        }
    }

    function renderProducts(products) {
        productsTableBody.innerHTML = '';
        if (products.length === 0) {
            productsTableBody.innerHTML = '<tr><td colspan="8" class="text-center">No products found.</td></tr>';
            return;
        }

        products.forEach(product => {
            const row = `
                <tr>
                    <td>${product.name}</td>
                    <td>${product.category || ''}</td>
                    <td>${product.size || ''}</td>
                    <td><span class="badge ${product.status === 'Active' ? 'bg-success' : 'bg-secondary'}">${product.status}</span></td>
                    <td>${product.version}</td>
                    <td>${product.description || ''}</td>
                    <td>${product.min_sensor_block_time_ms || 'N/A'} / ${product.max_sensor_block_time_ms || 'N/A'}</td>
                    <td class="text-end">
                        <button class="btn btn-sm btn-outline-secondary edit-btn" data-id="${product.id}"><i class="bi bi-pencil"></i></button>
                        <button class="btn btn-sm btn-outline-danger delete-btn" data-id="${product.id}"><i class="bi bi-trash"></i></button>
                    </td>
                </tr>
            `;
            productsTableBody.insertAdjacentHTML('beforeend', row);
        });
    }

    function openModalForEdit(product) {
        currentProductId = product.id;
        productModalTitle.textContent = 'Edit Product';
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
        // --- NEW: Populate geometric validation fields ---
        document.getElementById('product-target-angle').value = product.target_angle || '';
        document.getElementById('product-angle-tolerance').value = product.angle_tolerance || '';
        document.getElementById('product-min-aspect-ratio').value = product.min_aspect_ratio || '';
        document.getElementById('product-max-aspect-ratio').value = product.max_aspect_ratio || '';
        productModal.show();
    }

    addProductBtn.addEventListener('click', () => {
        currentProductId = null;
        productModalTitle.textContent = 'Add New Product';
        productForm.reset();
        productModal.show();
    });

    productsTableBody.addEventListener('click', async function(e) {
        const editBtn = e.target.closest('.edit-btn');
        const deleteBtn = e.target.closest('.delete-btn');

        if (editBtn) {
            const id = editBtn.dataset.id;
            try {
                const response = await fetch(`/api/v1/products/${id}`);
                if (!response.ok) throw new Error('Failed to fetch product details');
                const product = await response.json();
                openModalForEdit(product);
            } catch (error) {
                console.error('Error fetching product for edit:', error);
            }
        }

        if (deleteBtn) {
            const id = deleteBtn.dataset.id;
            if (confirm('Are you sure you want to delete this product? This action cannot be undone.')) {
                try {
                    const response = await fetch(`/api/v1/products/${id}`, { method: 'DELETE' });
                    if (!response.ok) {
                         const errorData = await response.json();
                         throw new Error(errorData.detail || 'Failed to delete product');
                    }
                    fetchProducts();
                } catch (error) {
                    alert(`Error: ${error.message}`);
                }
            }
        }
    });

    productForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const getFloatOrNull = (id) => {
            const val = document.getElementById(id).value;
            return val ? parseFloat(val) : null;
        };
        
        const getIntOrNull = (id) => {
            const val = document.getElementById(id).value;
            return val ? parseInt(val, 10) : null;
        };

        const productData = {
            name: document.getElementById('product-name').value,
            version: document.getElementById('product-version').value,
            category: document.getElementById('product-category').value,
            size: document.getElementById('product-size').value,
            description: document.getElementById('product-description').value,
            status: document.getElementById('product-status').value,
            ai_model_path: document.getElementById('product-ai-model').value,
            min_sensor_block_time_ms: getIntOrNull('product-min-block-time'),
            max_sensor_block_time_ms: getIntOrNull('product-max-block-time'),
            verify_category: document.getElementById('verify-category').checked,
            verify_size: document.getElementById('verify-size').checked,
            verify_defects: document.getElementById('verify-defects').checked,
            verify_ticks: document.getElementById('verify-ticks').checked,
            // --- NEW: Read geometric validation fields ---
            target_angle: getFloatOrNull('product-target-angle'),
            angle_tolerance: getFloatOrNull('product-angle-tolerance'),
            min_aspect_ratio: getFloatOrNull('product-min-aspect-ratio'),
            max_aspect_ratio: getFloatOrNull('product-max-aspect-ratio'),
        };

        const url = currentProductId ? `/api/v1/products/${currentProductId}` : '/api/v1/products/';
        const method = currentProductId ? 'PUT' : 'POST';

        try {
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(productData)
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to save product');
            }
            productModal.hide();
            fetchProducts();
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    });

    fetchProducts();
});