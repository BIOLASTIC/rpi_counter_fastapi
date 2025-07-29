// This is a new file dedicated to the USB camera gallery.
document.addEventListener('DOMContentLoaded', () => {
    const galleryCol1 = document.getElementById('gallery-col-1');
    const galleryCol2 = document.getElementById('gallery-col-2');
    const loader = document.getElementById('loader');

    // The only change is the camera ID, ensuring it fetches from the correct API endpoint.
    const CAMERA_ID = 'usb';
    let page = 1;
    let isLoading = false;
    let hasMore = true;

    async function fetchImages() {
        if (isLoading || !hasMore) return;
        isLoading = true;
        loader.style.display = 'block';

        try {
            const response = await fetch(`/api/v1/captures/${CAMERA_ID}?page=${page}&page_size=8`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();

            if (data.images.length > 0) {
                data.images.forEach((src, index) => {
                    const galleryItem = document.createElement('div');
                    galleryItem.className = 'gallery-item';
                    const link = document.createElement('a');
                    link.href = src;
                    link.target = '_blank';
                    const img = document.createElement('img');
                    img.src = src;
                    img.loading = 'lazy';
                    link.appendChild(img);
                    galleryItem.appendChild(link);

                    // Distribute images between two columns
                    if (index % 2 === 0) {
                        galleryCol1.appendChild(galleryItem);
                    } else {
                        galleryCol2.appendChild(galleryItem);
                    }
                });
                page++;
                hasMore = data.has_more;
            } else {
                hasMore = false;
            }
        } catch (error) {
            console.error('Failed to fetch images:', error);
            hasMore = false; // Stop trying if there's an error
        } finally {
            isLoading = false;
            loader.style.display = 'none';
        }
    }

    function handleScroll() {
        // Load more images when the user is 200px from the bottom
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 200) {
            fetchImages();
        }
    }

    window.addEventListener('scroll', handleScroll, { passive: true });
    fetchImages(); // Initial load
});