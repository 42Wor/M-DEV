// Sticky Navigation Menu JS Code
let nav = document.querySelector("nav");
let scrollBtn = document.querySelector(".scroll-button a");
console.log(scrollBtn);
let val;
window.onscroll = function() {
  if(document.documentElement.scrollTop > 20){
    nav.classList.add("sticky");
    scrollBtn.style.display = "block";
  }else{
    nav.classList.remove("sticky");
    scrollBtn.style.display = "none";
  }

}
function openprojectlink(){
    window. open ('Project/python/')
}
function com(){
    window. open ('com/')
}
// Side NavIgation Menu JS Code
let body = document.querySelector("body");
let navBar = document.querySelector(".navbar");
let menuBtn = document.querySelector(".menu-btn");
let cancelBtn = document.querySelector(".cancel-btn");
menuBtn.onclick = function(){
  navBar.classList.add("active");
  menuBtn.style.opacity = "0";
  menuBtn.style.pointerEvents = "none";
  body.style.overflow = "hidden";
  scrollBtn.style.pointerEvents = "none";
}
cancelBtn.onclick = function(){
  navBar.classList.remove("active");
  menuBtn.style.opacity = "1";
  menuBtn.style.pointerEvents = "auto";
  body.style.overflow = "auto";
  scrollBtn.style.pointerEvents = "auto";
}

// Side Navigation Bar Close While We Click On Navigation Links

// Function to handle change event of the subject select


function handleCVFile() {
  // Define the file URL
  var fileUrl = 'Assets/MBK_CV.pdf'; // Replace this with the actual file URL

  // Check if the user is on a mobile device
  var isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);

  if (isMobile) {
      // If user is on a mobile device, initiate download
      var a = document.createElement('a');
      a.href = fileUrl;
      a.download = 'MBK_CV.pdf'; // Set the desired filename here
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
  } else {
      // If user is on a desktop, open in a new tab/window
      window.open(fileUrl, '_blank');
  }
}





















function AskForCookieConsent() {
    fetch('https://42wor.github.io/Assets/cookie.html').then(response => response.text()).then(html => {
        document.getElementById('cookie').innerHTML = html;
        const termsVersion = document.getElementById('termsVersion').innerText.split(': ')[1];
        checkCookie(termsVersion);
    });
}

function SaveCookie(){
    const termsVersion = document.getElementById('termsVersion').innerText.split(': ')[1];
    setCookie('agreed', termsVersion, 365);
    hideOverlay();
}

function checkCookie(currentVersion) {
    const agreedVersion = getCookie('agreed');
    if (agreedVersion === currentVersion) {
        hideOverlay();
    }
}

function hideOverlay() {
    document.getElementById('cookieNotice').style.display = 'none';
}

function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i];
        while (cookie.charAt(0) === ' ') {
            cookie = cookie.substring(1, cookie.length);
        }
        if (cookie.indexOf(nameEQ) === 0) {
            return cookie.substring(nameEQ.length, cookie.length);
        }
    }
    return null;
}

function hideCookieNotice() {
    document.getElementById('cookieNotice').style.display = 'none';
}
window.addEventListener('error', function(event) {
  if (event.target.status === 404) {
    // Redirect the user to a custom 404 page
    window.location.href = '/404.html';
  }
});
