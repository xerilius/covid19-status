"use strict";
$(document).ready(function() {
    const getDateTime = function() {
        // Date object
        const now = new Date().toString().toLowerCase();
        
        // Display on page
        $(".datetime").text(now);
        $(".datetime").append("   United States".toLowerCase());
        $(".datetime").append("   Confirmed:".toLowerCase());
        $(".datetime").append(country_confirmed);
        $(".datetime").append("   Deaths:".toLowerCase());
        $(".datetime").append(country_deaths);
    }
    // Update time every second
    setInterval(getDateTime, 1000);
});