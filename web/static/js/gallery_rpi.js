// /static/js/gallery_rpi.js

document.addEventListener('DOMContentLoaded', () => {
    const galleryContainer = document.getElementById('gallery-container');
    const loader = document.getElementById('loader');
    
    // The only change from the USB version is this CAMERA_ID variable
    const CAMERA_ID = 'rpi'; 

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
            
            if (data.images.length > 0) {
                data.images.forEach(imagePath => {
                    const galleryItem = document.createElement('div');
        galleryContainer.appendChild(galleryItem); // <--- THIS IS LINE 43, THE CRASH POINT

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
                    galleryContainer.appendChild(galleryItem);
                });
                hasMore = data.has_more;
                currentPage++;
            } else {
                hasMore = false;
            }
        } catch (error) {
            console.error("Failed to fetch images:", error);
            hasMore = false; // Stop trying on error
        } finally {
            isLoading = false;
            loader.style.display = 'none';
        }
    }

    // Initial load
    fetchImages();

    // Infinite scroll listener
    window.addEventListener('scroll', () => {
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 100) {
            fetchImages();
        }
    });
});