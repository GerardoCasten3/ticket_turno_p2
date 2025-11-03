// static/js/dashboard/barNiv.js

let barChartNiv = null;

const barColorsNiv = [
    'rgba(54, 162, 235, 0.7)',
    'rgba(255, 99, 132, 0.7)',
    'rgba(75, 192, 192, 0.7)',
    'rgba(255, 159, 64, 0.7)',
    'rgba(153, 102, 255, 0.7)',
    'rgba(255, 205, 86, 0.7)',
    'rgba(201, 203, 207, 0.7)',
];

const borderColorsNiv = [
    'rgb(54, 162, 235)',
    'rgb(255, 99, 132)',
    'rgb(75, 192, 192)',
    'rgb(255, 159, 64)',
    'rgb(153, 102, 255)',
    'rgb(255, 205, 86)',
    'rgb(201, 203, 207)',
];

async function loadBarChartNiv() {
    try {
        const response = await fetch('/admin/dashboard/nivel-data/');
        
        if (!response.ok) {
            throw new Error('Error al obtener los datos');
        }
        
        const apiData = await response.json();
        
        const ctx = document.getElementById('barChart2');
        
        if (!ctx) {
            console.error('Canvas barChart2 no encontrado');
            return;
        }
        
        if (barChartNiv) {
            barChartNiv.destroy();
        }
        
        const backgroundColors = apiData.labels.map((_, index) => 
            barColorsNiv[index % barColorsNiv.length]
        );
        const borderColorsArray = apiData.labels.map((_, index) => 
            borderColorsNiv[index % borderColorsNiv.length]
        );
        
        const data = {
            labels: apiData.labels,
            datasets: [{
                label: 'Citas',
                data: apiData.data,
                backgroundColor: backgroundColors,
                borderColor: borderColorsArray,
                borderWidth: 2
            }]
        };
        
        const config = {
            type: 'bar',  // ✅ Cambiar a 'horizontalBar' si usas Chart.js 2.x, o usar indexAxis
            data: data,
            options: {
                indexAxis: 'y',  // ✅ Esto hace la gráfica horizontal
                responsive: true,
                maintainAspectRatio: false,  // ✅ Cambié a false para mejor control
                scales: {
                    x: {  // ✅ Ahora X es el valor numérico
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,
                            precision: 0
                        },
                        title: {
                            display: false
                        }
                    },
                    y: {  // ✅ Ahora Y son las etiquetas
                        title: {
                            display: false
                        },
                        ticks: {
                            autoSkip: false,
                            font: {
                                size: 11  // ✅ Texto más pequeño
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false  // ✅ Ocultar leyenda para ahorrar espacio
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.parsed.x + ' citas';
                            }
                        }
                    }
                }
            }
        };
        
        barChartNiv = new Chart(ctx, config);
        
        console.log('Gráfica de nivel educativo cargada exitosamente');
        
    } catch (error) {
        console.error('Error al cargar la gráfica de nivel:', error);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        loadBarChartNiv();
    }, 250);
});

function refreshBarChartNiv() {
    loadBarChartNiv();
}