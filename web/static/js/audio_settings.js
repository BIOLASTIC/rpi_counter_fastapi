// rpi_counter_fastapi-apintrigation/web/static/js/audio_settings.js

document.addEventListener('DOMContentLoaded', function () {
    const fileListContainer = document.getElementById('audio-file-list');
    const mappingContainer = document.getElementById('event-mapping-container');
    const uploadInput = document.getElementById('audio-upload-input');
    const uploadBtn = document.getElementById('upload-btn');
    const saveMappingsBtn = document.getElementById('save-mappings-btn');
    const toastElement = document.getElementById('notification-toast');
    const toast = new bootstrap.Toast(toastElement);

    let state = {
        audio_files: [],
        mappings: {},
        valid_events: {}
    };

    function showToast(title, body, isError = false) {
        const toastHeader = toastElement.querySelector('.toast-header');
        toastElement.querySelector('#toast-title').textContent = title;
        toastElement.querySelector('#toast-body').textContent = body;
        
        if(isError) {
            toastHeader.classList.add('bg-danger', 'text-white');
            toastHeader.classList.remove('bg-success');
        } else {
            toastHeader.classList.add('bg-success', 'text-white');
            toastHeader.classList.remove('bg-danger');
        }
        toast.show();
    }

    async function fetchData() {
        try {
            const response = await fetch('/api/v1/audio/config');
            if (!response.ok) throw new Error('Failed to fetch config');
            state = await response.json();
            render();
        } catch (error) {
            console.error("Error fetching audio config:", error);
            showToast('Error', 'Could not load audio settings from server.', true);
        }
    }

    function render() {
        renderFileList();
        renderMappings();
    }

    function renderFileList() {
        fileListContainer.innerHTML = '';
        if (state.audio_files.length === 0) {
            fileListContainer.innerHTML = '<p class="text-center text-muted">No audio files found.</p>';
            return;
        }

        state.audio_files.forEach(filename => {
            const item = document.createElement('div');
            item.className = 'list-group-item d-flex justify-content-between align-items-center';
            item.innerHTML = `
                <span><i class="bi bi-soundwave me-2"></i>${filename}</span>
                <button class="btn btn-sm btn-outline-danger delete-file-btn" data-filename="${filename}">
                    <i class="bi bi-trash"></i>
                </button>
            `;
            fileListContainer.appendChild(item);
        });
    }

    function renderMappings() {
        mappingContainer.innerHTML = '';
        for (const [category, events] of Object.entries(state.valid_events)) {
            const categoryTitle = category.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
            
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'mb-4';
            categoryDiv.innerHTML = `<h5>${categoryTitle}</h5>`;
            
            const table = document.createElement('table');
            table.className = 'table table-sm';
            const tbody = document.createElement('tbody');

            events.forEach(event => {
                const row = document.createElement('tr');
                
                const labelCell = document.createElement('td');
                labelCell.className = 'w-50';
                labelCell.textContent = event;

                const selectCell = document.createElement('td');
                const select = document.createElement('select');
                select.className = 'form-select form-select-sm event-mapping-select';
                select.dataset.event = event;
                
                let optionsHtml = '<option value="">None</option>';
                state.audio_files.forEach(file => {
                    const isSelected = state.mappings[event] === file ? 'selected' : '';
                    optionsHtml += `<option value="${file}" ${isSelected}>${file}</option>`;
                });
                select.innerHTML = optionsHtml;
                
                selectCell.appendChild(select);
                row.appendChild(labelCell);
                row.appendChild(selectCell);
                tbody.appendChild(row);
            });

            table.appendChild(tbody);
            categoryDiv.appendChild(table);
            mappingContainer.appendChild(categoryDiv);
        }
    }

    async function handleUpload() {
        const file = uploadInput.files[0];
        if (!file) {
            showToast('Upload Error', 'Please select a file to upload.', true);
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            uploadBtn.disabled = true;
            uploadBtn.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Uploading...`;
            
            const response = await fetch('/api/v1/audio/upload', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.detail || 'Upload failed');
            }
            showToast('Success', result.message);
            await fetchData(); // Refresh data and UI
        } catch (error) {
            console.error('Upload error:', error);
            showToast('Upload Error', error.message, true);
        } finally {
            uploadBtn.disabled = false;
            uploadBtn.innerHTML = 'Upload';
            uploadInput.value = ''; // Clear the input
        }
    }

    async function handleDeleteFile(filename) {
        if (!confirm(`Are you sure you want to delete "${filename}"? This cannot be undone.`)) {
            return;
        }

        try {
            const response = await fetch(`/api/v1/audio/files/${filename}`, {
                method: 'DELETE'
            });

            const result = await response.json();
            if (!response.ok) {
                throw new Error(result.detail || 'Failed to delete file');
            }
            showToast('Success', result.message);
            await fetchData();
        } catch (error) {
            console.error('Delete error:', error);
            showToast('Delete Error', error.message, true);
        }
    }

    async function handleSaveMappings() {
        const newMappings = {};
        document.querySelectorAll('.event-mapping-select').forEach(select => {
            const event = select.dataset.event;
            const filename = select.value;
            if (filename) {
                newMappings[event] = filename;
            }
        });
        
        try {
            saveMappingsBtn.disabled = true;
            saveMappingsBtn.innerHTML = `<span class="spinner-border spinner-border-sm"></span> Saving...`;

            const response = await fetch('/api/v1/audio/mappings', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(newMappings)
            });
            
            const result = await response.json();
            if (!response.ok) {
                throw new Error(result.detail || 'Failed to save mappings');
            }
            showToast('Success', result.message);
            await fetchData();
        } catch (error) {
            console.error('Save mappings error:', error);
            showToast('Save Error', error.message, true);
        } finally {
            saveMappingsBtn.disabled = false;
            saveMappingsBtn.innerHTML = '<i class="bi bi-save me-2"></i>Save All Mappings';
        }
    }

    uploadBtn.addEventListener('click', handleUpload);
    saveMappingsBtn.addEventListener('click', handleSaveMappings);
    fileListContainer.addEventListener('click', function(e) {
        const button = e.target.closest('.delete-file-btn');
        if (button) {
            handleDeleteFile(button.dataset.filename);
        }
    });

    fetchData();
});