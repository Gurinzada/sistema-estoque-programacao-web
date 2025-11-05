
document.addEventListener('DOMContentLoaded', () => {
    const elements = {
        lowStockCount: document.getElementById('low-stock-count'),
        totalItemsCount: document.getElementById('total-items-count'),
        profitCount: document.getElementById('profit-count'),
        stockBarChartCtx: document.getElementById('stockBarChart')?.getContext('2d'),
        categoryDonutChartCtx: document.getElementById('categoryDonutChart')?.getContext('2d'),
        movementDonutChartCtx: document.getElementById('movementDonutChart')?.getContext('2d'),
        logoutButton: document.getElementById('logout-btn')
    };

    const LOW_STOCK_THRESHOLD = 10;

    async function checkAuthentication() {
        try {
            const token = localStorage.getItem('token');
            if (!token) {
                throw new Error('Não autenticado');
            }
            const response = await fetch('/api/me', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            }); 

            if (!response.ok) {
                throw new Error('Não autenticado');
            }
            
            console.log('Autenticação OK. Carregando dashboard...');
            await initDashboard();

            document.body.classList.remove('hidden');

        } catch (error) {
            console.error('Falha na autenticação:', error.message);
            window.location.href = '/'; 
        }
    }

    async function initDashboard() {
        try {
            const [products, categoryData, profitData, movementData] = await Promise.all([
                fetchData('/api/products', "GET"),
                fetchData('/api/products/count', "GET"),
                fetchData('/api/stock/profit', "GET"),
                fetchData('/api/stock/out-and-in', "GET")
            ]);

            updateStatCards(products, profitData);
            createStockBarChart(products);
            createCategoryDonutChart(categoryData);
            createMovementDonutChart(movementData);

        } catch (error) {
            console.error('Erro ao carregar dados do dashboard:', error);
            alert('Não foi possível carregar os dados do dashboard.');
        }

        if (elements.logoutButton) {
            elements.logoutButton.addEventListener('click', (e) => {
                e.preventDefault();
                console.log('Logout...');
                localStorage.removeItem('token');
                localStorage.removeItem('refresh');
                window.location.href = '/';
            });
        }
    }

    async function fetchData(endpoint, method = "GET") {
        const token = localStorage.getItem("token")
        const response = await fetch(endpoint, {
            headers: {
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            },
            method: method
        });
        if (!response.ok) {
            throw new Error(`Falha ao buscar ${endpoint}: ${response.statusText}`);
        }
        return response.json();
    }

    function updateStatCards(products, profitData) {
        if (!products || !profitData) return;

        const lowStockProducts = products.filter(p => p.quatityStock < LOW_STOCK_THRESHOLD);
        elements.lowStockCount.textContent = lowStockProducts.length;

        const totalItems = products.reduce((sum, p) => sum + p.quatityStock, 0);
        elements.totalItemsCount.textContent = totalItems;

        const profit = profitData.profit || 0;
        elements.profitCount.textContent = `R$ ${profit.toFixed(2)}`;
    }

    function createStockBarChart(products) {
        if (!products || !elements.stockBarChartCtx) return;

        const sortedProducts = [...products]
            .sort((a, b) => b.quatityStock - a.quatityStock)
            .slice(0, 6);

        new Chart(elements.stockBarChartCtx, {
            type: 'bar',
            data: {
                labels: sortedProducts.map(p => p.name),
                datasets: [{
                    label: 'Quantidade em Estoque',
                    data: sortedProducts.map(p => p.quatityStock),
                    backgroundColor: '#00BFFF',
                    borderRadius: 4,
                }]
            },
            options: chartOptions(false)
        });
    }

    function createCategoryDonutChart(categoryData) {
        if (!categoryData || !elements.categoryDonutChartCtx) return;

        new Chart(elements.categoryDonutChartCtx, {
            type: 'doughnut',
            data: {
                labels: Object.keys(categoryData),
                datasets: [{
                    data: Object.values(categoryData),
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
                }]
            },
            options: chartOptions(true)
        });
    }

    function createMovementDonutChart(movementData) {
        if (!movementData || !elements.movementDonutChartCtx) return;

        new Chart(elements.movementDonutChartCtx, {
            type: 'doughnut',
            data: {
                labels: ['Entrada', 'Saída'],
                datasets: [{
                    data: [movementData.total_in, movementData.total_out],
                    backgroundColor: ['#2ECC71', '#E74C3C'],
                }]
            },
            options: chartOptions(true) 
        });
    }

    function chartOptions(showLegend = true) {
        return {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: showLegend,
                    position: 'bottom',
                    labels: {
                        font: { family: "'Poppins', sans-serif" }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { font: { family: "'Poppins', sans-serif" } }
                },
                x: {
                    ticks: { font: { family: "'Poppins', sans-serif" } }
                }
            }
        };
    }

    checkAuthentication();
});