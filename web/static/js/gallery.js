// /static/js/gallery.js

document.addEventListener('DOMContentLoaded', () => {
    const galleryContainer = document.getElementById('gallery-container');
    const loader = document.getElementById('loader');
    
    // --- THE FIX: Check if the container element exists before proceeding ---
    if (!galleryContainer) {
        console.error("Gallery container with ID 'gallery-container' not found. Aborting script.");
        return;
    }

    // --- The script now dynamically determines the camera ID from the HTML ---
    const CAMERA_ID = galleryContainer.dataset.cameraId;
    
    if (!CAMERA_ID) {
        console.error("Camera ID not found in data-camera-id attribute. Aborting script.");
        return;
    }

    let currentPage = 1;
    let isLoading = false;
    let hasMore = true;

    async function fetchImages() {
        if (isLoading || !hasMore) return;
        isLoading = true;
        loader.style.display = 'block';

        try {
            const response = await fetch(`/api/v1/camera/captures/${CAMERA_ID}?page=${currentPage}&page_size=10`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            
            displayImages(data);

        } catch (error) {
            console.error("Failed to fetch images:", error);
            hasMore = false; // Stop trying on error
        } finally {
            isLoading = false;
            loader.style.display = 'none';
        }
    }

    function displayImages(data) {
        if (data.images.length > 0) {
            data.images.forEach(imagePath => {
                const galleryItem = document.createElement('div');
                galleryItem.className = 'gallery-item';

                const link = document.createElement('a');
                link.href = imagePath;
                link.target = '_blank';

                const img = document.createElement('img');
                img.src = imagePath;
                img.className = 'img-fluid';
                img.alt = 'Captured Image';
                img.loading = 'lazy';

                link.appendChild(img);
                galleryItem.appendChild(link);
                // This line will now work because we've confirmed galleryContainer is not null
                galleryContainer.appendChild(galleryItem);
            });
            hasMore = data.has_more;
            currentPage++;
        } else {
            hasMore = false;
            if (currentPage === 1) {
                const noImagesMsg = document.createElement('p');
                noImagesMsg.textContent = 'No images have been captured for this camera yet.';
                noImagesMsg.className = 'text-muted text-center';
                galleryContainer.appendChild(noImagesMsg);
            }
        }
    }

    // Initial load
    fetchImages();

    // Infinite scroll listener
    window.addEventListener('scroll', () => {
        // Only fetch more if we're near the bottom of the page
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 200) {
            fetchImages();
        }
    });
});