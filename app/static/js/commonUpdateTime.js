function updateDateTime() {
    const now = new Date();

    // Extract the current date
    const currentDate = now.toLocaleDateString(); // Get local date

    // Extract the current time
    const currentTime = now.toLocaleTimeString(); // Get local time

    // Update the HTML elements with the current date and time
    document.getElementById("date").textContent = currentDate;
    document.getElementById("time").textContent = currentTime;
  }

  // Update the date and time when the page loads
  window.onload = updateDateTime;

  // Optionally, keep the time updated every second (for real-time display)
  setInterval(updateDateTime, 1000); // Updates every second
