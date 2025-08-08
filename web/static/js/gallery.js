const galleryContainer = document.getElementById('gallery-container');
const loader = document.getElementById('loader');
const cameraId = galleryContainer.dataset.cameraId;
let currentPage = 1;
let isLoading = false;
let hasMore = true;

async function loadImages() {
    if (isLoading || !hasMore) return;
    isLoading = true;
    loader.style.display = 'block';

    try {
        const response = await fetch(`/api/v1/camera/captures/${cameraId}?page=${currentPage}&page_size=12`);
        if (!response.ok) throw new Error('Failed to load images');
        const data = await response.json();
        
        data.images.forEach(imagePath => {
            const item = document.createElement('div');
            item.className = 'gallery-item';
            item.innerHTML = `<a href="${imagePath}" target="_blank"><img src="${imagePath}" loading="lazy"></a>`;
            galleryContainer.appendChild(item);
        });
        
        hasMore = data.has_more;
        currentPage++;
    } catch (error) {
        console.error('Error loading images:', error);
        loader.innerHTML = '<p class="text-danger">Failed to load images.</p>';
    } finally {
        isLoading = false;
        if (!hasMore) loader.style.display = 'none';
    }
}

// Infinite scroll listener
window.addEventListener('scroll', () => {
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 500) {
        loadImages();
    }
});

// --- PHASE 5: New ZIP Download Logic ---
const downloadBtn = document.getElementById('download-zip-btn');
const startDateInput = document.getElementById('start-date');
const endDateInput = document.getElementById('end-date');

// Set default dates to today
const today = new Date().toISOString().split('T')[0];
startDateInput.value = today;
endDateInput.value = today;

downloadBtn.addEventListener('click', async () => {
    const startDate = startDateInput.value;
    const endDate = endDateInput.value;

    if (!startDate || !endDate) {
        alert('Please select both a start and end date.');
        return;
    }

    downloadBtn.disabled = true;
    downloadBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Creating ZIP...';

    try {
        const response = await fetch('/api/v1/camera/captures/download-zip', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                camera_id: cameraId,
                start_date: startDate,
                end_date: endDate
            }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create ZIP file.');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        // Extract filename from response header if available, otherwise create one
        const disposition = response.headers.get('content-disposition');
        let filename = `captures_${cameraId}.zip`;
        if (disposition && disposition.indexOf('attachment') !== -1) {
            const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
            const matches = filenameRegex.exec(disposition);
            if (matches != null && matches[1]) {
                filename = matches[1].replace(/['"]/g, '');
            }
        }
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
        
    } catch (error) {
        alert(`Error: ${error.message}`);
    } finally {
        downloadBtn.disabled = false;
        downloadBtn.textContent = 'Download Images as ZIP';
    }
});

// Initial load
loadImages();