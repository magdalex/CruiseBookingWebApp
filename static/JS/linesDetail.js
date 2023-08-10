$(document).ready(function() {
  // Show the first tab by default
  $('.tab-pane').first().show();

  // Add a click event listener to each tab button
  $('.tab-button').click(function() {
    // Get the ID of the tab content to show
    var tabId = $(this).attr('data-tab');

    // Hide all tab content
    $('.tab-pane').hide();

    // Show the selected tab content
    $('#' + tabId).show();

    // Set the active class on the selected tab button
    $('.tab-button').removeClass('active');
    $(this).addClass('active');
  });

  // Slideshow script
  var slideIndex = 1;
  showSlides(slideIndex);

  // Next/previous controls
  $('.next').click(function() {
    showSlides(slideIndex += 1);
  });

  $('.prev').click(function() {
    showSlides(slideIndex -= 1);
  });

  function showSlides(n) {
  // Initialize the slideshow
  var slideIndex = 0;
  showSlides();

  // Function to show the slides
  function showSlides() {
  var i;
  var slides = document.getElementsByClassName("slideshow-container")[0].getElementsByTagName("img");

  // Hide all slides
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";
  }

  // Update the slide index
  slideIndex++;

  // Reset the index if it exceeds the number of slides
  if (slideIndex > slides.length) {
    slideIndex = 1;
  }

  // Show the current slide
  slides[slideIndex-1].style.display = "block";

  // Call the function again after 2 seconds (2000 milliseconds)
  setTimeout(showSlides, 2000);
}

// Initialize slideIndex to 1
var slideIndex = 1;

// Call showSlides() to start the slideshow
showSlides();
  }
});