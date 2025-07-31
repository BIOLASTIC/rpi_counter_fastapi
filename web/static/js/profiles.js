document.addEventListener('DOMContentLoaded', () => {
    const cameraTbody = document.getElementById('camera-profiles-table-body');
    const objectTbody = document.getElementById('object-profiles-table-body');
    const cameraProfileSelect = document.getElementById('object-camera-profile-select');

    const cameraModalEl = document.getElementById('camera-profile-modal');
    const cameraModal = new bootstrap.Modal(cameraModalEl);
    const cameraForm = document.getElementById('camera-profile-form');

    const objectModalEl = document.getElementById('object-profile-modal');
    const objectModal = new bootstrap.Modal(objectModalEl);
    const objectForm = document.getElementById('object-profile-form');

    let cameraProfilesCache = [];

    const fetchAndRender = async () => {
        // Fetch both sets of profiles concurrently
        const [camRes, objRes] = await Promise.all([
            fetch('/api/v1/profiles/camera'),
            fetch('/api/v1/profiles/object')
        ]);

        if (!camRes.ok || !objRes.ok) {
            console.error("Failed to fetch profiles");
            return;
        }

        const cameraProfiles = await camRes.json();
        const objectProfiles = await objRes.json();
        cameraProfilesCache = cameraProfiles;

        // Render Camera Profiles Table
        cameraTbody.innerHTML = cameraProfiles.map(p => `
            <tr>
                <td>${p.name}</td>
                <td>${p.exposure === 0 ? 'Auto' : p.exposure}</td>
                <td>${p.gain === 0 ? 'Auto' : p.gain}</td>
                <td>
                    <button class="btn btn-outline-secondary btn-sm edit-camera-btn" data-id="${p.id}"><i class="bi bi-pencil-fill"></i></button>
                    <button class="btn btn-outline-danger btn-sm delete-camera-btn" data-id="${p.id}"><i class="bi bi-trash-fill"></i></button>
                </td>
            </tr>
        `).join('');

        // Render Object Profiles Table
        objectTbody.innerHTML = objectProfiles.map(p => `
            <tr>
                <td>${p.name}</td>
                <td>${p.camera_profile.name}</td>
                <td>${p.sort_offset_ms}</td>
                <td>
                    <button class="btn btn-outline-secondary btn-sm edit-object-btn" data-id="${p.id}"><i class="bi bi-pencil-fill"></i></button>
                    <button class="btn btn-outline-danger btn-sm delete-object-btn" data-id="${p.id}"><i class="bi bi-trash-fill"></i></button>
                </td>
            </tr>
        `).join('');

        // Populate the dropdown in the object modal
        cameraProfileSelect.innerHTML = cameraProfiles.map(p =>
            `<option value="${p.id}">${p.name}</option>`
        ).join('');
    };

    // --- Event Listeners ---

    document.getElementById('add-camera-profile-btn').addEventListener('click', () => {
        document.getElementById('camera-modal-title').textContent = 'Add New Camera Profile';
        cameraForm.reset();
        document.getElementById('camera-profile-id').value = '';
        cameraModal.show();
    });

    document.getElementById('add-object-profile-btn').addEventListener('click', () => {
        document.getElementById('object-modal-title').textContent = 'Add New Object Recipe';
        objectForm.reset();
        document.getElementById('object-profile-id').value = '';
        objectModal.show();
    });

    cameraTbody.addEventListener('click', async (e) => {
        const editBtn = e.target.closest('.edit-camera-btn');
        const deleteBtn = e.target.closest('.delete-camera-btn');

        if (editBtn) {
            const id = editBtn.dataset.id;
            const res = await fetch(`/api/v1/profiles/camera/${id}`);
            if (!res.ok) return;
            const p = await res.json();

            document.getElementById('camera-modal-title').textContent = 'Edit Camera Profile';
            document.getElementById('camera-profile-id').value = p.id;
            document.getElementById('camera-profile-name').value = p.name;
            document.getElementById('camera-profile-exposure').value = p.exposure;
            document.getElementById('camera-profile-gain').value = p.gain;
            document.getElementById('camera-profile-brightness').value = p.brightness;
            document.getElementById('camera-profile-wb').value = p.white_balance_temp;
            document.getElementById('camera-profile-autofocus').checked = p.autofocus;
            document.getElementById('camera-profile-desc').value = p.description;
            cameraModal.show();
        }

        if (deleteBtn) {
            const id = deleteBtn.dataset.id;
            if (confirm('Are you sure you want to delete this camera profile?')) {
                await fetch(`/api/v1/profiles/camera/${id}`, { method: 'DELETE' });
                fetchAndRender();
            }
        }
    });

     objectTbody.addEventListener('click', async (e) => {
        const editBtn = e.target.closest('.edit-object-btn');
        const deleteBtn = e.target.closest('.delete-object-btn');

        if (editBtn) {
            const id = editBtn.dataset.id;
            const res = await fetch(`/api/v1/profiles/object/${id}`);
            if (!res.ok) return;
            const p = await res.json();
            
            document.getElementById('object-modal-title').textContent = 'Edit Object Recipe';
            document.getElementById('object-profile-id').value = p.id;
            document.getElementById('object-profile-name').value = p.name;
            document.getElementById('object-camera-profile-select').value = p.camera_profile_id;
            document.getElementById('object-sort-offset').value = p.sort_offset_ms;
            document.getElementById('object-profile-desc').value = p.description;
            objectModal.show();
        }

        if (deleteBtn) {
            const id = deleteBtn.dataset.id;
            if (confirm('Are you sure you want to delete this object recipe?')) {
                await fetch(`/api/v1/profiles/object/${id}`, { method: 'DELETE' });
                fetchAndRender();
            }
        }
    });

    cameraForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('camera-profile-id').value;
        const method = id ? 'PUT' : 'POST';
        const url = id ? `/api/v1/profiles/camera/${id}` : '/api/v1/profiles/camera';
        
        const body = {
            name: document.getElementById('camera-profile-name').value,
            exposure: parseInt(document.getElementById('camera-profile-exposure').value),
            gain: parseInt(document.getElementById('camera-profile-gain').value),
            brightness: parseInt(document.getElementById('camera-profile-brightness').value),
            white_balance_temp: parseInt(document.getElementById('camera-profile-wb').value),
            autofocus: document.getElementById('camera-profile-autofocus').checked,
            description: document.getElementById('camera-profile-desc').value,
        };

        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (res.ok) {
            cameraModal.hide();
            fetchAndRender();
        } else {
            alert('Failed to save camera profile.');
        }
    });

    objectForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const id = document.getElementById('object-profile-id').value;
        const method = id ? 'PUT' : 'POST';
        const url = id ? `/api/v1/profiles/object/${id}` : '/api/v1/profiles/object';

        const body = {
            name: document.getElementById('object-profile-name').value,
            camera_profile_id: parseInt(document.getElementById('object-camera-profile-select').value),
            sort_offset_ms: parseInt(document.getElementById('object-sort-offset').value),
            description: document.getElementById('object-profile-desc').value,
        };

        const res = await fetch(url, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body)
        });

        if (res.ok) {
            objectModal.hide();
            fetchAndRender();
        } else {
            alert('Failed to save object profile.');
        }
    });

    // Initial load
    fetchAndRender();
});