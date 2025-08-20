document.addEventListener('DOMContentLoaded', () => {
    // Element References
    const loader = document.getElementById('loader');
    const content = document.getElementById('analytics-content');
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    const operatorFilter = document.getElementById('operator-filter');
    const productFilter = document.getElementById('product-filter');
    const filterBtn = document.getElementById('filter-btn');
    const exportBtn = document.getElementById('export-btn');

    // Chart instances
    let hourlyChart, productMixChart, downtimeChart, dailyTrendChart;

    const CHART_CONFIG = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: true, position: 'bottom', labels: { color: '#343a40' } } },
        scales: {
            x: { ticks: { color: '#6c757d' }, grid: { display: false } },
            y: { ticks: { color: '#6c757d', beginAtZero: true }, grid: { color: '#e9ecef' } }
        }
    };

    // Fetches analytics data and orchestrates rendering
    async function fetchAndRenderAnalytics() {
        loader.style.display = 'block';
        content.style.visibility = 'hidden';

        const params = new URLSearchParams();
        if (startDateInput.value) params.append('start_date', new Date(startDateInput.value).toISOString());
        if (endDateInput.value) params.append('end_date', new Date(endDateInput.value).toISOString());
        if (operatorFilter.value) params.append('operator_id', operatorFilter.value);
        if (productFilter.value) params.append('product_id', productFilter.value);
        
        const url = `/api/v1/analytics/summary?${params.toString()}`;

        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();
            
            updateKpiCards(data.kpis);
            updateOeeCards(data.oee_lite);
            renderDowntimeChart(data.downtime);
            renderDailyTrendChart(data.daily_trends);
            renderHourlyChart(data.hourly_throughput);
            renderProductMixChart(data.product_counts);
            populateTopTables(data.top_5_products, data.quality_control.top_5_defects);

        } catch (error) {
            console.error('Error fetching analytics data:', error);
            content.innerHTML = '<div class="alert alert-danger">Could not load analytics data. Please try again.</div>';
        } finally {
            loader.style.display = 'none';
            content.style.visibility = 'visible';
        }
    }
    
    // --- Data Population Functions ---
    
    function updateKpiCards(kpis) {
        document.getElementById('kpi-total-items').textContent = kpis.total_items_detected.toLocaleString();
        document.getElementById('kpi-total-runs').textContent = kpis.total_runs.toLocaleString();
        document.getElementById('kpi-completed-runs').textContent = kpis.completed_runs.toLocaleString();
        document.getElementById('kpi-failed-runs').textContent = kpis.failed_runs.toLocaleString();
        document.getElementById('kpi-aborted-runs').textContent = kpis.aborted_runs.toLocaleString();
        document.getElementById('kpi-pass-rate').textContent = `${kpis.quality_pass_rate.toFixed(1)}%`;
    }

    function updateOeeCards(oee) {
        document.getElementById('oee-availability').textContent = `${oee.availability.toFixed(1)}%`;
        document.getElementById('oee-performance').textContent = oee.performance_items_per_hour.toFixed(0);
    }
    
    function populateTopTables(products, defects) {
        const populate = (tbodyId, data, nameKey, valueKey) => {
            const tbody = document.querySelector(`#${tbodyId} tbody`);
            tbody.innerHTML = '';
            if (data.length > 0) {
                data.forEach(item => {
                    const row = `<tr><td>${item[nameKey]}</td><td class="text-end fw-bold">${item[valueKey].toLocaleString()}</td></tr>`;
                    tbody.innerHTML += row;
                });
            } else {
                 tbody.innerHTML = '<tr><td colspan="2" class="text-center text-muted">No data available.</td></tr>';
            }
        };
        populate('top-products-table', products.map(([name, count]) => ({name, count})), 'name', 'count');
        populate('top-defects-table', defects.map(([name, count]) => ({name, count})), 'name', 'count');
    }

    async function populateFilterDropdowns() {
        const populateSelect = async (url, selectElement, nameField) => {
            try {
                const response = await fetch(url);
                const data = await response.json();
                data.forEach(item => {
                    const option = new Option(item[nameField], item.id);
                    selectElement.add(option);
                });
            } catch (error) {
                console.error(`Failed to load data for ${selectElement.id}:`, error);
            }
        };
        await populateSelect('/api/v1/operators/', operatorFilter, 'name');
        await populateSelect('/api/v1/products/', productFilter, 'name');
    }

    // --- Chart Rendering Functions ---

    function renderDowntimeChart(data) {
        const ctx = document.getElementById('downtime-chart').getContext('2d');
        if (downtimeChart) downtimeChart.destroy();
        downtimeChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Downtime'],
                datasets: [
                    { label: 'Planned (hrs)', data: [data.planned_changeover_hours.toFixed(2)], backgroundColor: '#ffc107' },
                    { label: 'Unplanned (hrs)', data: [data.unplanned_downtime_hours.toFixed(2)], backgroundColor: '#dc3545' }
                ]
            },
            options: { ...CHART_CONFIG, indexAxis: 'y' }
        });
    }

    function renderDailyTrendChart(data) {
        const ctx = document.getElementById('daily-trend-chart').getContext('2d');
        const labels = Object.keys(data).sort();
        const itemsData = labels.map(day => data[day].items);
        const qualityData = labels.map(day => data[day].pass_rate);

        if (dailyTrendChart) dailyTrendChart.destroy();
        dailyTrendChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    { label: 'Items Detected', data: itemsData, yAxisID: 'yItems', borderColor: '#0d6efd', tension: 0.1 },
                    { label: 'Quality Pass Rate (%)', data: qualityData, yAxisID: 'yQuality', borderColor: '#198754', tension: 0.1 }
                ]
            },
            options: { ...CHART_CONFIG, scales: {
                x: { ticks: { color: '#6c757d' }, grid: { display: false } },
                yItems: { type: 'linear', position: 'left', ticks: { color: '#0d6efd' }, grid: { color: '#e9ecef' } },
                yQuality: { type: 'linear', position: 'right', min: 0, max: 100, ticks: { color: '#198754', callback: v => `${v}%` }, grid: { display: false } }
            }}
        });
    }

    function renderHourlyChart(data) {
        const ctx = document.getElementById('hourly-chart').getContext('2d');
        const labels = Object.keys(data).sort();
        const values = labels.map(label => data[label]);

        if (hourlyChart) hourlyChart.destroy();
        hourlyChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels.map(h => `${h}:00`),
                datasets: [{ label: 'Items per Hour', data: values, backgroundColor: 'rgba(54, 162, 235, 0.6)' }]
            },
            options: CHART_CONFIG
        });
    }

    function renderProductMixChart(data) {
        const ctx = document.getElementById('product-mix-chart').getContext('2d');
        if (productMixChart) productMixChart.destroy();
        productMixChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(data),
                datasets: [{ data: Object.values(data), backgroundColor: ['#0d6efd', '#198754', '#ffc107', '#dc3545', '#6c757d', '#0dcaf0'] }]
            },
            options: { ...CHART_CONFIG, scales: {} }
        });
    }

    // --- Event Listeners ---
    
    filterBtn.addEventListener('click', fetchAndRenderAnalytics);

    document.querySelectorAll('.btn-group .btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const range = e.target.dataset.range;
            const end = new Date();
            let start = new Date();
            if (range === 'today') start.setHours(0, 0, 0, 0);
            if (range === 'week') { start.setDate(end.getDate() - end.getDay()); start.setHours(0, 0, 0, 0); }
            if (range === 'month') { start.setDate(1); start.setHours(0, 0, 0, 0); }
            
            startDateInput.value = start.toISOString().slice(0, 16);
            endDateInput.value = end.toISOString().slice(0, 16);
            fetchAndRenderAnalytics();
        });
    });

    exportBtn.addEventListener('click', () => {
        const params = new URLSearchParams();
        if (startDateInput.value) params.append('start_date', new Date(startDateInput.value).toISOString());
        if (endDateInput.value) params.append('end_date', new Date(endDateInput.value).toISOString());
        if (operatorFilter.value) params.append('operator_id', operatorFilter.value);
        if (productFilter.value) params.append('product_id', productFilter.value);
        window.location.href = `/api/v1/analytics/export-csv?${params.toString()}`;
    });

    // --- Initial Load ---
    
    async function initialize() {
        await populateFilterDropdowns();
        document.querySelector('[data-range="today"]').click(); // Load today's data by default
    }

    initialize();
});