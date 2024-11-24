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


// Function to fetch new data from the backend     @backendteam [Atharva,Shreyash,Rishi]
// document.getElementById('updateData').addEventListener('click', () => {
//     fetch('/dairyOwner/Dashboard/milk/collection/chart')
//         .then(response => response.json())
//         .then(newData => {
//             myPieChart.data.datasets[0].data = newData;
//             myPieChart.update();
//         })
//         .catch(error => console.error('Error fetching data:', error));
// });

// Function to fetch new data from the backend
document.addEventListener('DOMContentLoaded', () => {

    fetchChartData(null, 'daily');
    document.addEventListener('DOMContentLoaded', () => {
        const selectBox = document.querySelector('.select_box select');
        const savedValue = localStorage.getItem('selectedView');
    
        selectBox.value = savedValue || 'daily';
    });

    const selectBox = document.querySelector('.select_box select');
    const daysContainer = document.getElementById('days');

    function fetchChartData(date = null, viewType = 'daily') {
        fetch(`/dairyOwner/Dashboard/milk/collection/chart?date=${date}&viewType=${viewType}`)
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

    daysContainer.addEventListener('click', event => {
        if (event.target.tagName === 'DIV' && event.target.textContent) {
            const selectedDate = `${currentDate.getFullYear()}-${(currentDate.getMonth() + 1).toString().padStart(2, '0')}-${event.target.textContent.padStart(2, '0')}`;
            const viewType = selectBox.value.toLowerCase();
            fetchChartData(selectedDate, viewType);
        }
    });

    selectBox.addEventListener('change', () => {
        const viewType = selectBox.value.toLowerCase();

        if (viewType === "yearly") {
            window.location.href = `/dairyOwner/Dashboard/milk/collection/yearly?year=null`;
        }
        localStorage.setItem('selectedView', selectBox.value);
        fetchChartData(null, viewType);
        const todayElements = document.getElementsByClassName("today");
        if (todayElements.length > 0) {
            todayElements[0].click();
        }
    });

    renderCalendar();


    // CSS class to highlight selected dates
    function highlightDates(dates) {
        const dayElements = daysContainer.querySelectorAll('div');
        dayElements.forEach(day => day.classList.remove('highlight'));

        dates.forEach(date => {
            const day = new Date(date).getDate();
            dayElements.forEach(dayElement => {
                if (parseInt(dayElement.textContent) === day) {
                    dayElement.classList.add('highlight');
                }
            });
        });
    }

    daysContainer.addEventListener('click', event => {
        if (event.target.tagName === 'DIV' && event.target.textContent) {
            const selectedDate = `${currentDate.getFullYear()}-${(currentDate.getMonth() + 1).toString().padStart(2, '0')}-${event.target.textContent.padStart(2, '0')}`;
            const viewType = selectBox.value.toLowerCase();

            if (viewType === 'weekly') {
                // Calculate the last 7 days including the selected date but restrict to visible days
                const selectedDay = parseInt(event.target.textContent); // Get selected day from the clicked element
                const visibleDays = Array.from(daysContainer.querySelectorAll('div')).map(el => parseInt(el.textContent)); // Get visible days
                const dates = visibleDays
                    .filter(day => day <= selectedDay && day > selectedDay - 7) // Restrict to the last 7 visible days
                    .map(day => `${currentDate.getFullYear()}-${(currentDate.getMonth() + 1).toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`);
                highlightDates(dates);
    
            } else if (viewType === 'monthly') {
                // Highlight all visible days in the current month
                const dates = Array.from(daysContainer.querySelectorAll('div')).map(dayElement => {
                    const day = parseInt(dayElement.textContent);
                    return `${currentDate.getFullYear()}-${(currentDate.getMonth() + 1).toString().padStart(2, '0')}-${day.toString().padStart(2, '0')}`;
                });
                highlightDates(dates);
            } else {
                highlightDates([selectedDate]);
            }

            fetchChartData(selectedDate, viewType);
        }
    });
});



// this is the code for the calender functionlaity 
  const daysContainer = document.getElementById('days');
  const monthYearDisplay = document.getElementById('monthYear');
  let currentDate = new Date();

  function renderCalendar() {
    daysContainer.innerHTML = '';
    const month = currentDate.getMonth();
    const year = currentDate.getFullYear();

    monthYearDisplay.textContent = `${currentDate.toLocaleString('default', { month: 'long' })} ${year}`;

    const firstDayOfMonth = new Date(year, month, 1).getDay();
    const lastDateOfMonth = new Date(year, month + 1, 0).getDate();

    const paddingDays = (firstDayOfMonth === 0 ? 7 : firstDayOfMonth) - 1;

    for (let i = 0; i < paddingDays; i++) {
      daysContainer.innerHTML += `<div></div>`;
    }

    for (let day = 1; day <= lastDateOfMonth; day++) {
      const dayElement = document.createElement('div');
      dayElement.textContent = day;

      const isToday =
        day === new Date().getDate() &&
        month === new Date().getMonth() &&
        year === new Date().getFullYear();

      if (isToday) {
        dayElement.classList.add('today');
      }
      dayElement.addEventListener('click', () => {
      // Remove highlight from previously selected day
      if (selectedDayElement) {
        selectedDayElement.classList.remove('selected');
      }

      // Highlight the clicked day
      dayElement.classList.add('selected');
      selectedDayElement = dayElement; // Update selected day element
    });
      daysContainer.appendChild(dayElement);
    }
  }

  function prevMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
  }

  function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
  }

  renderCalendar();
