// rpi_counter_fastapi-dev2/web/static/js/profiles.js

// --- API Helper ---
const api = {
    get: (url) => fetch(`/api/v1${url}`).then(res => res.ok ? res.json() : Promise.reject(res)),
    post: (url, data) => fetch(`/api/v1${url}`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }).then(res => res.ok ? res.json() : Promise.reject(res)),
    put: (url, data) => fetch(`/api/v1${url}`, { method: 'PUT', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) }).then(res => res.ok ? res.json() : Promise.reject(res)),
    del: (url) => fetch(`/api/v1${url}`, { method: 'DELETE' }).then(res => res.ok ? res : Promise.reject(res)),
};

document.addEventListener('DOMContentLoaded', () => {

    // --- Element Selectors ---
    const cameraTableBody = document.getElementById('camera-profiles-table-body');
    const objectTableBody = document.getElementById('object-profiles-table-body');
    const cameraProfileModalEl = document.getElementById('camera-profile-modal');
    const cameraProfileModal = new bootstrap.Modal(cameraProfileModalEl);
    const cameraForm = document.getElementById('camera-profile-form');
    const objectProfileModal = new bootstrap.Modal(document.getElementById('object-profile-modal'));
    const objectForm = document.getElementById('object-profile-form');
    
    const previewSelect = document.getElementById('camera-preview-select');
    const previewImage = document.getElementById('camera-preview-feed');
    const liveUpdateInputs = document.querySelectorAll('#camera-profile-form .live-update');

    // --- State ---
    let cameraProfiles = [];
    let objectProfiles = [];
    let products = [];

    // --- Debounce Function ---
    function debounce(func, delay) {
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), delay);
        };
    }

    const sendPreviewSettings = async () => {
        const cameraId = previewSelect.value;
        if (!cameraId) return;

        const settings = {
            exposure: parseInt(document.getElementById('camera-profile-exposure').value, 10),
            gain: parseInt(document.getElementById('camera-profile-gain').value, 10),
            brightness: parseInt(document.getElementById('camera-profile-brightness').value, 10),
            white_balance_temp: parseInt(document.getElementById('camera-profile-white-balance-temp').value, 10),
            autofocus: document.getElementById('camera-profile-autofocus').checked,
        };
        
        const payload = Object.fromEntries(Object.entries(settings).filter(([_, v]) => !isNaN(v)));
        
        try {
            await api.post(`/camera/preview_settings/${cameraId}`, payload);
        } catch (error) {
            console.error('Failed to send preview settings:', error);
        }
    };
    const debouncedSendPreviewSettings = debounce(sendPreviewSettings, 300);

    // --- Render Functions ---
    const renderCameraProfiles = () => {
        cameraTableBody.innerHTML = cameraProfiles.map(p => `
            <tr>
                <td>${p.name}</td>
                <td>${p.exposure}</td>
                <td>${p.gain}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary edit-camera-btn" data-id="${p.id}"><i class="bi bi-pencil"></i></button>
                    <button class="btn btn-sm btn-outline-danger delete-camera-btn" data-id="${p.id}"><i class="bi bi-trash"></i></button>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="4" class="text-center">No camera profiles found.</td></tr>';
    };

    const renderObjectProfiles = () => {
        objectTableBody.innerHTML = objectProfiles.map(p => `
            <tr>
                <td>${p.name}</td>
                <td>${p.product?.name || '<i class="text-muted">None</i>'}</td>
                <td>${p.camera_profile.name}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary edit-object-btn" data-id="${p.id}"><i class="bi bi-pencil"></i></button>
                    <button class="btn btn-sm btn-outline-danger delete-object-btn" data-id="${p.id}"><i class="bi bi-trash"></i></button>
                </td>
            </tr>
        `).join('') || '<tr><td colspan="4" class="text-center">No object profiles found.</td></tr>';
    };

    // --- Data Loading ---
    const loadAllData = async () => {
        try {
            [cameraProfiles, objectProfiles, products] = await Promise.all([
                api.get('/profiles/camera'),
                api.get('/profiles/object'),
                api.get('/products/')
            ]);
            renderCameraProfiles();
            renderObjectProfiles();
        } catch (error) {
            console.error("Failed to load profile data:", error);
            cameraTableBody.innerHTML = '<tr><td colspan="4" class="text-center text-danger">Error loading data.</td></tr>';
            objectTableBody.innerHTML = '<tr><td colspan="4" class="text-center text-danger">Error loading data.</td></tr>';
        }
    };

    // --- Camera Profile Handlers ---
    document.getElementById('add-camera-profile-btn').addEventListener('click', () => {
        document.getElementById('camera-modal-title').textContent = 'Add New Camera Profile';
        cameraForm.reset();
        document.getElementById('camera-profile-id').value = '';
        cameraProfileModal.show();
    });

    cameraTableBody.addEventListener('click', e => {
        const editBtn = e.target.closest('.edit-camera-btn');
        const deleteBtn = e.target.closest('.delete-camera-btn');
        
        if (editBtn) {
            const profile = cameraProfiles.find(p => p.id == editBtn.dataset.id);
            if (!profile) return;
            document.getElementById('camera-modal-title').textContent = 'Edit Camera Profile';
            cameraForm.reset();
            Object.keys(profile).forEach(key => {
                // This logic now correctly finds the 'white-balance-temp' input
                const input = document.getElementById(`camera-profile-${key.replace(/_/g, '-')}`);
                if (input) {
                    if (input.type === 'checkbox') input.checked = profile[key];
                    else input.value = profile[key];
                }
            });
            cameraProfileModal.show();
        }

        if (deleteBtn) {
            if (!confirm('Are you sure you want to delete this camera profile?')) return;
            api.del(`/profiles/camera/${deleteBtn.dataset.id}`).then(loadAllData).catch(err => alert(`Error: ${err.detail || 'Could not delete profile.'}`));
        }
    });

    cameraForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('camera-profile-id').value;
        const data = {
            name: document.getElementById('camera-profile-name').value,
            exposure: parseInt(document.getElementById('camera-profile-exposure').value),
            gain: parseInt(document.getElementById('camera-profile-gain').value),
            // --- THIS IS THE FIX ---
            // It now reads from the corrected ID 'camera-profile-white-balance-temp'
            white_balance_temp: parseInt(document.getElementById('camera-profile-white-balance-temp').value),
            // --- END OF FIX ---
            brightness: parseInt(document.getElementById('camera-profile-brightness').value),
            autofocus: document.getElementById('camera-profile-autofocus').checked,
            description: document.getElementById('camera-profile-desc').value,
        };
        const promise = id ? api.put(`/profiles/camera/${id}`, data) : api.post('/profiles/camera', data);
        try {
            await promise;
            cameraProfileModal.hide();
            loadAllData();
        } catch (error) {
            const errData = await error.json();
            alert(`Error: ${errData.detail || 'Failed to save profile'}`);
        }
    });
    
    // --- Object Profile Handlers (Unchanged) ---
    const populateObjectModalDropdowns = () => {
        const camSelect = document.getElementById('object-camera-profile-select');
        const prodSelect = document.getElementById('object-product-select');
        camSelect.innerHTML = cameraProfiles.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
        prodSelect.innerHTML = products.map(p => `<option value="${p.id}">${p.name}</option>`).join('');
    };

    document.getElementById('add-object-profile-btn').addEventListener('click', () => {
        document.getElementById('object-modal-title').textContent = 'Add New Object Profile (Recipe)';
        objectForm.reset();
        document.getElementById('object-profile-id').value = '';
        populateObjectModalDropdowns();
        objectProfileModal.show();
    });
    
    objectTableBody.addEventListener('click', e => {
        const editBtn = e.target.closest('.edit-object-btn');
        const deleteBtn = e.target.closest('.delete-object-btn');

        if (editBtn) {
            const profile = objectProfiles.find(p => p.id == editBtn.dataset.id);
            if (!profile) return;
            document.getElementById('object-modal-title').textContent = 'Edit Object Profile (Recipe)';
            objectForm.reset();
            populateObjectModalDropdowns();
            document.getElementById('object-profile-id').value = profile.id;
            document.getElementById('object-profile-name').value = profile.name;
            document.getElementById('object-camera-profile-select').value = profile.camera_profile_id;
            document.getElementById('object-product-select').value = profile.product_id;
            document.getElementById('object-sort-offset').value = profile.sort_offset_ms;
            document.getElementById('object-profile-desc').value = profile.description || '';
            objectProfileModal.show();
        }

        if (deleteBtn) {
            if (!confirm('Are you sure you want to delete this object profile?')) return;
            api.del(`/profiles/object/${deleteBtn.dataset.id}`).then(loadAllData).catch(err => alert(`Error: ${err.detail || 'Could not delete profile.'}`));
        }
    });

    objectForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('object-profile-id').value;
        const data = {
            name: document.getElementById('object-profile-name').value,
            camera_profile_id: parseInt(document.getElementById('object-camera-profile-select').value),
            product_id: parseInt(document.getElementById('object-product-select').value),
            sort_offset_ms: parseInt(document.getElementById('object-sort-offset').value),
            description: document.getElementById('object-profile-desc').value,
        };
        const promise = id ? api.put(`/profiles/object/${id}`, data) : api.post('/profiles/object', data);
        try {
            await promise;
            objectProfileModal.hide();
            loadAllData();
        } catch (error) {
            const errData = await error.json();
            alert(`Error: ${errData.detail || 'Failed to save recipe'}`);
        }
    });

    // --- Live Preview Logic (Uncha

    // --- NEW: Live Preview Logic ---
    const updatePreviewImageSource = () => {
        const cameraId = previewSelect.value;
        if (cameraId) {
            previewImage.src = `/api/v1/camera/stream/${cameraId}?t=${new Date().getTime()}`;
        } else {
            previewImage.src = '/static/images/placeholder.jpg';
        }
    };

    liveUpdateInputs.forEach(input => input.addEventListener('input', debouncedSendPreviewSettings));
    previewSelect.addEventListener('change', () => {
        updatePreviewImageSource();
        sendPreviewSettings(); // Send immediately on camera change
    });
    
    cameraProfileModalEl.addEventListener('shown.bs.modal', () => {
        updatePreviewImageSource();
        sendPreviewSettings();
    });

    cameraProfileModalEl.addEventListener('hidden.bs.modal', () => {
        previewImage.src = '/static/images/placeholder.jpg';
        // Optionally, could send a command to reset camera to default auto settings
    });

    // --- Initial Load ---
    loadAllData();
});