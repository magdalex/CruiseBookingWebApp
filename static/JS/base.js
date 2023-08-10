$(document).ready(function() {
  var slideIndex = 1;
  showSlides(slideIndex);

  function plusSlides(n) {
    showSlides(slideIndex += n);
  }

  function currentSlide(n) {
    showSlides(slideIndex = n);
  }

  function showSlides(n) {
    var i;
    var slides = $(".slideshow-container img");
    var dots = $(".slideshow-container a");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
        dots[i].style.opacity = "0";
    }
    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].style.opacity = "1";
    setTimeout(function(){plusSlides(1)}, 5000);
  }

  // Get the navbar element
var navbar = document.querySelector('.navbar');

// Get the initial position of the navbar
var navbarPosition = navbar.offsetTop;

// Add a scroll event listener to the window
window.addEventListener('scroll', function() {
  // If the user has scrolled past the navbar, add the fixed-navbar class to it
  if (window.pageYOffset >= navbarPosition) {
    navbar.classList.add('fixed-navbar');
  } else {
    // Otherwise, remove the fixed-navbar class
    navbar.classList.remove('fixed-navbar');
  }
});

});