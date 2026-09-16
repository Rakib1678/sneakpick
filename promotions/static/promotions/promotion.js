document.addEventListener('DOMContentLoaded', () => {
    console.log("Page loaded. Ready to apply discounts.");
});

function applyDiscount(event) {
    event.preventDefault(); // Prevent form submission

    const discountCode = document.getElementById('discountCode').value;
    const messageContainer = document.getElementById('messageContainer'); // Target the message container

    // Clear any previous message
    messageContainer.innerHTML = "";

    if (discountCode && discountMessages[discountCode]) {
        // Show the success message
        messageContainer.innerHTML = `
            <p class="success-message">${discountMessages[discountCode]}</p>
        `;
    } else {
        // Show an error message
        messageContainer.innerHTML = `
            <p class="error-message">Please select a valid discount code.</p>
        `;
    }
}
