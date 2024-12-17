// static/js/dashboard.js

document.addEventListener('DOMContentLoaded', function () {
    const transferForm = document.getElementById('transferForm');
    const getAccountsButtons = document.getElementById('getAccountsButtons');
    const accountsList = document.getElementById('accountsList');
    const accountNameInput = document.getElementById('accountName');
    const accountDetails = document.getElementById('accountDetails');
    const accountNameDisplay = document.getElementById('accountNameDisplay');
    const accountBalanceDisplay = document.getElementById('accountBalanceDisplay');
    const errorElement = document.getElementById('error');
    const messageElement = document.getElementById('message');

    document.getElementById('csvUploadForm').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent default form submission

        const formData = new FormData(this);  // Get form data
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
        // Use Axios to send the POST request
        axios.post('/api/import-accounts/', formData, {
            headers: {
                'X-CSRFToken': csrfToken,  // Add CSRF token to headers
                'Content-Type': 'multipart/form-data'
            }
        })
        .then(response => {
            if (response.data.message) {
                alert(response.data.message);  // Success message
            } else {
                alert('Failed to upload CSV: ' + response.data.error);  // Error message
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while uploading the CSV.');
        });
    });

    // Function to fetch accounts from the API
    const fetchAccounts = () => {
        axios.get('/api/accounts/')
            .then((response) => {
                const accounts = response.data;
                errorElement.style.display = 'none';  // Hide previous error

                if (accounts.length === 0) {
                    accountsList.innerHTML = '<li class="list-group-item">No accounts found.</li>';
                    return;
                }

                // Display only the first 2 accounts
                accountsList.innerHTML = '';
                accounts.forEach((account) => {
                    const li = document.createElement('li');
                    li.classList.add('list-group-item');
                    li.innerHTML = `Name: ${account.Name}<br>Balance: $${account.Balance}`;
                    accountsList.appendChild(li);
                });

                messageElement.style.display = 'block';
                messageElement.textContent = 'Accounts loaded successfully.';
            })
            .catch((err) => {
                errorElement.style.display = 'block';
                errorElement.textContent = 'Failed to fetch accounts.';
                messageElement.style.display = 'none';
            });
    };

    const getAccountByName = (name) => {
        axios.get(`/api/account/?name=${name}`)
            .then((response) => {
                const account = response.data;
                errorElement.style.display = 'none';  // Hide previous error

                // Display account details
                accountNameDisplay.textContent = `Name: ${account.Name}`;
                accountBalanceDisplay.textContent = `Balance: $${account.Balance}`;
                accountDetails.style.display = 'block';

                messageElement.style.display = 'block';
                messageElement.textContent = 'Account loaded successfully.';
            })
            .catch((err) => {
                console.log(err.message)
                errorElement.style.display = 'block';
                errorElement.textContent = 'Account not found.';
                messageElement.style.display = 'none';
               
                
            });
    };

    // Add click event listener to the "Refresh Accounts" button
    getAccountsButtons.addEventListener('click', () => {
        fetchAccounts();
    });
    accountSearchForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const accountName = accountNameInput.value.trim();
        if (accountName) {
            getAccountByName(accountName);
        }
    });

    transferForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent default form submission

        // Gather form data
        const senderName = senderNameInput.value.trim();
        const receiverName = receiverNameInput.value.trim();
        const amount = parseFloat(amountInput.value);

        // Validate the form fields
        if (!senderName || !receiverName || !amount || isNaN(amount) || amount <= 0) {
            errorElement.style.display = 'block';
            errorElement.textContent = 'Please fill in all fields with valid data.';
            messageElement.style.display = 'none';
            return;
        }

        // Send the transfer request to the backend
        axios.post('/api/transfer-funds/', {
            sender_name: senderName,
            receiver_name: receiverName,
            amount: amount
        })
        .then((response) => {
            // Display success message
            messageElement.style.display = 'block';
            messageElement.textContent = 'Transfer successful!';
            errorElement.style.display = 'none';
        })
        .catch((err) => {
            // Display error message
            errorElement.style.display = 'block';
            errorElement.textContent = 'Failed to transfer funds. Please try again.';
            messageElement.style.display = 'none';
        });
    });

    
});
