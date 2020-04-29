"use strict";
const searchInput = document.querySelector('.searchbar__search');
const suggestions = document.querySelector('.searchbar__suggestions');

searchInput.addEventListener('submit', disableSubmit);
searchInput.addEventListener('keyup', displaySuggestions);


function disableSubmit(evt) {
  console.log("hiiiiiiiiiiiiiiiiiiiiiiiiii");
  evt.preventDefault();
}

function displaySuggestions(evt) {
  console.log(evt);
  evt.preventDefault();
  let search = $('.searchbar__search').val();
  if (search == '') {
    search = null;
  }

  $.ajax({
    data: {input: `${search}`},
    type: 'POST',
    url: '/searchbar.json'
  })
  .done(function(data){
    const regex = new RegExp(search, 'gi');
    const html = data.map(place => {
      let countyName = place.county.replace(regex, `<span class="h1"> ${search}</span>`)
      let stateName = place.state.replace(regex, `<span class="h1"> ${search}</span>`)
      return (`
        <li> 
        <span class="name"> ${countyName}, ${stateName} </span>
        </li>`);
      }).join('');
      suggestions.innerHTML = html;
  });
  
}
