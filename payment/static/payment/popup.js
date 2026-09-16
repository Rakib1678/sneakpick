// If you are using AJAX, you can submit the form data via AJAX like this:
document.getElementById('paymentForm').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const paymentMethod = "Bank Transfer";  // You can pass dynamic payment method as needed
    const accountNumber = document.getElementById('account-number').value;
    const password = document.getElementById('password').value;
  
    fetch('{% url "payment_details" %}', {
      method: 'POST',
      body: new URLSearchParams({
        'payment_method': paymentMethod,
        'account_number': accountNumber,
        'password': password,
      }),
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
      }
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        alert('Payment details submitted successfully');
        window.close(); // Close the popup
      } else {
        alert('Failed to submit payment details');
      }
    })
    .catch(error => {
      alert('An error occurred');
      console.error(error);
    });
  });
  