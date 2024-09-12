function showFileName(input) {
    var fileNameElement = document.getElementById('file-name');
    var fileName = input.files[0].name;
    fileNameElement.textContent = fileName;
}

function showLoading() {
    var loaderContainer = document.getElementById('loader-container');
    loaderContainer.style.display = 'block'; // Show loader container

    // Simulate loading delay (2 seconds) - replace with actual logic
    setTimeout(function() {
        // Normally, you would perform an asynchronous action (e.g., AJAX request) here

        // Simulate success after loading
        hideLoading(); // This function should be called after receiving a response from your backend
    }, 500000); // Adjust delay time as per your requirements
}

function hideLoading() {
    var loaderContainer = document.getElementById('loader-container');
    loaderContainer.style.display = 'none'; // Hide loader container
}