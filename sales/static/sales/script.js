
document.addEventListener('DOMContentLoaded', function() {
    // Show the login form after 2 seconds
    setTimeout(function() {
        document.getElementById('gif-container').style.display = 'none';
        document.getElementById('container').style.display = 'flex';
        document.getElementById('login-container').style.display = 'flex';
        document.getElementById('logo-container').style.display = 'flex';
    }, 2000); // 2000 milliseconds = 2 seconds
});

function toggleForms() {
    var loginContainer = document.getElementById('login-container');
    var signupContainer = document.getElementById('signup-container');
    if (loginContainer.style.display === 'none') {
        loginContainer.style.display = 'flex';
        signupContainer.style.display = 'none';
    } else {
        loginContainer.style.display = 'none';
        signupContainer.style.display = 'flex';
    }
}
