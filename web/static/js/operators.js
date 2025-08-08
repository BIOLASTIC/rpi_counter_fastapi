document.addEventListener('DOMContentLoaded', function () {
    const addOperatorBtn = document.getElementById('add-operator-btn');
    const operatorModal = new bootstrap.Modal(document.getElementById('operator-modal'));
    const operatorForm = document.getElementById('operator-form');
    const modalTitle = document.getElementById('operator-modal-title');
    const tableBody = document.getElementById('operators-table-body');
    let currentOperatorId = null;

    // Fetch and display all operators
    async function loadOperators() {
        try {
            const response = await fetch('/api/v1/operators');
            if (!response.ok) throw new Error('Failed to fetch operators');
            const operators = await response.json();

            tableBody.innerHTML = '';
            if (operators.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="4" class="text-center">No operators found.</td></tr>';
                return;
            }

            operators.forEach(operator => {
                const statusBadge = operator.status === 'Active' ? 'bg-success' : 'bg-secondary';
                const row = `
                    <tr>
                        <td>${operator.name}</td>
                        <td><span class="badge ${statusBadge}">${operator.status}</span></td>
                        <td>${new Date(operator.created_at).toLocaleString()}</td>
                        <td class="text-end">
                            <button class="btn btn-sm btn-outline-primary edit-btn" data-id="${operator.id}"><i class="bi bi-pencil"></i></button>
                            <button class="btn btn-sm btn-outline-danger delete-btn" data-id="${operator.id}"><i class="bi bi-trash"></i></button>
                        </td>
                    </tr>
                `;
                tableBody.insertAdjacentHTML('beforeend', row);
            });
        } catch (error) {
            console.error('Error loading operators:', error);
            tableBody.innerHTML = '<tr><td colspan="4" class="text-center text-danger">Error loading operators.</td></tr>';
        }
    }

    // Show modal for creating
    addOperatorBtn.addEventListener('click', () => {
        currentOperatorId = null;
        modalTitle.textContent = 'Add New Operator';
        operatorForm.reset();
        document.getElementById('operator-id').value = '';
        operatorModal.show();
    });

    // Handle form submission (Create or Update)
    operatorForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const operatorData = {
            name: document.getElementById('operator-name').value,
            status: document.getElementById('operator-status').value,
        };

        const url = currentOperatorId ? `/api/v1/operators/${currentOperatorId}` : '/api/v1/operators';
        const method = currentOperatorId ? 'PUT' : 'POST';

        try {
            const response = await fetch(url, {
                method: method,
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(operatorData),
            });
            if (!response.ok) {
                 const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to save operator');
            }
            operatorModal.hide();
            await loadOperators();
        } catch (error) {
            alert(`Error saving operator: ${error.message}`);
        }
    });
    
    // Handle Edit and Delete buttons
    tableBody.addEventListener('click', async (e) => {
        const target = e.target.closest('button');
        if (!target) return;

        const operatorId = target.dataset.id;
        
        if (target.classList.contains('edit-btn')) {
            try {
                const response = await fetch(`/api/v1/operators/${operatorId}`);
                if (!response.ok) throw new Error('Failed to fetch operator details');
                const operator = await response.json();
                
                currentOperatorId = operator.id;
                modalTitle.textContent = 'Edit Operator';
                document.getElementById('operator-id').value = operator.id;
                document.getElementById('operator-name').value = operator.name;
                document.getElementById('operator-status').value = operator.status;
                operatorModal.show();

            } catch (error) {
                alert(`Error: ${error.message}`);
            }
        }

        if (target.classList.contains('delete-btn')) {
            if (confirm('Are you sure you want to delete this operator?')) {
                try {
                    const response = await fetch(`/api/v1/operators/${operatorId}`, { method: 'DELETE' });
                     if (!response.ok) {
                         const errorData = await response.json();
                         throw new Error(errorData.detail || 'Failed to delete operator');
                    }
                    await loadOperators();
                } catch (error) {
                    alert(`Error deleting operator: ${error.message}`);
                }
            }
        }
    });

    // Initial load
    loadOperators();
});