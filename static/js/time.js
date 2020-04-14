"use strict";
$(document).ready(function() {
    const getDateTime = function() {
        // Date object
        const now = new Date().toString().toLowerCase();
    
        // Display on page
        $(".datetime").text(now);
        
    }
    // Update time every second
    setInterval(getDateTime, 1000);
});