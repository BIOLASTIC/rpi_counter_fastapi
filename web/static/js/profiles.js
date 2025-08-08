document.addEventListener('DOMContentLoaded', function () {
    const cameraModal = new bootstrap.Modal(document.getElementById('camera-profile-modal'));
    const objectModal = new bootstrap.Modal(document.getElementById('object-profile-modal'));

    // --- Common Functions ---
    async function fetchData(url, errorMessage) {
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(errorMessage);
            return await response.json();
        } catch (error) {
            console.error(`Error fetching data from ${url}:`, error);
            alert(`Error: ${error.message}. Check console for details.`);
            return [];
        }
    }
    
    // --- Camera Profile Logic ---
    const cameraForm = document.getElementById('camera-profile-form');
    const cameraTableBody = document.getElementById('camera-profiles-table-body');
    let currentCameraId = null;

    async function loadCameraProfiles() {
        const profiles = await fetchData('/api/v1/profiles/camera', 'Failed to fetch camera profiles');
        cameraTableBody.innerHTML = '';
        if (profiles.length === 0) {
            cameraTableBody.innerHTML = '<tr><td colspan="4" class="text-center">No camera profiles found.</td></tr>';
        } else {
            profiles.forEach(p => {
                cameraTableBody.innerHTML += `
                    <tr>
                        <td>${p.name}</td>
                        <td>${p.exposure}</td>
                        <td>${p.gain}</td>
                        <td class="text-end">
                            <button class="btn btn-sm btn-outline-primary edit-camera-btn" data-id="${p.id}"><i class="bi bi-pencil"></i></button>
                            <button class="btn btn-sm btn-outline-danger delete-camera-btn" data-id="${p.id}"><i class="bi bi-trash"></i></button>
                        </td>
                    </tr>`;
            });
        }
    }

    document.getElementById('add-camera-profile-btn').addEventListener('click', () => {
        currentCameraId = null;
        document.getElementById('camera-modal-title').textContent = 'Add New Camera Profile';
        cameraForm.reset();
        cameraModal.show();
    });

    cameraForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            name: document.getElementById('camera-profile-name').value,
            exposure: parseInt(document.getElementById('camera-profile-exposure').value),
            gain: parseInt(document.getElementById('camera-profile-gain').value),
            white_balance_temp: parseInt(document.getElementById('camera-profile-wb').value),
            brightness: parseInt(document.getElementById('camera-profile-brightness').value),
            autofocus: document.getElementById('camera-profile-autofocus').checked,
            description: document.getElementById('camera-profile-desc').value,
        };

        const url = currentCameraId ? `/api/v1/profiles/camera/${currentCameraId}` : '/api/v1/profiles/camera';
        const method = currentCameraId ? 'PUT' : 'POST';

        try {
            const response = await fetch(url, { method, headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
            if (!response.ok) { const err = await response.json(); throw new Error(err.detail); }
            cameraModal.hide();
            await loadCameraProfiles();
            await loadObjectProfiles(); // Refresh object profiles in case names changed
        } catch (error) {
            alert(`Error saving camera profile: ${error.message}`);
        }
    });

    cameraTableBody.addEventListener('click', async (e) => {
        const target = e.target.closest('button');
        if (!target) return;
        const id = target.dataset.id;

        if (target.classList.contains('edit-camera-btn')) {
            const profile = await fetchData(`/api/v1/profiles/camera/${id}`, 'Failed to fetch camera profile data.');
            if (!profile) return;
            currentCameraId = id;
            document.getElementById('camera-modal-title').textContent = 'Edit Camera Profile';
            Object.keys(profile).forEach(key => {
                const el = document.getElementById(`camera-profile-${key.replace(/_/g, '-')}`);
                if (el) {
                    if (el.type === 'checkbox') el.checked = profile[key];
                    else el.value = profile[key] ?? '';
                }
            });
            cameraModal.show();
        }

        if (target.classList.contains('delete-camera-btn')) {
            if (confirm('Are you sure you want to delete this camera profile?')) {
                const response = await fetch(`/api/v1/profiles/camera/${id}`, { method: 'DELETE' });
                if (!response.ok) { const err = await response.json(); alert(`Delete failed: ${err.detail}`); }
                else { await loadCameraProfiles(); }
            }
        }
    });

    // --- Object Profile Logic ---
    const objectForm = document.getElementById('object-profile-form');
    const objectTableBody = document.getElementById('object-profiles-table-body');
    const cameraSelect = document.getElementById('object-camera-profile-select');
    const productSelect = document.getElementById('object-product-select'); // PHASE 2: Get product select element
    let currentObjectId = null;

    // PHASE 2: Function to populate select dropdowns
    async function populateSelect(element, url, nameField, valueField, prompt) {
        const items = await fetchData(url, `Failed to fetch ${prompt}`);
        element.innerHTML = `<option value="">-- Select ${prompt} --</option>`;
        items.forEach(item => {
            element.innerHTML += `<option value="${item[valueField]}">${item[nameField]}</option>`;
        });
    }

    async function loadObjectProfiles() {
        const profiles = await fetchData('/api/v1/profiles/object', 'Failed to fetch object profiles');
        objectTableBody.innerHTML = '';
        if (profiles.length === 0) {
            objectTableBody.innerHTML = '<tr><td colspan="4" class="text-center">No object profiles (recipes) found.</td></tr>';
        } else {
            profiles.forEach(p => {
                // PHASE 2: Display product name, or 'N/A' if not linked
                const productName = p.product ? p.product.name : '<span class="text-danger">Not Linked</span>';
                objectTableBody.innerHTML += `
                    <tr>
                        <td>${p.name}</td>
                        <td>${productName}</td>
                        <td>${p.camera_profile.name}</td>
                        <td class="text-end">
                            <button class="btn btn-sm btn-outline-primary edit-object-btn" data-id="${p.id}"><i class="bi bi-pencil"></i></button>
                            <button class="btn btn-sm btn-outline-danger delete-object-btn" data-id="${p.id}"><i class="bi bi-trash"></i></button>
                        </td>
                    </tr>`;
            });
        }
    }

    document.getElementById('add-object-profile-btn').addEventListener('click', async () => {
        currentObjectId = null;
        document.getElementById('object-modal-title').textContent = 'Add New Object Profile (Recipe)';
        objectForm.reset();
        // PHASE 2: Populate dropdowns for new entry
        await populateSelect(cameraSelect, '/api/v1/profiles/camera', 'name', 'id', 'Camera Profile');
        await populateSelect(productSelect, '/api/v1/products', 'name', 'id', 'Product');
        objectModal.show();
    });

    objectForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            name: document.getElementById('object-profile-name').value,
            camera_profile_id: parseInt(cameraSelect.value),
            sort_offset_ms: parseInt(document.getElementById('object-sort-offset').value),
            description: document.getElementById('object-profile-desc').value,
            product_id: parseInt(productSelect.value) || null, // PHASE 2: Get product_id
        };

        const url = currentObjectId ? `/api/v1/profiles/object/${currentObjectId}` : '/api/v1/profiles/object';
        const method = currentObjectId ? 'PUT' : 'POST';

        try {
            const response = await fetch(url, { method, headers: {'Content-Type': 'application/json'}, body: JSON.stringify(data) });
            if (!response.ok) { const err = await response.json(); throw new Error(err.detail); }
            objectModal.hide();
            await loadObjectProfiles();
        } catch (error) {
            alert(`Error saving object profile: ${error.message}`);
        }
    });

    objectTableBody.addEventListener('click', async (e) => {
        const target = e.target.closest('button');
        if (!target) return;
        const id = target.dataset.id;

        if (target.classList.contains('edit-object-btn')) {
            const profile = await fetchData(`/api/v1/profiles/object/${id}`, 'Failed to fetch object profile data.');
            if (!profile) return;
            currentObjectId = id;
            
            // PHASE 2: Populate dropdowns before showing modal
            await populateSelect(cameraSelect, '/api/v1/profiles/camera', 'name', 'id', 'Camera Profile');
            await populateSelect(productSelect, '/api/v1/products', 'name', 'id', 'Product');

            document.getElementById('object-modal-title').textContent = 'Edit Object Profile (Recipe)';
            document.getElementById('object-profile-name').value = profile.name;
            document.getElementById('object-sort-offset').value = profile.sort_offset_ms;
            document.getElementById('object-profile-desc').value = profile.description || '';
            cameraSelect.value = profile.camera_profile_id;
            productSelect.value = profile.product_id || ''; // PHASE 2: Set selected product
            
            objectModal.show();
        }

        if (target.classList.contains('delete-object-btn')) {
            if (confirm('Are you sure you want to delete this object profile?')) {
                const response = await fetch(`/api/v1/profiles/object/${id}`, { method: 'DELETE' });
                if (!response.ok) { const err = await response.json(); alert(`Delete failed: ${err.detail}`); }
                else { await loadObjectProfiles(); }
            }
        }
    });

    // --- Initial Load ---
    loadCameraProfiles();
    loadObjectProfiles();
});