/* Deploy do not show alert follow 
   https://github.com/OCA/website/blob/8.0/website_cookie_notice/views/website.xml
*/
"use strict";
(function($){
    $(".kdvn_alert button").click(function(e){
       e.preventDefault();
       e.stopPropagation();
       $.ajax("/alert_off/" + $(e.target).attr("id"), {
           "complete": function(jqXHR, textStatus) {
                //console.log("DONE", jqXHR, textStatus);
                //TODO: How to hide here
                $(e.target).closest(".kdvn_alert").hide("fast");
           }
       });
    });
})(jQuery);