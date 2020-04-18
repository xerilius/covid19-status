"use strict";
$(document).ready(function() {
    const getDate = function() {
        // Date object
        const now = new Date();
        
        const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

        const weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        
        let mth = months[now.getMonth()];
        let dates = now.getDate();
        let year = now.getFullYear();
        let weekday = weekdays[now.getDay()];
        let todaysDate = mth + " " + dates + ", " + year + " (" + weekday + ")";
        // Display on page
        $(".header__date").html(todaysDate);
    }
    getDate()

    const getTime = function() {
        const now = new Date();
        let timeOfDay = "AM";
        let hours = now.getHours();
        if (hours > 12) {
            hours = hours - 12;
            timeOfDay = " PM";
        }
        let minutes = now.getMinutes();
        let seconds = now.getSeconds();
        
        let todaysTime = hours.toString() + " : " + minutes.toString() + " : " + seconds.toString() + timeOfDay;
        $(".main-header__time").text(todaysTime);
        
    }
    setInterval(getTime, 1000);
});