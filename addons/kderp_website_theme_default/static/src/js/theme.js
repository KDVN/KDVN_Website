(function() {
  'use strict';
  $(document).ready(function() {
    if (window.location.pathname !== "/") {
      if ($("#list-features").text().trim()) {
        //Showing features
        $("#list-features").addClass("col-md-4");
      } else {
        //Center list main
        $("#list-main").addClass("col-md-push-2");
        $("#list-pager").addClass("col-md-push-2");
      }
    }

    if (!$("#kdvn_news").text().trim()) {
      //Hide KDVN News on homepage
      $("#kdvn_news").removeClass("col-md-3");
      $("#kdvn_meq")
        .removeClass("col-md-9")
        .addClass("col-md-12");
    }
  });
})();


