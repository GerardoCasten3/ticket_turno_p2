// static/js/dashboard/bar.js

let barChart = null;

// Colores para las barras (puedes personalizarlos)
const barColors = [
    'rgba(54, 162, 235, 0.7)',   // Azul
    'rgba(255, 99, 132, 0.7)',   // Rojo
    'rgba(75, 192, 192, 0.7)',   // Verde agua
    'rgba(255, 159, 64, 0.7)',   // Naranja
    'rgba(153, 102, 255, 0.7)',  // Morado
    'rgba(255, 205, 86, 0.7)',   // Amarillo
    'rgba(201, 203, 207, 0.7)',  // Gris
];

const borderColors = [
    'rgb(54, 162, 235)',
    'rgb(255, 99, 132)',
    'rgb(75, 192, 192)',
    'rgb(255, 159, 64)',
    'rgb(153, 102, 255)',
    'rgb(255, 205, 86)',
    'rgb(201, 203, 207)',
];

// Función para cargar los datos de la gráfica de barras
async function loadBarChart() {
    try {
        // Llamada a tu API de municipios
        const response = await fetch('/admin/dashboard/municipios-data/');
        
        if (!response.ok) {
            throw new Error('Error al obtener los datos');
        }
        
        const apiData = await response.json();
        
        const ctx = document.getElementById('barChart');
        
        if (!ctx) {
            console.error('Canvas barChart no encontrado');
            return;
        }
        
        // Si ya existe una gráfica, destrúyela antes de crear una nueva
        if (barChart) {
            barChart.destroy();
        }
        
        // Generar colores dinámicamente basados en la cantidad de municipios
        const backgroundColors = apiData.labels.map((_, index) => 
            barColors[index % barColors.length]
        );
        const borderColorsArray = apiData.labels.map((_, index) => 
            borderColors[index % borderColors.length]
        );
        
        // Usar los datos de la API
        const data = {
            labels: apiData.labels,  // Nombres de municipios
            datasets: [{
                label: 'Citas por Municipio',
                data: apiData.data,  // Cantidad de citas
                backgroundColor: backgroundColors,
                borderColor: borderColorsArray,
                borderWidth: 2
            }]
        };
        
        // Configuración de la gráfica
        const config = {
            type: 'bar',
            data: data,
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1,  // Para mostrar solo números enteros
                            precision: 0
                        },
                        title: {
                            display: true,
                            text: 'Número de Citas'
                        }
                    },
                    x: {
                        title: {
                            display: true,
                            text: 'Municipios'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                return context.dataset.label + ': ' + context.parsed.y + ' citas';
                            }
                        }
                    }
                }
            }
        };
        
        // Crear la gráfica
        barChart = new Chart(ctx, config);
        
        console.log('Gráfica de barras cargada exitosamente');
        console.log('Municipios:', apiData.labels);
        console.log('Datos:', apiData.data);
        
    } catch (error) {
        console.error('Error al cargar la gráfica de barras:', error);
    }
}

// Cargar la gráfica cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        loadBarChart();
    }, 150);
    
    // Auto-actualizar cada 60 segundos (opcional)
    // setInterval(loadBarChart, 60000);
});

// Función para actualizar manualmente
function refreshBarChart() {
    loadBarChart();
}