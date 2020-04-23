"use strict";

const saveButton = document.getElementById("save");

saveButton.addEventListener('click', saveCounty);

function saveCounty(evt) {
    const countyInfo = evt.target.dataset.countyInfo;
    
    if (saveButton.innerHTML == 'Save') {
        $.post(`/save/${countyInfo}`, function() {  
                console.log("Save");
        });
        saveButton.innerHTML = 'Unsave';    
    }

    else if (saveButton.innerHTML =='Unsave') {
        $.post(`/delete/${countyInfo}`, function() {
            console.log("Delete");
        });
        saveButton.innerHTML = 'Save';   
    }
}

