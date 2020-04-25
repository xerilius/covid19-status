"use strict";
const countyLinks = document.getElementsByClassName("county-link");

for (let countyLink of countyLinks) {
    countyLink.addEventListener('click', goToLink);
}

function goToLink(evt) {
    const  countyLink = evt.target;
    const countyId = countyLink.dataset.countyId;
    $.get(`/county/${countyId}`, function() {
        console.log(`Go to ${countyId}`)
    })
}