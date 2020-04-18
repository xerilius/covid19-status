"use strict";
$(document).ready(function() {
    const getDateTime = function() {
        // Date object
        const now = new Date().toString().toLowerCase();
        
        // Display on page
        $(".marquee").text("⚠️ " + now);
        $(".marquee").append("&nbsp; ⋙ &nbsp; United States".toLowerCase());
        $(".marquee").append("&nbsp;  <b>Confirmed: </b>".toLowerCase());
        $(".marquee").append(country_confirmed);
        $(".marquee").append("&nbsp; <b>Deaths: </b>".toLowerCase());
        $(".marquee").append(country_deaths + "&nbsp;⚠️");
    }
    // Update time every second
    setInterval(getDateTime, 1000);
});