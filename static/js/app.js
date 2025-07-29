// UPI Expense Tracker JavaScript Application

class ExpenseTracker {
    constructor() {
        this.currentPage = 1;
        this.currentFilters = {};
        this.charts = {};
        this.init();
    }

    init() {
        this.bindEvents();
        this.showSection('dashboard');
        this.loadDashboard();
        this.loadCategories();
    }

    bindEvents() {
        // SMS form submission
        document.getElementById('sms-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.parseSMS();
        });

        // Bulk import form submission
        document.getElementById('bulk-import-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.bulkImport();
        });

        // Filter changes
        document.getElementById('type-filter').addEventListener('change', () => {
            this.applyFilters();
        });

        document.getElementById('category-filter').addEventListener('change', () => {
            this.applyFilters();
        });
    }

    showSection(sectionId) {
        // Hide all sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.style.display = 'none';
        });

        // Show selected section
        document.getElementById(sectionId).style.display = 'block';

        // Update navigation
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });

        // Load section-specific data
        switch(sectionId) {
            case 'dashboard':
                this.loadDashboard();
                break;
            case 'transactions':
                this.loadTransactions();
                break;
        }
    }

    async parseSMS() {
        const smsText = document.getElementById('sms-text').value.trim();
        
        if (!smsText) {
            this.showError('Please enter SMS text');
            return;
        }

        try {
            this.showLoading('Parsing SMS...');
            
            const response = await fetch('/api/parse-sms', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ sms_text: smsText })
            });

            const result = await response.json();
            this.hideLoading();

            if (result.success) {
                this.showParseResult(result.transaction);
                document.getElementById('sms-text').value = '';
                // Refresh dashboard if it's visible
                if (document.getElementById('dashboard').style.display !== 'none') {
                    this.loadDashboard();
                }
            } else {
                this.showError(result.error || 'Failed to parse SMS');
            }
        } catch (error) {
            this.hideLoading();
            this.showError('Network error: ' + error.message);
        }
    }

    async bulkImport() {
        const bulkText = document.getElementById('bulk-sms-text').value.trim();
        
        if (!bulkText) {
            this.showError('Please enter SMS messages');
            return;
        }

        const messages = bulkText.split('\n').filter(msg => msg.trim());
        
        if (messages.length === 0) {
            this.showError('No valid messages found');
            return;
        }

        try {
            this.showLoading('Importing messages...');
            
            const response = await fetch('/api/bulk-import', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ messages: messages })
            });

            const result = await response.json();
            this.hideLoading();

            if (result.success) {
                this.showBulkResult(result);
                document.getElementById('bulk-sms-text').value = '';
                // Refresh dashboard
                this.loadDashboard();
            } else {
                this.showError(result.error || 'Failed to import messages');
            }
        } catch (error) {
            this.hideLoading();
            this.showError('Network error: ' + error.message);
        }
    }

    async loadDashboard() {
        try {
            const [analyticsResponse, transactionsResponse] = await Promise.all([
                fetch('/api/analytics'),
                fetch('/api/transactions?per_page=1000')
            ]);

            const analytics = await analyticsResponse.json();
            const transactions = await transactionsResponse.json();

            this.updateSummaryCards(transactions.transactions);
            this.updateCharts(analytics);
            this.updateTopMerchants(analytics.top_merchants);
        } catch (error) {
            console.error('Error loading dashboard:', error);
        }
    }

    updateSummaryCards(transactions) {
        const totalSpent = transactions
            .filter(t => t.transaction_type === 'debit')
            .reduce((sum, t) => sum + t.amount, 0);

        const totalReceived = transactions
            .filter(t => t.transaction_type === 'credit')
            .reduce((sum, t) => sum + t.amount, 0);

        const currentMonth = new Date().toISOString().substring(0, 7);
        const thisMonth = transactions
            .filter(t => t.transaction_type === 'debit' && t.date.startsWith(currentMonth))
            .reduce((sum, t) => sum + t.amount, 0);

        document.getElementById('total-spent').textContent = `₹${totalSpent.toLocaleString('en-IN')}`;
        document.getElementById('total-received').textContent = `₹${totalReceived.toLocaleString('en-IN')}`;
        document.getElementById('this-month').textContent = `₹${thisMonth.toLocaleString('en-IN')}`;
        document.getElementById('total-transactions').textContent = transactions.length;
    }

    updateCharts(analytics) {
        this.updateMonthlyChart(analytics.monthly_spending);
        this.updateCategoryChart(analytics.category_spending);
    }

    updateMonthlyChart(monthlyData) {
        const ctx = document.getElementById('monthlyChart').getContext('2d');
        
        if (this.charts.monthly) {
            this.charts.monthly.destroy();
        }

        this.charts.monthly = new Chart(ctx, {
            type: 'line',
            data: {
                labels: monthlyData.map(d => d.month),
                datasets: [{
                    label: 'Monthly Spending',
                    data: monthlyData.map(d => d.amount),
                    borderColor: '#007bff',
                    backgroundColor: 'rgba(0, 123, 255, 0.1)',
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            callback: function(value) {
                                return '₹' + value.toLocaleString('en-IN');
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return 'Amount: ₹' + context.parsed.y.toLocaleString('en-IN');
                            }
                        }
                    }
                }
            }
        });
    }

    updateCategoryChart(categoryData) {
        const ctx = document.getElementById('categoryChart').getContext('2d');
        
        if (this.charts.category) {
            this.charts.category.destroy();
        }

        const colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
            '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
        ];

        this.charts.category = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: categoryData.map(d => d.category),
                datasets: [{
                    data: categoryData.map(d => d.amount),
                    backgroundColor: colors.slice(0, categoryData.length),
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.label + ': ₹' + context.parsed.toLocaleString('en-IN');
                            }
                        }
                    }
                }
            }
        });
    }

    updateTopMerchants(merchants) {
        const container = document.getElementById('top-merchants');
        container.innerHTML = '';

        merchants.slice(0, 6).forEach(merchant => {
            const col = document.createElement('div');
            col.className = 'col-md-4 col-sm-6 mb-3';
            
            col.innerHTML = `
                <div class="merchant-card">
                    <div class="merchant-name">${merchant.merchant}</div>
                    <div class="merchant-amount">₹${merchant.amount.toLocaleString('en-IN')}</div>
                </div>
            `;
            
            container.appendChild(col);
        });
    }

    async loadTransactions(page = 1) {
        try {
            const params = new URLSearchParams({
                page: page,
                per_page: 20,
                ...this.currentFilters
            });

            const response = await fetch(`/api/transactions?${params}`);
            const data = await response.json();

            this.renderTransactions(data.transactions);
            this.renderPagination(data.current_page, data.pages);
        } catch (error) {
            console.error('Error loading transactions:', error);
        }
    }

    renderTransactions(transactions) {
        const tbody = document.getElementById('transactions-table');
        tbody.innerHTML = '';

        transactions.forEach(transaction => {
            const row = document.createElement('tr');
            row.className = 'transaction-row';
            row.onclick = () => this.showTransactionDetails(transaction);

            const amountClass = transaction.transaction_type === 'debit' ? 'amount-debit' : 'amount-credit';
            const amountPrefix = transaction.transaction_type === 'debit' ? '-' : '+';

            row.innerHTML = `
                <td>${new Date(transaction.date).toLocaleDateString('en-IN')}</td>
                <td>
                    <span class="badge ${transaction.transaction_type === 'debit' ? 'bg-danger' : 'bg-success'}">
                        ${transaction.transaction_type.toUpperCase()}
                    </span>
                </td>
                <td class="${amountClass}">${amountPrefix}₹${transaction.amount.toLocaleString('en-IN')}</td>
                <td>${transaction.merchant || 'Unknown'}</td>
                <td>
                    <span class="badge bg-secondary category-badge">
                        ${transaction.category || 'Uncategorized'}
                    </span>
                </td>
                <td>${transaction.bank || 'Unknown'}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary" onclick="event.stopPropagation(); expenseTracker.showTransactionDetails(${JSON.stringify(transaction).replace(/"/g, '&quot;')})">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            `;

            tbody.appendChild(row);
        });
    }

    renderPagination(currentPage, totalPages) {
        const pagination = document.getElementById('pagination');
        pagination.innerHTML = '';

        if (totalPages <= 1) return;

        // Previous button
        const prevLi = document.createElement('li');
        prevLi.className = `page-item ${currentPage === 1 ? 'disabled' : ''}`;
        prevLi.innerHTML = `<a class="page-link" href="#" onclick="expenseTracker.loadTransactions(${currentPage - 1})">Previous</a>`;
        pagination.appendChild(prevLi);

        // Page numbers
        const startPage = Math.max(1, currentPage - 2);
        const endPage = Math.min(totalPages, currentPage + 2);

        for (let i = startPage; i <= endPage; i++) {
            const li = document.createElement('li');
            li.className = `page-item ${i === currentPage ? 'active' : ''}`;
            li.innerHTML = `<a class="page-link" href="#" onclick="expenseTracker.loadTransactions(${i})">${i}</a>`;
            pagination.appendChild(li);
        }

        // Next button
        const nextLi = document.createElement('li');
        nextLi.className = `page-item ${currentPage === totalPages ? 'disabled' : ''}`;
        nextLi.innerHTML = `<a class="page-link" href="#" onclick="expenseTracker.loadTransactions(${currentPage + 1})">Next</a>`;
        pagination.appendChild(nextLi);
    }

    async loadCategories() {
        try {
            const response = await fetch('/api/transactions');
            const data = await response.json();
            
            const categories = [...new Set(data.transactions.map(t => t.category))].filter(Boolean);
            const categoryFilter = document.getElementById('category-filter');
            
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category;
                option.textContent = category;
                categoryFilter.appendChild(option);
            });
        } catch (error) {
            console.error('Error loading categories:', error);
        }
    }

    applyFilters() {
        const typeFilter = document.getElementById('type-filter').value;
        const categoryFilter = document.getElementById('category-filter').value;

        this.currentFilters = {};
        if (typeFilter) this.currentFilters.type = typeFilter;
        if (categoryFilter) this.currentFilters.category = categoryFilter;

        this.loadTransactions(1);
    }

    showTransactionDetails(transaction) {
        const modal = new bootstrap.Modal(document.getElementById('transactionModal'));
        const detailsDiv = document.getElementById('transaction-details');

        detailsDiv.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <strong>Amount:</strong><br>
                    <span class="${transaction.transaction_type === 'debit' ? 'text-danger' : 'text-success'}">
                        ${transaction.transaction_type === 'debit' ? '-' : '+'}₹${transaction.amount.toLocaleString('en-IN')}
                    </span>
                </div>
                <div class="col-md-6">
                    <strong>Date:</strong><br>
                    ${new Date(transaction.date).toLocaleString('en-IN')}
                </div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-6">
                    <strong>Merchant:</strong><br>
                    ${transaction.merchant || 'Unknown'}
                </div>
                <div class="col-md-6">
                    <strong>Category:</strong><br>
                    <span class="badge bg-secondary">${transaction.category || 'Uncategorized'}</span>
                </div>
            </div>
            <hr>
            <div class="row">
                <div class="col-md-6">
                    <strong>Bank:</strong><br>
                    ${transaction.bank || 'Unknown'}
                </div>
                <div class="col-md-6">
                    <strong>Account:</strong><br>
                    ${transaction.account_number || 'N/A'}
                </div>
            </div>
            ${transaction.balance ? `
            <hr>
            <div class="row">
                <div class="col-12">
                    <strong>Balance after transaction:</strong><br>
                    ₹${transaction.balance.toLocaleString('en-IN')}
                </div>
            </div>
            ` : ''}
            <hr>
            <div class="row">
                <div class="col-12">
                    <strong>Original SMS:</strong><br>
                    <div class="bg-light p-2 rounded mt-1" style="font-size: 0.9rem;">
                        ${transaction.raw_message || transaction.description}
                    </div>
                </div>
            </div>
        `;

        modal.show();
    }

    showParseResult(transaction) {
        const resultDiv = document.getElementById('parse-result');
        const detailsDiv = document.getElementById('parsed-details');

        detailsDiv.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <strong>Amount:</strong> 
                    <span class="${transaction.transaction_type === 'debit' ? 'text-danger' : 'text-success'}">
                        ${transaction.transaction_type === 'debit' ? '-' : '+'}₹${transaction.amount.toLocaleString('en-IN')}
                    </span>
                </div>
                <div class="col-md-6">
                    <strong>Merchant:</strong> ${transaction.merchant || 'Unknown'}
                </div>
            </div>
            <div class="row mt-2">
                <div class="col-md-6">
                    <strong>Category:</strong> 
                    <span class="badge bg-secondary">${transaction.category || 'Uncategorized'}</span>
                </div>
                <div class="col-md-6">
                    <strong>Bank:</strong> ${transaction.bank || 'Unknown'}
                </div>
            </div>
        `;

        resultDiv.style.display = 'block';
        document.getElementById('parse-error').style.display = 'none';

        setTimeout(() => {
            resultDiv.style.display = 'none';
        }, 5000);
    }

    showBulkResult(result) {
        const resultDiv = document.getElementById('bulk-result');
        const detailsDiv = document.getElementById('bulk-details');

        detailsDiv.innerHTML = `
            <div class="row">
                <div class="col-md-4">
                    <strong>Successful:</strong> <span class="text-success">${result.successful}</span>
                </div>
                <div class="col-md-4">
                    <strong>Failed:</strong> <span class="text-danger">${result.failed}</span>
                </div>
                <div class="col-md-4">
                    <strong>Total:</strong> ${result.successful + result.failed}
                </div>
            </div>
            ${result.errors && result.errors.length > 0 ? `
            <div class="mt-2">
                <strong>Errors:</strong>
                <ul class="mt-1">
                    ${result.errors.map(error => `<li class="text-danger small">${error}</li>`).join('')}
                </ul>
            </div>
            ` : ''}
        `;

        resultDiv.style.display = 'block';

        setTimeout(() => {
            resultDiv.style.display = 'none';
        }, 10000);
    }

    showError(message) {
        const errorDiv = document.getElementById('parse-error');
        const detailsDiv = document.getElementById('error-details');
        
        detailsDiv.textContent = message;
        errorDiv.style.display = 'block';
        document.getElementById('parse-result').style.display = 'none';

        setTimeout(() => {
            errorDiv.style.display = 'none';
        }, 5000);
    }

    showLoading(message) {
        // You can implement a loading indicator here
        console.log(message);
    }

    hideLoading() {
        // You can hide the loading indicator here
        console.log('Loading complete');
    }
}

// Global functions for onclick handlers
function showSection(sectionId) {
    expenseTracker.showSection(sectionId);
}

// Initialize the application
const expenseTracker = new ExpenseTracker();