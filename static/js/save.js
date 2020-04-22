"use strict";
// Get all node list
const saveButtons = document.getElementsByClassName("save-btn");
// For all the nodes
for (let saveButton of saveButtons) {
    saveButton.addEventListener('click', saveCounty);
}
 function saveCounty(evt) {
    console.log(evt);
    // console.log(evt.target);  // the save button
    const saveButton = evt.target;
    const countyInfo = saveButton.dataset.saveInfo;
    console.log(countyInfo)

    $.post(`/save/${countyInfo}`, function() {
        console.log("AJAX POST");
        // change button to say "unsave"
        saveButton.className = "unsave";
        saveButton.innerHTML = "Unsave";
        console.log(saveButton.className);
    });
   
}