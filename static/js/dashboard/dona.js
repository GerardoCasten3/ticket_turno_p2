// static/js/dashboard/dona.js

let donutChart = null;

// Configuración de colores para la gráfica
const chartColors = [
    '#FF6384',
    '#36A2EB',
    '#FFCE56',
    '#4BC0C0',
    '#9966FF',
    '#FF9F40',
    '#E7E9ED',
    '#FFA1B5'
];

// Función para cargar los datos y crear/actualizar la gráfica
async function loadDonutChart() {
    try {
        const response = await fetch('/admin/dashboard/asuntos-data/');
        const data = await response.json();
        
        const ctx = document.getElementById('donutChart');
        
        if (!ctx) {
            console.error('Canvas donutChart no encontrado');
            return;
        }
        
        // Si ya existe una gráfica, destrúyela antes de crear una nueva
        if (donutChart) {
            donutChart.destroy();
        }
        
        // Crea la gráfica de dona
        donutChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Citas por Asunto',
                    data: data.data,
                    backgroundColor: chartColors,
                    borderColor: '#fff',
                    borderWidth: 2
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 10,
                            font: {
                                size: 11
                            },
                            boxWidth: 15
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                let label = context.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                label += context.parsed + ' citas';
                                
                                // Calcular porcentaje
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = ((context.parsed / total) * 100).toFixed(1);
                                label += ` (${percentage}%)`;
                                
                                return label;
                            }
                        }
                    }
                }
            }
        });
        
        console.log('Gráfica de dona cargada exitosamente');
        
    } catch (error) {
        console.error('Error al cargar los datos de asuntos:', error);
    }
}

// Cargar la gráfica cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Pequeño delay para asegurar que todo esté renderizado
    setTimeout(() => {
        loadDonutChart();
    }, 100);
    
    // Actualizar cada 30 segundos (opcional)
    // setInterval(loadDonutChart, 30000);
});

// Función para actualizar manualmente
function refreshDonutChart() {
    loadDonutChart();
}