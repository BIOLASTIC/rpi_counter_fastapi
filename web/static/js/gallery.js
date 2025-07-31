/**
 * Reusable gallery logic for fetching and displaying captured images.
 * It supports infinite scrolling to load more images as the user scrolls down.
 */

// A variable to keep track of the current page for a given camera
const galleryState = {
    page: 1,
    isLoading: false,
    hasMore: true,
};

/**
 * Fetches a page of images from the API.
 * @param {string} cameraId - The ID of the camera to fetch images for (e.g., 'rpi', 'usb').
 */
async function fetchImages(cameraId) {
    if (galleryState.isLoading || !galleryState.hasMore) {
        return; // Don't fetch if already loading or no more images
    }

    galleryState.isLoading = true;
    const loader = document.getElementById('loader');
    loader.style.display = 'block';

    try {
        const response = await fetch(`/api/v1/camera/captures/${cameraId}?page=${galleryState.page}&page_size=10`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();

        displayImages(data.images);
        galleryState.hasMore = data.has_more;
        galleryState.page += 1; // Increment page for the next fetch

        if (!galleryState.hasMore) {
            loader.innerHTML = '<p class="text-muted">No more images to load.</p>';
        }

    } catch (error) {
        console.error('Failed to fetch images:', error);
        loader.innerHTML = `<p class="text-danger">Error loading images: ${error.message}</p>`;
    } finally {
        galleryState.isLoading = false;
        if (galleryState.hasMore) {
             loader.style.display = 'none';
        }
    }
}

/**
 * Appends images to the DOM, distributing them between two columns.
 * @param {string[]} imageUrls - An array of image URLs to display.
 */
function displayImages(imageUrls) {
    const col1 = document.getElementById('gallery-col-1');
    const col2 = document.getElementById('gallery-col-2');

    imageUrls.forEach((url, index) => {
        const galleryItem = document.createElement('div');
        galleryItem.className = 'gallery-item';
        galleryItem.innerHTML = `
            <a href="${url}" target="_blank" rel="noopener noreferrer">
                <img src="${url}" alt="Captured image" loading="lazy">
            </a>
        `;

        // Distribute images between the two columns
        if (index % 2 === 0) {
            col1.appendChild(galleryItem);
        } else {
            col2.appendChild(galleryItem);
        }
    });
}

/**
 * Initializes the gallery, sets up the scroll listener, and performs the first fetch.
 * @param {string} cameraId - The ID of the camera for this gallery page.
 */
export function initializeGallery(cameraId) {
    // Initial fetch
    fetchImages(cameraId);

    // Infinite scroll listener
    window.addEventListener('scroll', () => {
        // If user has scrolled to the bottom of the page
        if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 200) {
            fetchImages(cameraId);
        }
    });
}