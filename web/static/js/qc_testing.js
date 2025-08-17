// web/static/js/qc_testing.js

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('qc-test-form');
    const imageUpload = document.getElementById('image-upload');
    const submitBtn = document.getElementById('submit-btn');
    const spinner = document.getElementById('submit-spinner');
    const resultsArea = document.getElementById('results-area');
    const errorAlert = document.getElementById('error-alert');
    const jsonResponseEl = document.getElementById('json-response');
    const canvas = document.getElementById('result-canvas');
    const ctx = canvas.getContext('2d');
    let uploadedImage = null;

    // --- Element cache for details ---
    const details = {
        qc: document.getElementById('details-qc'),
        category: document.getElementById('details-category'),
        size: document.getElementById('details-size'),
        defects: document.getElementById('details-defects'),
    };

    const AI_API_BASE_URL = 'http://192.168.88.97:8001/api/v1/inspection/single/upload';

    imageUpload.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                uploadedImage = new Image();
                uploadedImage.onload = () => console.log('Image loaded for annotation');
                uploadedImage.src = event.target.result;
            };
            reader.readAsDataURL(file);
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const imageFile = imageUpload.files[0];
        const checks = Array.from(form.querySelectorAll('input[type=checkbox]:checked')).map(cb => cb.value);
        if (!imageFile || checks.length === 0) return showError('Please upload an image and select at least one check.');
        setLoading(true);
        hideError();
        resultsArea.style.display = 'none';

        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('serial_number', `test-${Date.now()}`);
        const params = new URLSearchParams();
        checks.forEach(check => params.append('checks_to_perform', check));

        try {
            const response = await fetch(`${AI_API_BASE_URL}?${params.toString()}`, { method: 'POST', body: formData });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }
            const results = await response.json();
            displayResults(results);
        } catch (error) {
            showError(error.message);
        } finally {
            setLoading(false);
        }
    });

    function displayResults(results) {
        resultsArea.style.display = 'block';
        jsonResponseEl.textContent = JSON.stringify(results, null, 2);
        updateDetailsText(results); // Populate the text summary
        if (uploadedImage) {
            canvas.width = uploadedImage.width;
            canvas.height = uploadedImage.height;
            ctx.drawImage(uploadedImage, 0, 0);
            drawAnnotations(results);
        }
    }

    function updateDetailsText(results) {
        const idResults = results.identification_results || {};
        const qc = idResults.qc;
        details.qc.textContent = qc ? qc.overall_status : 'N/A';
        const category = idResults.category;
        details.category.textContent = category ? `${category.detected_product_type} (${(category.confidence * 100).toFixed(1)}%)` : 'N/A';
        const size = idResults.size;
        details.size.textContent = (size && size.detected_product_size) ? size.detected_product_size : 'N/A';
        const defects = idResults.defects && idResults.defects.defects ? idResults.defects.defects : [];
        details.defects.textContent = defects.length > 0 ? `${defects.length} Found` : 'None Detected';
    }

    function drawAnnotations(results) {
        const idResults = results.identification_results;
        if (!idResults) return;

        const drawBoundingBox = (boxData, label, color, thickness, labelInside = false) => {
            if (!boxData) return;
            const { x, y, width, height } = boxData;
            ctx.strokeStyle = color;
            ctx.lineWidth = thickness;
            ctx.strokeRect(x, y, width, height);
            const fontScale = 1.0;
            const font = `bold ${24 * fontScale}px sans-serif`;
            ctx.font = font;
            const textMetrics = ctx.measureText(label);
            const textWidth = textMetrics.width;
            const textHeight = 24 * fontScale;
            if (labelInside) {
                const textY = y + textHeight + 10;
                ctx.fillStyle = color;
                ctx.fillRect(x, y, textWidth + 20, textHeight + 20);
                ctx.fillStyle = 'white';
                ctx.fillText(label, x + 10, textY);
            } else {
                const textY = y - 10, bgY = y - textHeight - 20;
                ctx.fillStyle = color;
                ctx.fillRect(x, bgY, textWidth + 10, textHeight + 10);
                ctx.fillStyle = 'white';
                ctx.fillText(label, x + 5, textY);
            }
        };

        const qcCheck = idResults.qc;
        if (qcCheck && qcCheck.overall_status) drawBoundingBox(qcCheck.bounding_box, `Status: ${qcCheck.overall_status}`, qcCheck.overall_status === 'ACCEPT' ? 'lime' : 'red', 10, true);
        const categoryCheck = idResults.category;
        if (categoryCheck && categoryCheck.detected_product_type) drawBoundingBox(categoryCheck.bounding_box, `Type: ${categoryCheck.detected_product_type} (${(categoryCheck.confidence || 0).toFixed(2)})`, 'blue', 5);
        const defects = (idResults.defects && idResults.defects.defects) ? idResults.defects.defects : [];
        defects.forEach(defect => drawBoundingBox(defect.bounding_box, `Defect: ${defect.defect_type} (${(defect.confidence || 0).toFixed(2)})`, 'yellow', 3));
    }

    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        spinner.style.display = isLoading ? 'inline-block' : 'none';
    }
    function showError(message) {
        errorAlert.textContent = message;
        errorAlert.style.display = 'block';
    }
    function hideError() { errorAlert.style.display = 'none'; }
});