document.addEventListener('DOMContentLoaded', function () {
    const galleryCol1 = document.getElementById('gallery-col-1');
    const galleryCol2 = document.getElementById('gallery-col-2');
    const loader = document.getElementById('loader');

    let currentPage = 1;
    let isLoading = false;
    let hasMoreImages = true;

    async function fetchImages(page) {
        if (isLoading || !hasMoreImages) return;
        isLoading = true;
        loader.style.display = 'block';

        try {
            const response = await fetch(`/api/v1/camera/captures?page=${page}&page_size=8`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            
            appendImages(data.images);
            hasMoreImages = data.has_more;
            currentPage++;

            if (!hasMoreImages) {
                loader.style.display = 'none';
            }

        } catch (error) {
            console.error("Failed to fetch images:", error);
            loader.style.display = 'none';
        } finally {
            isLoading = false;
        }
    }

    function appendImages(images) {
        images.forEach((imagePath, index) => {
            const galleryItem = document.createElement('a');
            galleryItem.href = imagePath;
            galleryItem.target = '_blank';
            galleryItem.className = 'gallery-item';

            const img = document.createElement('img');
            img.src = imagePath;
            img.alt = `Capture ${imagePath.split('/').pop()}`;
            img.loading = 'lazy'; // Native browser lazy loading

            galleryItem.appendChild(img);

            // Distribute images between the two columns
            if (index % 2 === 0) {
                galleryCol1.appendChild(galleryItem);
            } else {
                galleryCol2.appendChild(galleryItem);
            }
        });
    }

    // --- Intersection Observer for infinite scroll ---
    const observer = new IntersectionObserver((entries) => {
        // If the loader is visible in the viewport, fetch more images
        if (entries[0].isIntersecting) {
            fetchImages(currentPage);
        }
    }, {
        root: null, // relative to the viewport
        rootMargin: '0px',
        threshold: 0.1 // trigger when 10% of the loader is visible
    });

    // Start observing the loader
    observer.observe(loader);

    // Initial load
    fetchImages(currentPage);
});