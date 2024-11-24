function updateDateTime() {
    const now = new Date();

    
    const hours = now.getHours();
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    const ampm = hours >= 12 ? 'PM' : 'AM';
    const formattedTime = `${hours % 12 || 12}:${minutes}:${seconds} ${ampm}`;

    
    const day = now.getDate().toString().padStart(2, '0');
    const month = (now.getMonth() + 1).toString().padStart(2, '0'); // Months are zero-based
    const year = now.getFullYear();
    const formattedDate = `${day}/${month}/${year}`;

    // Update the div content
    document.querySelector('.header_time').textContent = formattedTime;
    document.querySelector('.header_date').textContent = formattedDate;
}


setInterval(updateDateTime, 1000);

updateDateTime();



// #pieeeeeeeeeeeeeeeeeee chartttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt
const ctx = document.getElementById('myChart').getContext('2d');

// Function to get the appropriate legend configuration
function getLegendConfig() {
    if (window.matchMedia("(max-width: 768px)").matches) {
        return { position: 'top', labels: { boxWidth: 20 } }; // For mobile, position is top
    } else {
        return {
            position: 'right',
            align: 'center',
            labels: {
                boxWidth: 20, // Width of the legend boxes
                padding: 16,  // Spacing around the legend items
                usePointStyle: true // Use point style for circle shapes
            }
        }; // For desktop, position is top-right
    }
}

let myPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
        labels: ['COW MILK', 'BUFFALO MILK', 'GOAT MILK', 'SPOIL MILK', 'WEST MILK'],
        datasets: [{
            label: 'PERCENTAGE',

            data: [30,10,10,20,10],
            backgroundColor: ['#23CD3E', '#415ADD', '#D9FB52','#D15EEE',"#CF1313"],
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: getLegendConfig(),
            title: {
                display: true,
                text: ''
            }
        },
        layout: {
            padding: {
                top: 20, // Adjust padding to give space for the legend
            }
        }
    }
});

// Update the chart when the window is resized
window.addEventListener('resize', () => {
    myPieChart.options.plugins.legend = getLegendConfig();
    myPieChart.update();
});

document.addEventListener('DOMContentLoaded', () => {
    fetchChartData(null);
    const selectBox = document.querySelector('.select_box select');
    const daysContainer = document.getElementById('days');

    function fetchChartData(year = null) {
        fetch(`/dairyOwner/Dashboard/milk/collection/yearly/pie?year=${year}`)
            .then(response => response.json())
            .then(newData => {
                const total = newData.reduce((sum, value) => sum + value, 0);
                const percentageData = newData.map(value => (value / total * 100).toFixed(2));
                myPieChart.data.datasets[0].data = percentageData;
                myPieChart.update();

                document.querySelector('.total_milk_value').textContent = `${total} L`;
            })
            .catch(error => console.error('Error fetching data:', error));
    }
});