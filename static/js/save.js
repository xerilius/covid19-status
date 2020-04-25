"use strict";

const saveButton = document.getElementById("save");

saveButton.addEventListener('click', saveCounty);

function saveCounty(evt) {
    const countyId = evt.target.dataset.countyId;
    console.log(evt)
    
    if (saveButton.innerHTML == 'Save') {
        $.post(`/save/${countyId}`, function() {  
            console.log("Save");           
        });
        $('#save').toggleClass('unfollow follow');
        saveButton.innerHTML = 'Unsave';     
    }

    else if (saveButton.innerHTML =='Unsave') {
        $.post(`/delete/${countyId}`, function() {
            console.log("Delete");       
        });
        $('#save').toggleClass('follow unfollow');    
        saveButton.innerHTML = 'Save'; 
        
        
    }
}

