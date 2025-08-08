document.addEventListener('DOMContentLoaded', function () {
    const addProductBtn = document.getElementById('add-product-btn');
    const productModal = new bootstrap.Modal(document.getElementById('product-modal'));
    const productForm = document.getElementById('product-form');
    const modalTitle = document.getElementById('product-modal-title');
    const tableBody = document.getElementById('products-table-body');
    let currentProductId = null;

    // Fetch and display all products
    async function loadProducts() {
        try {
            const response = await fetch('/api/v1/products');
            if (!response.ok) throw new Error('Failed to fetch products');
            const products = await response.json();

            tableBody.innerHTML = '';
            if (products.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="6" class="text-center">No products found.</td></tr>';
                return;
            }

            products.forEach(product => {
                const statusBadge = product.status === 'Active' ? 'bg-success' : 'bg-secondary';
                const row = `
                    <tr>
                        <td>${product.name}</td>
                        <td><span class="badge ${statusBadge}">${product.status}</span></td>
                        <td>${product.version}</td>
                        <td>${product.description || ''}</td>
                        <td>${product.min_sensor_block_time_ms || 'N/A'} / ${product.max_sensor_block_time_ms || 'N/A'}</td>
                        <td class="text-end">
                            <button class="btn btn-sm btn-outline-primary edit-btn" data-id="${product.id}"><i class="bi bi-pencil"></i></button>
                            <button class="btn btn-sm btn-outline-danger delete-btn" data-id="${product.id}"><i class="bi bi-trash"></i></button>
                        </td>
                    </tr>
                `;
                tableBody.insertAdjacentHTML('beforeend', row);
            });
        } catch (error) {
            console.error('Error loading products:', error);
            tableBody.innerHTML = '<tr><td colspan="6" class="text-center text-danger">Error loading products.</td></tr>';
        }
    }

    // Show modal for creating
    addProductBtn.addEventListener('click', () => {
        currentProductId = null;
        modalTitle.textContent = 'Add New Product';
        productForm.reset();
        document.getElementById('product-id').value = '';
        productModal.show();
    });

    // Handle form submission (Create or Update)
    productForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const productData = {
            name: document.getElementById('product-name').value,
            description: document.getElementById('product-description').value,
            version: document.getElementById('product-version').value,
            status: document.getElementById('product-status').value,
            ai_model_path: document.getElementById('product-ai-model').value,
            min_sensor_block_time_ms: document.getElementById('product-min-block-time').value ? parseInt(document.getElementById('product-min-block-time').value) : null,
            max_sensor_block_time_ms: document.getElementById('product-max-block-time').value ? parseInt(document.getElementById('product-max-block-time').value) : null,
        };

        const url = currentProductId ? `/api/v1/products/${currentProductId}` : '/api/v1/products';
        const method = currentProductId ? 'PUT' : 'POST';

        try {
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(productData),
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to save product');
            }
            productModal.hide();
            await loadProducts();
        } catch (error) {
            alert(`Error saving product: ${error.message}`);
        }
    });
    
    // Handle Edit and Delete buttons
    tableBody.addEventListener('click', async (e) => {
        const target = e.target.closest('button');
        if (!target) return;

        const productId = target.dataset.id;
        
        // Edit button
        if (target.classList.contains('edit-btn')) {
            try {
                const response = await fetch(`/api/v1/products/${productId}`);
                 if (!response.ok) throw new Error('Failed to fetch product details');
                const product = await response.json();
                
                currentProductId = product.id;
                modalTitle.textContent = 'Edit Product';
                document.getElementById('product-id').value = product.id;
                document.getElementById('product-name').value = product.name;
                document.getElementById('product-description').value = product.description || '';
                document.getElementById('product-version').value = product.version;
                document.getElementById('product-status').value = product.status;
                document.getElementById('product-ai-model').value = product.ai_model_path || '';
                document.getElementById('product-min-block-time').value = product.min_sensor_block_time_ms || '';
                document.getElementById('product-max-block-time').value = product.max_sensor_block_time_ms || '';

                productModal.show();
            } catch (error) {
                 alert(`Error: ${error.message}`);
            }
        }

        // Delete button
        if (target.classList.contains('delete-btn')) {
            if (confirm('Are you sure you want to delete this product?')) {
                try {
                    const response = await fetch(`/api/v1/products/${productId}`, { method: 'DELETE' });
                    if (!response.ok) {
                         const errorData = await response.json();
                         throw new Error(errorData.detail || 'Failed to delete product');
                    }
                    await loadProducts();
                } catch (error) {
                    alert(`Error deleting product: ${error.message}`);
                }
            }
        }
    });

    // Initial load
    loadProducts();
});