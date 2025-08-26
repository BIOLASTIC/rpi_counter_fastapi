document.addEventListener('DOMContentLoaded', function () {
    // --- Element Cache for AI Strategy Page ---
    const form = document.getElementById('ai-strategy-form');
    const saveBtn = document.getElementById('save-strategy-btn');
    const testAudioButtons = document.querySelectorAll('.test-audio-btn');
    const testItemPipelineBtn = document.getElementById('test-item-pipeline-btn');
    const testSummaryPipelineBtn = document.getElementById('test-summary-pipeline-btn');
    const summaryResultText = document.getElementById('summary-pipeline-result-text');

    // --- Core Functions for AI Strategy Page ---

    /**
     * Fetches the current AI strategy from the API and populates the form fields.
     */
    async function loadStrategy() {
        try {
            const response = await fetch('/api/v1/ai-strategy/');
            if (!response.ok) {
                throw new Error(`Failed to load strategy: ${response.statusText}`);
            }
            const strategy = await response.json();
            
            for (const key in strategy) {
                const element = form.elements[key];
                if (element) {
                    if (element.type === 'checkbox') {
                        element.checked = strategy[key];
                    } else {
                        element.value = strategy[key];
                    }
                }
            }
            showToast('Success', 'Successfully loaded AI & Audio strategy.');
        } catch (error) {
            console.error('Error loading AI strategy:', error);
            showToast('Error', 'Could not load AI & Audio strategy.', 'bg-danger');
        }
    }

    /**
     * Gathers all data from the form into a structured JSON object.
     * @returns {object} The form data.
     */
    function getFormData() {
        const formData = new FormData(form);
        const data = {};
        for (const [key, value] of formData.entries()) {
            const element = form.elements[key];
            if (element.type === 'checkbox') {
                data[key] = element.checked;
            } else if (element.type === 'number') {
                data[key] = parseInt(value, 10);
            } else {
                data[key] = value;
            }
        }
        // Ensure checkboxes that are unchecked are sent as false
        form.querySelectorAll('input[type="checkbox"]').forEach(cb => {
            if (!data.hasOwnProperty(cb.name)) {
                data[cb.name] = false;
            }
        });
        return data;
    }

    /**
     * Sends the current form data to the backend to be saved.
     */
    async function saveStrategy() {
        const data = getFormData();
        saveBtn.disabled = true;
        saveBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Saving...';
        
        try {
            const response = await fetch('/api/v1/ai-strategy/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data),
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to save strategy');
            }
            showToast('Success', 'AI & Audio strategy saved successfully.');
        } catch (error) {
            showToast('Error', `Failed to save strategy: ${error.message}`, 'bg-danger');
        } finally {
            saveBtn.disabled = false;
            saveBtn.innerHTML = '<i class="fas fa-save me-2"></i>Save Strategy';
        }
    }

    /**
     * Tests a single audio template by sending its text and selected engine to the backend.
     * @param {HTMLButtonElement} button - The button that was clicked.
     */
    async function testAudioTemplate(button) {
        const templateKey = button.dataset.templateKey;
        const text = document.getElementById(templateKey.toLowerCase()).value;
        const realtimeEngine = document.getElementById('realtime_tts_engine').value;
        const summaryEngine = document.getElementById('summary_tts_engine').value;
        const engineForTest = templateKey.includes('BATCH') || templateKey.includes('NEXT') || templateKey.includes('COMPLETE') ? summaryEngine : realtimeEngine;
        const ttsLanguage = document.getElementById('tts_language').value;

        button.disabled = true;
        button.innerHTML = '<span class="spinner-border spinner-border-sm"></span>';
        try {
            const response = await fetch('/api/v1/ai-strategy/test-audio', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    template_key: templateKey, 
                    text: text,
                    engine: engineForTest,
                    tts_language: ttsLanguage
                }),
            });
            if (!response.ok) throw new Error((await response.json()).detail || 'Failed to generate audio');
            
            const audioBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioBlob);
            new Audio(audioUrl).play();
        } catch (error) {
            showToast('Error', error.message, 'bg-danger');
        } finally {
            button.disabled = false;
            button.innerHTML = '<i class="fas fa-play"></i> Test';
        }
    }
    
    /**
     * Tests the full per-item LLM -> TTS pipeline.
     * @param {HTMLButtonElement} button - The button that was clicked.
     */
    async function testItemPipeline(button) {
        button.disabled = true;
        button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Testing...';
        const currentSettings = getFormData();
        try {
            const response = await fetch('/api/v1/ai-strategy/test-item-pipeline', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    llm_language: currentSettings.LANGUAGE,
                    tts_language: currentSettings.TTS_LANGUAGE,
                    word_count: currentSettings.LLM_ITEM_WORD_COUNT,
                    engine: currentSettings.REALTIME_TTS_ENGINE
                }),
            });
            if (!response.ok) throw new Error((await response.json()).detail);
            
            const audioBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioBlob);
            new Audio(audioUrl).play();
            showToast('Success', 'Per-item pipeline test successful.');
        } catch (error) {
            showToast('Error', `Per-item pipeline test failed: ${error.message}`, 'bg-danger');
        } finally {
            button.disabled = false;
            button.innerHTML = '<i class="fas fa-microchip me-2"></i>Test Per-Item Pipeline';
        }
    }

    /**
     * Tests the full batch summary LLM -> TTS pipeline.
     * @param {HTMLButtonElement} button - The button that was clicked.
     */
    async function testSummaryPipeline(button) {
        button.disabled = true;
        button.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Testing...';
        summaryResultText.style.display = 'none';
        const currentSettings = getFormData();
        try {
            const response = await fetch('/api/v1/ai-strategy/test-summary-pipeline', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    llm_language: currentSettings.LANGUAGE,
                    tts_language: currentSettings.TTS_LANGUAGE,
                    word_count: currentSettings.LLM_SUMMARY_WORD_COUNT,
                    model_preference: currentSettings.SUMMARY_LLM_MODEL,
                    engine: currentSettings.SUMMARY_TTS_ENGINE
                }),
            });
            if (!response.ok) throw new Error((await response.json()).detail);
            
            const audioBlob = await response.blob();
            const audioUrl = URL.createObjectURL(audioBlob);
            new Audio(audioUrl).play();
            showToast('Success', 'Batch summary pipeline test successful.');
        } catch (error) {
            summaryResultText.textContent = `Pipeline Test Failed: ${error.message}`;
            summaryResultText.classList.add('alert-danger');
            summaryResultText.style.display = 'block';
            showToast('Error', 'Batch summary pipeline test failed.', 'bg-danger');
        } finally {
            button.disabled = false;
            button.innerHTML = '<i class="fas fa-file-alt me-2"></i>Test Batch Summary Pipeline';
        }
    }

    // --- Event Listeners ---
    saveBtn.addEventListener('click', saveStrategy);
    testAudioButtons.forEach(button => button.addEventListener('click', () => testAudioTemplate(button)));
    testItemPipelineBtn.addEventListener('click', () => testItemPipeline(testItemPipelineBtn));
    testSummaryPipelineBtn.addEventListener('click', () => testSummaryPipeline(testSummaryPipelineBtn));

    // --- Initial Load ---
    loadStrategy();
});