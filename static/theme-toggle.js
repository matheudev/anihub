document.addEventListener('DOMContentLoaded', () => {
    const htmlElement = document.documentElement;
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
      const body = document.body;
    
      // Check for saved theme preference in localStorage and apply the appropriate theme
      const savedTheme = localStorage.getItem('theme');
      if (savedTheme) {
        body.classList.add(savedTheme);
        updateThemeIcon(savedTheme);
      } else {
        body.classList.add('white-theme');
      }
    
      // Toggle theme and save the preference in localStorage
      themeToggle.addEventListener('click', () => {
        body.classList.toggle('white-theme');
        if (body.classList.contains('white-theme')) {
          localStorage.setItem('theme', 'white-theme');
          updateThemeIcon('white-theme');
        } else {
          localStorage.removeItem('theme');
          updateThemeIcon('');
        }
      });
    }
    
    // Remove the 'no-js' class and show the body content
    htmlElement.classList.remove('no-js');
  });
  
  // Function to update the theme icon based on the current theme
  function updateThemeIcon(theme) {
    const themeIcon = document.querySelector('#theme-toggle i');
    if (theme === 'white-theme') {
      themeIcon.classList.remove('ri-sun-fill');
      themeIcon.classList.add('ri-sun-line');
    } else {
      themeIcon.classList.remove('ri-sun-line');
      themeIcon.classList.add('ri-sun-fill');
    }
  }
  
// Get the alert box element
const alertBox = document.getElementById('alert-box');

// Get the close button element
const closeButton = alertBox.querySelector('.close');

// Remove the margin when the alert is closed
closeButton.addEventListener('click', () => {
alertBox.style.display = 'none';
});