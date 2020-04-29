"use strict";
const searchInput = document.querySelector('.searchbar__search');
const suggestions = document.querySelector('.searchbar__suggestions');

searchInput.addEventListener('keyup', displaySuggestions);

function displaySuggestions(evt) {
  console.log(evt);
  evt.preventDefault();
  let search = $('.searchbar__search').val();
  if (search == '') {
    search = null;
  }

  $.ajax({
    data: {input: `${search}`},
    type: 'GET',
    url: '/searchbar.json'
  })
  .done(function(data){
    const regex = new RegExp(search, 'gi');
    const html = data.map(place => {
      let countyName = place.county.replace(regex, `<span class="u-highlight"> ${search}</span>`)
      let stateName = place.state.replace(regex, `<span class="u-highlight"> ${search}</span>`)
      return (`
        <li> 
        <span class="name"><a href="/county/${place.id}" class="county-link" data-county-id="${place.id}"> ${countyName}, ${stateName} </a> </span>
        </li>`);
      }).join('');
      suggestions.innerHTML = html;
  });
  
}
