document.addEventListener("DOMContentLoaded", function() {
    // Initialize chart if the chart canvas exists
    const chartCanvas = document.getElementById("priceChart");
    if (chartCanvas) {
        const ctx = chartCanvas.getContext("2d");
        new Chart(ctx, {
            type: "line",
            data: {
                labels: ["March 1", "March 2", "March 3", "March 4", "March 5"],
                datasets: [{
                    label: "Current Price",
                    data: [25, 30, 28, 32, 29],
                    borderColor: "#ff79c6",
                    backgroundColor: "rgba(255, 121, 198, 0.1)",
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                }, {
                    label: "Suggested Price",
                    data: [26.5, 31.2, 29.5, 33.5, 30.8],
                    borderColor: "#8a65ff",
                    backgroundColor: "rgba(138, 101, 255, 0.1)",
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: "#fff",
                            font: {
                                size: 14
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: "#29293d",
                        titleColor: "#ff79c6",
                        bodyColor: "#fff",
                        borderColor: "#444",
                        borderWidth: 1
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: "rgba(255, 255, 255, 0.1)"
                        },
                        ticks: {
                            color: "#ccc"
                        }
                    },
                    y: {
                        grid: {
                            color: "rgba(255, 255, 255, 0.1)"
                        },
                        ticks: {
                            color: "#ccc"
                        },
                        suggestedMin: 20,
                        suggestedMax: 40
                    }
                }
            }
        });
    }

    // Add active class to current navigation item
    const path = window.location.pathname;
    const navItems = document.querySelectorAll('nav ul li');
    
    navItems.forEach(item => item.classList.remove('active'));
    if (path.includes('/form/') || path.includes('/suggestion_result/')) {
        navItems[0].classList.add('active');
    } else if (path.includes('/history/')) {
        navItems[1].classList.add('active');
    }
});

function downloadReport() {
    alert("Report Downloaded!");
}