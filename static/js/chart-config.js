function initializePurchaseChart(purchaseData) {
    const ctx = document.getElementById('purchaseChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: purchaseData.dates,
            datasets: [{
                label: 'Purchase Amount ($)',
                data: purchaseData.amounts,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 2,
                tension: 0.1,
                fill: true
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value;
                        }
                    }
                }
            }
        }
    });
}