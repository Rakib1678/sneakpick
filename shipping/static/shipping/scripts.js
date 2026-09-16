function updatePrice() {
    // Get the shipping methods dropdown, total price, and estimated delivery elements
    const shippingMethods = document.getElementById('shippingMethods');
    const totalPrice = document.getElementById('totalPrice');
    const finalTotal = document.getElementById('finalTotal');
    const estimatedDelivery = document.getElementById('estimatedDelivery');
    
    // Get the selected option
    const selectedOption = shippingMethods.options[shippingMethods.selectedIndex];

    // Fetch the price from the 'data-charge' attribute and parse it as a float
    const charge = parseFloat(selectedOption.getAttribute('data-charge'));
    
    // If the charge is NaN, default to 0.00
    if (isNaN(charge)) {
        totalPrice.textContent = '0.00';
        finalTotal.textContent = '0.00';
        estimatedDelivery.textContent = 'N/A';
        return;
    }

    // Update the shipping price
    totalPrice.textContent = charge.toFixed(2);

    // Update the estimated delivery time
    const deliveryTime = selectedOption.getAttribute('data-delivery');
    estimatedDelivery.textContent = deliveryTime || 'N/A';

    // Retrieve the total payment value from a data attribute (assumed to be passed in from the backend)
    const totalPayment = parseFloat(document.body.getAttribute('data-total-payment')) || 0.00;

    // Calculate and update the final total (total payment + shipping)
    const finalAmount = totalPayment + charge;
    finalTotal.textContent = finalAmount.toFixed(2);
}
