// rpi_counter_fastapi-apinaudio/web/static/js/analytics.js

document.addEventListener('DOMContentLoaded', function () {
    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    const operatorFilter = document.getElementById('operator-filter');
    const productFilter = document.getElementById('product-filter');
    const filterBtn = document.getElementById('filter-btn');
    const exportBtn = document.getElementById('export-btn');
    const loader = document.getElementById('loader');
    const content = document.getElementById('analytics-content');

    let charts = {};

    function showLoader() {
        loader.style.display = 'block';
        content.style.visibility = 'hidden';
    }

    function hideLoader() {
        loader.style.display = 'none';
        content.style.visibility = 'visible';
    }

    function createChart(ctx, type, data, options) {
        const chartId = ctx.canvas.id;
        if (charts[chartId]) {
            charts[chartId].destroy();
        }
        charts[chartId] = new Chart(ctx, { type, data, options });
    }

    async function fetchFilterOptions() {
        try {
            const [operatorsRes, productsRes] = await Promise.all([
                fetch('/api/v1/operators/'),
                fetch('/api/v1/products/')
            ]);
            const operators = await operatorsRes.json();
            const products = await productsRes.json();

            operators.forEach(op => {
                const option = document.createElement('option');
                option.value = op.id;
                option.textContent = op.name;
                operatorFilter.appendChild(option);
            });

            products.forEach(p => {
                const option = document.createElement('option');
                option.value = p.id;
                option.textContent = p.name;
                productFilter.appendChild(option);
            });
        } catch (error) {
            console.error('Failed to load filter options:', error);
        }
    }

    async function fetchAnalyticsData() {
        showLoader();
        const params = new URLSearchParams();
        if (startDateInput.value) params.append('start_date', new Date(startDateInput.value).toISOString());
        if (endDateInput.value) params.append('end_date', new Date(endDateInput.value).toISOString());
        if (operatorFilter.value) params.append('operator_id', operatorFilter.value);
        if (productFilter.value) params.append('product_id', productFilter.value);

        try {
            const response = await fetch(`/api/v1/analytics/summary?${params.toString()}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            const data = await response.json();
            updateDashboard(data);
        } catch (error) {
            console.error('Error fetching analytics data:', error);
            content.innerHTML = `<div class="alert alert-danger">Failed to load analytics data. Please try again.</div>`;
        } finally {
            hideLoader();
        }
    }
    
    function updateDashboard(data) {
        // KPIs
        document.getElementById('kpi-total-items').textContent = data.kpis.total_items_detected.toLocaleString();
        document.getElementById('kpi-total-runs').textContent = data.kpis.total_runs.toLocaleString();
        document.getElementById('kpi-completed-runs').textContent = data.kpis.completed_runs.toLocaleString();
        document.getElementById('kpi-failed-runs').textContent = data.kpis.failed_runs.toLocaleString();
        document.getElementById('kpi-aborted-runs').textContent = data.kpis.aborted_runs.toLocaleString();
        document.getElementById('kpi-pass-rate').textContent = `${data.kpis.quality_pass_rate.toFixed(1)}%`;

        // OEE-Lite
        document.getElementById('oee-availability').textContent = `${data.oee_lite.availability.toFixed(1)}%`;
        document.getElementById('oee-performance').textContent = data.oee_lite.performance_items_per_hour.toFixed(0);
        
        // Downtime Chart
        const downtimeCtx = document.getElementById('downtime-chart').getContext('2d');
        createChart(downtimeCtx, 'doughnut', {
            labels: ['Planned Changeover (hrs)', 'Unplanned Downtime (hrs)'],
            datasets: [{
                data: [data.downtime.planned_changeover_hours, data.downtime.unplanned_downtime_hours],
                backgroundColor: ['#ffc107', '#dc3545']
            }]
        }, { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'top' } } });
        
        // Daily Trend Chart
        const dailyTrendCtx = document.getElementById('daily-trend-chart').getContext('2d');
        const trendLabels = Object.keys(data.daily_trends);
        createChart(dailyTrendCtx, 'bar', {
            labels: trendLabels,
            datasets: [
                { label: 'Items Passed', data: trendLabels.map(d => data.daily_trends[d].pass), backgroundColor: 'rgba(25, 135, 84, 0.7)' },
                { label: 'Items Failed', data: trendLabels.map(d => data.daily_trends[d].fail), backgroundColor: 'rgba(220, 53, 69, 0.7)' }
            ]
        }, { responsive: true, maintainAspectRatio: false, scales: { x: { stacked: true }, y: { stacked: true, beginAtZero: true } } });

        // Hourly Chart
        const hourlyCtx = document.getElementById('hourly-chart').getContext('2d');
        createChart(hourlyCtx, 'bar', {
            labels: Object.keys(data.hourly_throughput),
            datasets: [{
                label: 'Items per Hour',
                data: Object.values(data.hourly_throughput),
                backgroundColor: 'rgba(13, 110, 253, 0.7)'
            }]
        }, { responsive: true, maintainAspectRatio: false, scales: { y: { beginAtZero: true } } });
        
        // Product Mix Chart
        const productMixCtx = document.getElementById('product-mix-chart').getContext('2d');
        createChart(productMixCtx, 'pie', {
            labels: data.top_5_products.map(p => p[0]),
            datasets: [{
                data: data.top_5_products.map(p => p[1]),
                backgroundColor: ['#0d6efd', '#6c757d', '#198754', '#ffc107', '#dc3545']
            }]
        }, { responsive: true, maintainAspectRatio: false });
        
        // Top Products Table
        const topProductsTable = document.getElementById('top-products-table').querySelector('tbody');
        topProductsTable.innerHTML = data.top_5_products.map(p => `<tr><td>${p[0]}</td><td class="text-end">${p[1].toLocaleString()}</td></tr>`).join('') || '<tr><td colspan="2" class="text-center">No data available</td></tr>';
        
        // Top Defects Table
        const topDefectsTable = document.getElementById('top-defects-table').querySelector('tbody');
        topDefectsTable.innerHTML = data.quality_control.top_5_defects.map(d => `<tr><td>${d[0]}</td><td class="text-end">${d[1].toLocaleString()}</td></tr>`).join('') || '<tr><td colspan="2" class="text-center">No data available</td></tr>';
    }

    function setQuickFilter(range) {
        const timeZone = 'Asia/Kolkata';
        const nowInLocalTZ = new Date(new Date().toLocaleString('en-US', { timeZone }));
        
        let start = new Date(nowInLocalTZ);
        const end = new Date(nowInLocalTZ);

        if (range === 'today') {
            start.setHours(0, 0, 0, 0);
        } else if (range === 'week') {
            const dayOfWeek = start.getDay();
            const diff = start.getDate() - dayOfWeek + (dayOfWeek === 0 ? -6 : 1); // Adjust to Monday
            start.setDate(diff);
            start.setHours(0, 0, 0, 0);
        } else if (range === 'month') {
            start.setDate(1);
            start.setHours(0, 0, 0, 0);
        }
        
        // Helper to format date for <input type="datetime-local">
        const toLocalISOString = (date) => {
            const pad = (num) => (num < 10 ? '0' : '') + num;
            return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}T${pad(date.getHours())}:${pad(date.getMinutes())}`;
        };

        startDateInput.value = toLocalISOString(start);
        endDateInput.value = toLocalISOString(end);
        
        fetchAnalyticsData();
    }

    filterBtn.addEventListener('click', fetchAnalyticsData);
    document.querySelectorAll('.btn-group .btn').forEach(button => {
        button.addEventListener('click', (e) => setQuickFilter(e.target.dataset.range));
    });

    exportBtn.addEventListener('click', () => {
        const params = new URLSearchParams();
        if (startDateInput.value) params.append('start_date', new Date(startDateInput.value).toISOString());
        if (endDateInput.value) params.append('end_date', new Date(endDateInput.value).toISOString());
        if (operatorFilter.value) params.append('operator_id', operatorFilter.value);
        if (productFilter.value) params.append('product_id', productFilter.value);
        window.location.href = `/api/v1/analytics/export-csv?${params.toString()}`;
    });

    // Initialize the page
    fetchFilterOptions().then(() => {
        setQuickFilter('today'); // Default to "Today" in Asia/Kolkata
    });
});