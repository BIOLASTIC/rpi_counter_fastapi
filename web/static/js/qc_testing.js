// web/static/js/qc_testing.js

document.addEventListener('DOMContentLoaded', function () {
    const qcForm = document.getElementById('qc-test-form');
    const imageUpload = document.getElementById('image-upload');
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    const submitBtn = document.getElementById('submit-btn');
    const submitSpinner = document.getElementById('submit-spinner');
    
    const resultsArea = document.getElementById('results-area');
    const resultCanvas = document.getElementById('result-canvas');
    const jsonResponseEl = document.getElementById('json-response');
    const errorAlert = document.getElementById('error-alert');

    const QC_API_BASE_URL = 'http://192.168.88.97:8001';

    qcForm.addEventListener('submit', async function (e) {
        e.preventDefault();
        
        submitBtn.disabled = true;
        submitSpinner.style.display = 'inline-block';
        resultsArea.style.display = 'none';
        errorAlert.style.display = 'none';
        
        const imageFile = imageUpload.files[0];
        const checksToPerform = Array.from(checkboxes)
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        if (!imageFile || checksToPerform.length === 0) {
            showError('Please upload an image and select at least one check.');
            resetButton();
            return;
        }

        const formData = new FormData();
        formData.append('image', imageFile);
        formData.append('serial_number', `test-${Date.now()}`);

        const params = new URLSearchParams();
        checksToPerform.forEach(check => params.append('checks_to_perform', check));
        
        const requestUrl = `${QC_API_BASE_URL}/api/v1/inspection/single/upload?${params.toString()}`;

        try {
            const response = await fetch(requestUrl, {
                method: 'POST',
                body: formData,
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || `API returned status ${response.status}`);
            }

            const data = await response.json();
            
            displayJsonResponse(data);
            await drawAnnotatedImage(imageFile, data);
            resultsArea.style.display = 'block';

        } catch (error) {
            showError(`An error occurred: ${error.message}`);
        } finally {
            resetButton();
        }
    });

    function displayJsonResponse(data) {
        jsonResponseEl.textContent = JSON.stringify(data, null, 2);
    }

    async function drawAnnotatedImage(imageFile, apiData) {
        const ctx = resultCanvas.getContext('2d');
        const img = new Image();
        
        const imageUrl = URL.createObjectURL(imageFile);

        img.onload = () => {
            resultCanvas.width = img.width;
            resultCanvas.height = img.height;
            ctx.drawImage(img, 0, 0);
            URL.revokeObjectURL(imageUrl);

            // --- THIS IS THE CORRECTED LOGIC ---
            // Create a unified list of all valid detections from the entire response.
            const allDetections = [];
            const results = apiData.identification_results || {};

            // 1. Check for category detection
            if (results.category && results.category.bounding_box) {
                allDetections.push({
                    label: `${results.category.detected_product_type} (${results.category.confidence.toFixed(2)})`,
                    box: results.category.bounding_box
                });
            }

            // 2. Check for size detection
            if (results.size && results.size.bounding_box) {
                allDetections.push({
                    label: `Size: ${results.size.detected_product_size} (${results.size.confidence.toFixed(2)})`,
                    box: results.size.bounding_box
                });
            }
            
            // 3. Check for tick detections
            if (results.ticks) {
                if (results.ticks.name_tick_status && results.ticks.name_tick_status.bounding_box) {
                    allDetections.push({
                        label: `Name Tick: ${results.ticks.name_tick_status.status}`,
                        box: results.ticks.name_tick_status.bounding_box
                    });
                }
                if (results.ticks.size_tick_status && results.ticks.size_tick_status.bounding_box) {
                    allDetections.push({
                        label: `Size Tick: ${results.ticks.size_tick_status.status}`,
                        box: results.ticks.size_tick_status.bounding_box
                    });
                }
            }

            // 4. Check for defect detections
            if (results.defects && results.defects.defects) {
                results.defects.defects.forEach(defect => {
                    if (defect.bounding_box) {
                        allDetections.push({
                            label: `${defect.defect_type} (${defect.confidence.toFixed(2)})`,
                            box: defect.bounding_box
                        });
                    }
                });
            }

            // --- Now, draw based on the unified list ---
            if (allDetections.length === 0) {
                ctx.fillStyle = 'red';
                ctx.font = 'bold 80px sans-serif';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.shadowColor = 'black';
                ctx.shadowBlur = 10;
                ctx.fillText('NO DETECTION', resultCanvas.width / 2, resultCanvas.height / 2);
            } else {
                allDetections.forEach(detection => {
                    const box = detection.box;
                    
                    ctx.strokeStyle = '#00FF00'; // Bright green
                    ctx.lineWidth = 4;
                    ctx.strokeRect(box.x, box.y, box.width, box.height);

                    // Draw label with background
                    ctx.fillStyle = '#00FF00';
                    ctx.font = 'bold 24px sans-serif';
                    ctx.textBaseline = 'bottom';
                    const textWidth = ctx.measureText(detection.label).width;
                    ctx.fillRect(box.x, box.y - 30, textWidth + 10, 30);
                    ctx.fillStyle = 'black';
                    ctx.fillText(detection.label, box.x + 5, box.y);
                });
            }
            // --- END OF CORRECTED LOGIC ---
        };

        img.src = imageUrl;
    }

    function showError(message) {
        errorAlert.textContent = message;
        errorAlert.style.display = 'block';
    }

    function resetButton() {
        submitBtn.disabled = false;
        submitSpinner.style.display = 'none';
    }
});