// farmer_register.js

// function showFlashMessage(message) {
//     const flashMessage = document.getElementById("flash-message");
//     const flashMessageText = flashMessage.querySelector(".flash-message-text");
//     const progressBar = document.getElementById("flash-progress");

//     flashMessageText.innerText = message;
//     flashMessage.style.opacity = "1";
//     flashMessage.style.visibility = "visible";
    
//     // Set the progress bar to full (100%)
//     progressBar.value = 100;

//     // Duration settings
//     const displayDuration = 4000; // Message visible duration in milliseconds
//     const fadeOutDuration = 1000;  // Fade out duration in milliseconds
//     const totalDuration = displayDuration + fadeOutDuration;

//     const interval = 20; // Update every 20 ms
//     const decrement = 100 / (totalDuration / interval); // Amount to decrease per interval

//     // Use setInterval to decrease progress smoothly
//     const progressInterval = setInterval(() => {
//         progressBar.value -= decrement;

//         // If progress bar reaches 0, start fading out
//         if (progressBar.value <= 0) {
//             clearInterval(progressInterval);
//             closeFlashMessage();
//         }
//     }, interval);

//     // Start fade out after the message display duration
//     setTimeout(() => {
//         // Start fading out the flash message
//         const fadeOutInterval = setInterval(() => {
//             let currentOpacity = parseFloat(flashMessage.style.opacity);
//             currentOpacity -= 0.05; // Decrease opacity by 0.05 per interval

//             if (currentOpacity <= 0) {
//                 clearInterval(fadeOutInterval);
//                 flashMessage.style.opacity = "0";
//                 flashMessage.style.visibility = "hidden"; // Hide the message after fading out
//             } else {
//                 flashMessage.style.opacity = currentOpacity;
//             }
//         }, 50); // Fade out every 50 ms

//     }, displayDuration); // Wait for the display duration before starting fade out
// }

// // Function to close the flash message manually
// function closeFlashMessage() {
//     const flashMessage = document.getElementById("flash-message");
//     flashMessage.style.opacity = "0";
//     flashMessage.style.visibility = "hidden";
// }


function showFlashMessage(message, type = "success") {
    const flashMessage = document.getElementById("flash-message");
    const flashMessageText = flashMessage.querySelector(".flash-message-text");
    const progressBar = document.getElementById("flash-progress");

    // Apply alert type class
    flashMessage.className = `alert alert-${type} d-flex align-items-center`;

    flashMessageText.innerText = message;
    flashMessage.style.display = "block";  // Show the element
    flashMessage.style.opacity = "1";
    flashMessage.style.visibility = "visible";

    // Set the progress bar to full (100%)
    progressBar.value = 100;

    // Duration settings
    const displayDuration = 4000; // Message visible duration in milliseconds
    const fadeOutDuration = 1000;  // Fade out duration in milliseconds
    const totalDuration = displayDuration + fadeOutDuration;

    const interval = 20; // Update every 20 ms
    const decrement = 100 / (totalDuration / interval); // Amount to decrease per interval

    // Use setInterval to decrease progress smoothly
    const progressInterval = setInterval(() => {
        progressBar.value -= decrement;

        // If progress bar reaches 0, start fading out
        if (progressBar.value <= 0) {
            clearInterval(progressInterval);
            closeFlashMessage();
        }
    }, interval);

    // Start fade out after the message display duration
    setTimeout(() => {
        // Start fading out the flash message
        const fadeOutInterval = setInterval(() => {
            let currentOpacity = parseFloat(flashMessage.style.opacity);
            currentOpacity -= 0.05; // Decrease opacity by 0.05 per interval

            if (currentOpacity <= 0) {
                clearInterval(fadeOutInterval);
                flashMessage.style.opacity = "0";
                flashMessage.style.visibility = "hidden"; // Hide the message after fading out
                flashMessage.style.display = "none"; // Hide the element after fading out
            } else {
                flashMessage.style.opacity = currentOpacity;
            }
        }, 50); // Fade out every 50 ms

    }, displayDuration); // Wait for the display duration before starting fade out
}

// Function to close the flash message manually
function closeFlashMessage() {
    const flashMessage = document.getElementById("flash-message");
    flashMessage.style.opacity = "0";
    flashMessage.style.visibility = "hidden";
    flashMessage.style.display = "none";  // Hide the element
}

console.log(document.getElementById('registerBtn'))
document.getElementById('registerBtn').addEventListener('click', (e) => {
    e.preventDefault(); // Prevent the default form submission
    
    // Collect form data
    const formData = new FormData(document.querySelector('form'));
    // Send form data to the backend
    fetch('/farmer/register', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log("Data got")
            showOtpModal(); // Show OTP modal if registration is successful
        } else {
            displayMessage(data.message, 'error'); // Handle success false scenario
        }
    })
    .catch(error => console.error('Error:', error));
});

// Function to display messages
function displayMessage(message, type) {
    console.log("Displaying Msg");
    const messageContainer = document.getElementById('messageContainer');
    messageContainer.innerHTML = `<div class="${type}">${message}</div>`;
    messageContainer.style.color = type === 'error' ? 'red' : 'green'; // Set color based on message type
}

// Function to show the OTP modal
function showOtpModal() {
    console.log("Showing OTP model")
    const otpModal = document.createElement('div');
    otpModal.classList.add('modal');

    otpModal.innerHTML = `
        <div class="modal-background">
            <div class="modal-content">
                <form id="otpForm">
                    <label for="mobile_otp">Enter OTP sent to your registered mobile no.</label>
                    <input type="text" name="mobile_otp" placeholder="4 digit OTP" required>
                    <h2>OR</h2>
                    <label for="email_otp">Enter OTP sent to your registered email.</label>
                    <input type="text" name="email_otp" placeholder="4 digit OTP" required>
                    <br>
                    <button type="submit">Confirm</button>
                </form>
                <div id="otpMessageContainer"></div> <!-- Message container for OTP -->
            </div>
        </div>
    `;

    document.body.appendChild(otpModal);

    // Handle OTP form submission
    document.getElementById('otpForm').addEventListener('submit', (e) => {
        e.preventDefault();
        const email_otp = document.querySelector('#otpForm input[name="email_otp"]').value;
        const mobile_otp = document.querySelector('#otpForm input[name="mobile_otp"]').value;

        // Send OTP data to the backend for verification
        fetch('/farmer/validate-otp', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ email_otp: email_otp, mobile_otp: mobile_otp })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    displayOtpMessage(data.message, 'error');
                });
            }
            // If validation is successful, redirect to login
            window.location.href = '/farmer/login';
        })
        .catch(error => console.error('Error:', error));
    });
}

// Function to display messages in the OTP modal
function displayOtpMessage(message, type) {
    const otpMessageContainer = document.getElementById('otpMessageContainer');
    otpMessageContainer.innerHTML = `<div class="${type}">${message}</div>`;
    otpMessageContainer.style.color = type === 'error' ? 'red' : 'green'; // Set color based on message type
}

function validateMobileNumber()
{
    const mobileInput = document.getElementById('mobileNumber');
    const mobileError = document.getElementById('mobileError');


    if (mobileInput.value.length === 10 && /^\d{10}$/.test(mobileInput.value)) {
        mobileInput.style.border = "";
        mobileError.style.display = "none";
    }
    else
    {
        mobileInput.style.border = '1px solid red';
        mobileError.style.display = 'inline';
    }
}