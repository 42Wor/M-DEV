// Copy code to clipboard
function copyCode(id) {
  const codeElement = document.querySelector(`#${id}`);
  const code = codeElement.textContent;

  try {
    navigator.clipboard.writeText(code);
    console.log('Code copied to clipboard!');
    createNotification('Code copied to clipboard!', 'green');
  } catch (error) {
    console.error(`Error copying code to clipboard: ${error.message}`);
    createNotification('Failed to copy code to clipboard!', 'red');
  }
}

// Copy text to clipboard
function copyText(text) {
  try {
    navigator.clipboard.writeText(text);
    console.log('Text copied to clipboard!');
    createNotification('Text copied to clipboard!', 'green');
  } catch (error) {
    console.error(`Error copying text to clipboard: ${error.message}`);
    createNotification('Failed to copy text to clipboard!', 'red');
  }
}

// Creates a notification element with the given message and color.
function createNotification(message, color) {
  const notification = document.createElement('div');
  notification.className = `notification ${color}`;
  notification.innerHTML = message;

  document.body.appendChild(notification);

  setTimeout(() => {
    notification.remove();
  }, 2000);
}

// Phone number input formatting
$(document).ready(function() {
  $("#mobile_code").intlTelInput({
    initialCountry: "pk",
    separateDialCode: true
  });
});

// Ask for cookie consent
function askForCookieConsent() {
  // implementation not shown
}

// Smooth scrolling for navigation menu
function smoothScrolling() {
  const headerHeight = document.querySelector('header').offsetHeight;

  document.querySelectorAll('nav.menu li a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const targetId = this.getAttribute('href').substring(1);
      const targetElement = document.getElementById(targetId);

      if (targetElement) {
        const targetPosition = targetElement.offsetTop - headerHeight - 28;
        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });
      }
    });
  });
}

// Scroll to section and change button color
function scrollToSection(sectionId) {
  const section = document.getElementById(sectionId);
  if (section) {
    section.scrollIntoView({ behavior: 'smooth' });

    // Toggle 'active' class for the clicked button
    const button = event.target;
    const isActive = button.classList.contains('active');

    // Remove 'active' class from all buttons
    const buttons = document.getElementsByClassName('button');
    for (let i = 0; i < buttons.length; i++) {
      buttons[i].classList.remove('active');
    }

    // Add 'active' class only if it was not active before
    if (!isActive) {
      button.classList.add('active');
    }
  }
}

// Toggle sections
function toggleSection(sectionId, toggleHeadingId, initialState) {
  // implementation not shown
}

// Load terms
function loadTerms() {
  // implementation not shown
}

// Initialize scripts
document.addEventListener("DOMContentLoaded", function() {
  askForCookieConsent();
  smoothScrolling();
  loadTerms();
});
function copyHtmlCode(id) {
  const codeElement = document.querySelector(`#${id}`);
  const code = codeElement.textContent;

  try {
    navigator.clipboard.writeText(code);
    console.log('Code copied to clipboard!');
    createNotification('Code copied to clipboard!', 'green');
  } catch (error) {
    console.error(`Error copying code to clipboard: ${error.message}`);
    createNotification('Failed to copy code to clipboard!', 'ed');
  }
}