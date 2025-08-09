document.addEventListener("DOMContentLoaded", function () {
    const filterForm = document.getElementById("report-filter-form");
    const resetBtn = document.getElementById("reset-filter-btn");

    // UI elements for the summary card
    const reportPeriodDisplay = document.getElementById("report-period-display");
    const totalRunsEl = document.getElementById("total-runs");
    const totalDetectionsEl = document.getElementById("total-detections");
    const completedRunsEl = document.getElementById("completed-runs");
    const failedRunsEl = document.getElementById("failed-runs");
    const abortedRunsEl = document.getElementById("aborted-runs");
    const loadingState = document.getElementById("report-loading-state");
    const summaryContent = document.getElementById("report-summary-content");

    // UI element for the detailed history table
    const historyTableBody = document.getElementById("report-history-table-body");

    const API_REPORTS_BASE = "/api/v1/reports";
    const API_HISTORY_BASE = "/api/v1/run-history";

    const fetchReportData = async (params = {}) => {
        const urlParams = new URLSearchParams();
        if (params.start_date) urlParams.append('start_date', params.start_date);
        if (params.end_date) urlParams.append('end_date', params.end_date);
        
        // Show loading states for both sections
        loadingState.style.display = 'block';
        summaryContent.style.display = 'none';
        historyTableBody.innerHTML = `<tr><td colspan="7" class="text-center">Generating report...</td></tr>`;

        try {
            // Fetch both summary and detailed history data concurrently
            const [summaryResponse, historyResponse] = await Promise.all([
                fetch(`${API_REPORTS_BASE}/summary?${urlParams}`),
                fetch(`${API_HISTORY_BASE}/?${urlParams}`) // Fetch from the run history endpoint
            ]);

            if (!summaryResponse.ok) throw new Error(`Summary fetch failed! status: ${summaryResponse.status}`);
            if (!historyResponse.ok) throw new Error(`History fetch failed! status: ${historyResponse.status}`);

            const summaryData = await summaryResponse.json();
            const historyData = await historyResponse.json();
            
            // Update both UI sections with the new data
            updateSummaryUI(summaryData); 
            renderHistoryTable(historyData);

        } catch (error) {
            console.error("Failed to fetch report data:", error);
            summaryContent.innerHTML = `<div class="alert alert-danger">Failed to load summary data.</div>`;
            historyTableBody.innerHTML = `<tr><td colspan="7" class="text-center text-danger">Failed to load detailed run data.</td></tr>`;
        } finally {
            // Hide loading state
            loadingState.style.display = 'none';
            summaryContent.style.display = 'block';
        }
    };

    const updateSummaryUI = (data) => {
        if (data && data.summary) {
            totalRunsEl.textContent = data.summary.total_runs_in_period ?? '0';
            totalDetectionsEl.textContent = data.summary.total_items_detected ?? '0';
            completedRunsEl.textContent = data.summary.completed_runs ?? '0';
            failedRunsEl.textContent = data.summary.failed_runs ?? '0';
            abortedRunsEl.textContent = data.summary.aborted_runs ?? '0';
        } else {
            totalRunsEl.textContent = 'N/A';
            totalDetectionsEl.textContent = 'N/A';
            completedRunsEl.textContent = 'N/A';
            failedRunsEl.textContent = 'N/A';
            abortedRunsEl.textContent = 'N/A';
        }
        
        if (data && data.query_parameters) {
            const start = data.query_parameters.start_date;
            const end = data.query_parameters.end_date;
            if (start !== 'Not specified' || end !== 'Not specified') {
                 reportPeriodDisplay.textContent = `(Filtered)`;
            } else {
                 reportPeriodDisplay.textContent = `(All Time)`;
            }
        }
    };

    // THIS IS THE RESTORED FUNCTION: Renders the detailed run log table
    const renderHistoryTable = (runs) => {
        if (!runs || runs.length === 0) {
            historyTableBody.innerHTML = `<tr><td colspan="7" class="text-center">No runs found for the selected period.</td></tr>`;
            return;
        }

        historyTableBody.innerHTML = runs.map(run => `
            <tr>
                <td>${new Date(run.start_timestamp).toLocaleString()}</td>
                <td>${run.end_timestamp ? new Date(run.end_timestamp).toLocaleString() : 'N/A'}</td>
                <td><span class="badge bg-${getStatusColor(run.status)}">${run.status}</span></td>
                <td>${run.batch_code}</td>
                <td>${run.product ? run.product.name : 'N/A'}</td>
                <td>${run.operator ? run.operator.name : 'N/A'}</td>
                <td class="text-end">
                     <a href="/run-history#run-${run.id}" class="btn btn-sm btn-outline-primary" title="View Detections for this Run">
                        <i class="bi bi-images"></i> View
                    </a>
                </td>
            </tr>
        `).join('');
    };

    function getStatusColor(status) {
        switch (status) {
            case 'Completed': return 'success';
            case 'Running': return 'info';
            case 'Aborted by User': return 'warning';
            case 'Failed': return 'danger';
            default: return 'secondary';
        }
    }

    filterForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const startDate = document.getElementById("filter-start-date").value;
        const endDate = document.getElementById("filter-end-date").value;
        
        const params = {};
        if (startDate) params.start_date = new Date(startDate).toISOString();
        if (endDate) params.end_date = new Date(endDate).toISOString();

        fetchReportData(params);
    });
    
    resetBtn.addEventListener("click", () => {
        filterForm.reset();
        fetchReportData();
    });

    // Initial load of data for all time
    fetchReportData();
});