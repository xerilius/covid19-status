"use strict";
$(document).ready(function() {
    const getDateTime = function() {
        // Date object
        const now = new Date();
        $(".datetime").text(now);
    }

    setInterval(getDateTime, 1000);
});