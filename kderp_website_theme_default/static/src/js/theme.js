(function() {
  'use strict';
  $(document).ready(function() {
    //console.log($("#list-features").text().trim() === "");
    if (window.location.pathname !== "/") {
      if ($("#list-features").text().trim()) {
        //Showing features
        //$("#list-main").addClass("col-md-8")
        $("#list-features").addClass("col-md-4");
      } else {
        //Center list main
        $("#list-main").addClass("col-md-push-2");
        $("#list-pager").addClass("col-md-push-2");
      }
    }
  });
})();


