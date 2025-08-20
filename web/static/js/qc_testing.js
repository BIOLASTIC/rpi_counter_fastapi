// rpi_counter_fastapi-apintrigation/web/static/js/qc_testing.js

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('qc-test-form');
    const submitBtn = document.getElementById('submit-btn');
    const spinner = document.getElementById('submit-spinner');
    const imageUpload = document.getElementById('image-upload');
    const resultsArea = document.getElementById('results-area');
    const errorAlert = document.getElementById('error-alert');
    const jsonResponseEl = document.getElementById('json-response');
    
    const canvas = document.getElementById('result-canvas');
    const ctx = canvas.getContext('2d');
    let originalImage = null;

    const get = (path, obj) => path.reduce((xs, x) => (xs && xs[x] != null) ? xs[x] : null, obj);

    // --- THIS IS THE CORRECTED DRAWING FUNCTION ---
    function drawOBB(flatPoints, color, label, confidence) {
        // 1. INPUT VALIDATION: Ensure we have a flat array of 8 numbers.
        if (!flatPoints || flatPoints.length !== 8) {
            console.error("Invalid OBB points received:", flatPoints);
            return;
        }

        // 2. RESHAPE THE DATA: Convert the flat array into an array of [x, y] pairs.
        const points = [];
        for (let i = 0; i < flatPoints.length; i += 2) {
            points.push([flatPoints[i], flatPoints[i+1]]);
        }

        // 3. SCALE POINTS: Adjust coordinates from the original image size to the displayed canvas size.
        const scaleX = canvas.width / originalImage.naturalWidth;
        const scaleY = canvas.height / originalImage.naturalHeight;
        const scaledPoints = points.map(p => [p[0] * scaleX, p[1] * scaleY]);

        // 4. DRAW THE POLYGON
        ctx.strokeStyle = color;
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(scaledPoints[0][0], scaledPoints[0][1]);
        for (let i = 1; i < scaledPoints.length; i++) {
            ctx.lineTo(scaledPoints[i][0], scaledPoints[i][1]);
        }
        ctx.closePath();
        ctx.stroke();

        // 5. DRAW THE LABEL with a background for better visibility
        ctx.fillStyle = color;
        ctx.font = 'bold 20px sans-serif';
        const fullLabel = `${label} (${(confidence * 100).toFixed(1)}%)`;
        const textMetrics = ctx.measureText(fullLabel);
        const textWidth = textMetrics.width;
        const textHeight = 24; // Approximation of font height with padding
        
        const labelX = scaledPoints[0][0];
        const labelY = scaledPoints[0][1] - textHeight - 5; // Position above the first point

        ctx.fillRect(labelX, labelY, textWidth + 10, textHeight);
        
        ctx.fillStyle = '#ffffff'; // White text
        ctx.fillText(fullLabel, labelX + 5, scaledPoints[0][1] - 10);
    }
    // --- END OF CORRECTION ---

    function updateDetails(results) {
        const qcStatus = get(['yolo11m_qc', 'detections', 0, 'class_name'], results) || '--';
        const qcConfidence = get(['yolo11m_qc', 'detections', 0, 'confidence'], results);
        const qcAngle = get(['yolo11m_qc', 'detections', 0, 'coordinates', 'rotated_box', 'angle_degrees'], results);
        
        const qcStatusEl = document.getElementById('details-qc-status');
        qcStatusEl.textContent = qcStatus;
        qcStatusEl.className = `status-${qcStatus}`;
        document.getElementById('details-qc-confidence').textContent = qcConfidence ? `${(qcConfidence * 100).toFixed(1)}%` : '--';
        document.getElementById('details-qc-angle').textContent = qcAngle ? `${qcAngle.toFixed(2)}°` : '--';

        const categoryName = get(['yolo11m_categories', 'detections', 0, 'class_name'], results) || '--';
        const categoryConfidence = get(['yolo11m_categories', 'detections', 0, 'confidence'], results);
        const categoryAngle = get(['yolo11m_categories', 'detections', 0, 'coordinates', 'rotated_box', 'angle_degrees'], results);

        document.getElementById('details-category-name').textContent = categoryName;
        document.getElementById('details-category-confidence').textContent = categoryConfidence ? `${(categoryConfidence * 100).toFixed(1)}%` : '--';
        document.getElementById('details-category-angle').textContent = categoryAngle ? `${categoryAngle.toFixed(2)}°` : '--';
    }

    form.addEventListener('submit', async function (event) {
        event.preventDefault();
        
        spinner.style.display = 'inline-block';
        submitBtn.disabled = true;
        resultsArea.style.display = 'none';
        errorAlert.style.display = 'none';
        originalImage = null;

        const imageFile = imageUpload.files[0];
        if (!imageFile) {
            showError("Please select an image file.");
            return;
        }

        const checkedModels = Array.from(document.querySelectorAll('input[type="checkbox"]:checked')).map(cb => cb.value);
        if (checkedModels.length === 0) {
            showError("Please select at least one model to run.");
            return;
        }

        const formData = new FormData();
        formData.append('image', imageFile);
        checkedModels.forEach(model => formData.append('models', model));

        try {
            const response = await fetch('/api/v1/analytics/qc-test/upload', {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
            }

            const results = await response.json();
            
            const reader = new FileReader();
            reader.onload = function(e) {
                originalImage = new Image();
                originalImage.onload = function() {
                    canvas.width = originalImage.naturalWidth;
                    canvas.height = originalImage.naturalHeight;
                    ctx.drawImage(originalImage, 0, 0);

                    const qcDetection = get(['yolo11m_qc', 'detections', 0], results);
                    if (qcDetection) {
                        const color = qcDetection.class_name === 'ACCEPT' ? '#198754' : '#dc3545';
                        drawOBB(qcDetection.coordinates.obb_points, color, qcDetection.class_name, qcDetection.confidence);
                    }
                    
                    const catDetection = get(['yolo11m_categories', 'detections', 0], results);
                     if (catDetection) {
                        drawOBB(catDetection.coordinates.obb_points, '#0d6efd', catDetection.class_name, catDetection.confidence);
                    }

                    jsonResponseEl.textContent = JSON.stringify(results, null, 2);
                    updateDetails(results);
                    resultsArea.style.display = 'block';
                }
                originalImage.src = e.target.result;
            }
            reader.readAsDataURL(imageFile);

        } catch (error) {
            showError(error.message);
        } finally {
            spinner.style.display = 'none';
            submitBtn.disabled = false;
        }
    });

    function showError(message) {
        errorAlert.textContent = `Error: ${message}`;
        errorAlert.style.display = 'block';
        spinner.style.display = 'none';
        submitBtn.disabled = false;
    }
});