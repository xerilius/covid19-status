"use strict";

const saveButton = document.getElementById("save");

saveButton.addEventListener('click', saveCounty);

function saveCounty(evt) {
    const countyInfo = evt.target.dataset.countyInfo;
    console.log(evt)
    
    if (saveButton.innerHTML == 'Save') {
        $.post(`/save/${countyInfo}`, function() {  
            console.log("Save");           
        });
        $('#save').toggleClass('unfollow follow');
        saveButton.innerHTML = 'Unsave';     
    }

    else if (saveButton.innerHTML =='Unsave') {
        $.post(`/delete/${countyInfo}`, function() {
            console.log("Delete");       
        });
        $('#save').toggleClass('follow unfollow');    
        saveButton.innerHTML = 'Save'; 
        
        
    }
}

