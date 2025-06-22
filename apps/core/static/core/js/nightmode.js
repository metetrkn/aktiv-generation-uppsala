$(document).ready(function () {
    // Night mode functionality
    const nightModeToggle = $('#night-mode-toggle');
    const body = $('body');
    const icon = nightModeToggle.find('i');

    // Function to apply the correct theme
    function applyTheme(isDarkMode) {
        if (isDarkMode) {
            body.addClass('dark-mode');
            icon.removeClass('fa-sun').addClass('fa-moon');
        } else {
            body.removeClass('dark-mode');
            icon.removeClass('fa-moon').addClass('fa-sun');
        }
    }

    // Check for saved theme in localStorage
    let isDarkMode = localStorage.getItem('darkMode') === 'true';
    applyTheme(isDarkMode);

    // Toggle night mode on click
    nightModeToggle.click(function (e) {
        e.preventDefault();
        isDarkMode = !isDarkMode;
        applyTheme(isDarkMode);
        localStorage.setItem('darkMode', isDarkMode);
    });
}); 