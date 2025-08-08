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

// --- THIS IS THE ROBUST FIX ---
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
    if (new Date(startDate) > new Date(endDate)) {
        alert('Start date cannot be after the end date.');
        return;
    }

    console.log(`Requesting ZIP for ${cameraId} from ${startDate} to ${endDate}`);
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

        console.log("Response received from server:", response.status, response.statusText);

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `Server returned status ${response.status}`);
        }

        const blob = await response.blob();
        console.log("Blob created, size:", blob.size);

        if (blob.size === 0) {
            throw new Error("Received an empty file from the server.");
        }

        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        
        const disposition = response.headers.get('content-disposition');
        let filename = `captures_${cameraId}.zip`;
        if (disposition && disposition.includes('attachment')) {
            const matches = /filename="([^"]+)"/.exec(disposition);
            if (matches != null && matches[1]) {
                filename = matches[1];
            }
        }
        a.download = filename;
        
        document.body.appendChild(a);
        console.log("Triggering download for:", filename);
        a.click();
        
        window.URL.revokeObjectURL(url);
        a.remove();
        
    } catch (error) {
        console.error('Download failed:', error);
        alert(`Error: ${error.message}`);
    } finally {
        downloadBtn.disabled = false;
        downloadBtn.textContent = 'Download Images as ZIP';
    }
});
// ----------------------------

// Initial load
loadImages();