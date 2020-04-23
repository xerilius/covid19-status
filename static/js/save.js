"use strict";

const saveButton = document.getElementById("save");

saveButton.addEventListener('click', saveCounty);

function saveCounty(evt) {
    console.log(evt);

    let countyInfo = evt.target.dataset.countyInfo;
    console.log(countyInfo);
    
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

