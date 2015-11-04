(function() {
  'use strict';
  $(document).ready(function() {
    //console.log($("#list-features").text().trim() === "");
    if ($("#list-features").text().trim()) {
      //Showing features
      $("#list-features").addClass("col-md-4");
    } else {
      //Center list main
      $("#list-main").addClass("col-md-push-2");
      $("#list-pager").addClass("col-md-push-2");
    }
  });
})();


