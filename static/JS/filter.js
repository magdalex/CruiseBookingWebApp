$(document).ready(function() {
  // Parse the URL to get the regions parameter value
  var urlParams = new URLSearchParams(window.location.search);
  var regions = urlParams.get('regions');
  var ports = urlParams.get('ports');

  // If the regions parameter is present, set the value of the regions filter dropdown
  if (regions) {
    $('#regions').val(regions);
  }

   // If the ports parameter is present, set the value of the ports filter dropdown
  if (ports) {
    $('#ports').val(ports);
  }

  // Detect when the user changes the value of a filter dropdown
  $('.filter').change(function() {
    // Build the query string based on the current filter values
    var queryParams = '?';
    $('.filter').each(function() {
      var filter = $(this).data('filter');
      var value = $(this).val();
      if (value) {
        queryParams += filter + '=' + value + '&';
      }
    });
    // Remove the trailing '&' from the query string
    queryParams = queryParams.slice(0, -1);

    // Update the URL of the page to include the current filter values
    var newUrl = window.location.origin + window.location.pathname + queryParams;
    window.history.replaceState(null, null, newUrl);
  });
});