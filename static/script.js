let menu = document.querySelector('#menu-icon');
let navbar = document.querySelector('.navbar');

menu.onclick = () => {
  menu.classList.toggle('bx-x');
  navbar.classList.toggle('open');
  if (navbar.classList.contains('open')) {
    navbar.style.display = 'flex';
  } else {
    navbar.style.display = 'none';
  }
}

window.addEventListener('resize', () => {
  if (window.innerWidth > 1090) {
    navbar.style.display = 'flex';
  } else {
    navbar.style.display = 'none';
  }
});

window.addEventListener('click', (event) => {
  // If the clicked element is not within the navbar or menu button
  if (window.innerWidth < 1090) {
    if (!navbar.contains(event.target) && event.target !== menu) {
        navbar.classList.remove('open');
        navbar.style.display = 'none';
        menu.classList.remove('bx-x');
      }
  }
});


const formGroups = document.querySelectorAll('.form-group-s');
const seasonalFormGroups = document.querySelectorAll('.seasonal-form-group');

formGroups.forEach((formGroup) => {
    const selectBtn = formGroup.querySelector('.select-btn'),
        items = formGroup.querySelectorAll('.item');
    const listItems = formGroup.querySelector('.list-items');
    const formItems = listItems.querySelectorAll('.item');

    selectBtn.addEventListener('click', (event) => {
        event.stopPropagation();
        selectBtn.classList.toggle('open');
        listItems.style.display = listItems.style.display === 'block' ? 'none' : 'block';
    
        // Close other dropdowns
        formGroups.forEach((fg) => {
            if (fg !== formGroup) {
                fg.querySelector('.select-btn').classList.remove('open');
                fg.querySelector('.list-items').style.display = 'none';
            }
        });
    });

    items.forEach(item => {
        item.addEventListener("click", (event) => {
            event.stopPropagation();
            item.classList.toggle("checked");
    
            let formGroup = item.closest(".form-group-s");
            let checked = formGroup.querySelectorAll(".checked"),
                btnText = formGroup.querySelector(".btn-text");

            if(checked && checked.length > 0){
                btnText.innerText = `${checked.length} Selected`;
            }else{
                btnText.innerText = "Select Genres";
            }
        });
    })
});

seasonalFormGroups.forEach((formGroup) => {
    const selectBtn = formGroup.querySelector('.select-btn'),
        items = formGroup.querySelectorAll('.item');
    const listItems = formGroup.querySelector('.list-items');

    selectBtn.addEventListener('click', (event) => {
        event.stopPropagation();
        selectBtn.classList.toggle('open');
        listItems.style.display = listItems.style.display === 'block' ? 'none' : 'block';
    });

    items.forEach(item => {
        item.addEventListener("click", (event) => {
            event.stopPropagation();
            let selectedItem = item.querySelector('input[type="radio"]');
            selectedItem.checked = true;
            let btnText = formGroup.querySelector(".btn-text");
            btnText.innerText = item.querySelector('.item-text').innerText;
            selectBtn.classList.remove('open');
            listItems.style.display = 'none';
        });
    });
});

document.addEventListener('click', (e) => {
    if (!e.target.closest('.form-group-s') && !e.target.closest('#search_query') && !e.target.closest('.search-container')) {
        formGroups.forEach((formGroup) => {
            const selectBtn = formGroup.querySelector('.select-btn');
            const listItems = formGroup.querySelector('.list-items');
            selectBtn.classList.remove('open');
            listItems.style.display = 'none';
        });
    }

    if (!e.target.closest('.seasonal-form-group')) {
        seasonalFormGroups.forEach((formGroup) => {
            const selectBtn = formGroup.querySelector('.select-btn');
            const listItems = formGroup.querySelector('.list-items');
            selectBtn.classList.remove('open');
            listItems.style.display = 'none';
        });
    }
});

const filterForm = document.getElementById('filter-form');

filterForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const selectedGenres = document.querySelectorAll('.item.checked input[name="genres"]');
    const selectedTypes = document.querySelectorAll('.item.checked input[name="type"]');
    const selectedAiringStatuses = document.querySelectorAll('.item.checked input[name="airing_status"]');
    const searchQueryInput = document.getElementById('search_query');

    let queryParams = '';

    selectedGenres.forEach((genre, index) => {
        queryParams += (queryParams.length === 0 ? '?' : '&') + 'genres=' + encodeURIComponent(genre.getAttribute('data-genre-name'));
    });
    
    selectedTypes.forEach((type, index) => {
        queryParams += (queryParams.length === 0 ? '?' : '&') + 'type=' + encodeURIComponent(type.value);
    });
    
    selectedAiringStatuses.forEach((status, index) => {
        queryParams += (queryParams.length === 0 ? '?' : '&') + 'status=' + encodeURIComponent(status.value);
    });    

    if (searchQueryInput.value.trim() !== '') {
        queryParams += (queryParams.length === 0 ? '?' : '&') + 'search_query=' + encodeURIComponent(searchQueryInput.value.trim());
    }
    
    if (queryParams.endsWith('&')) {
        queryParams = queryParams.slice(0, -1);
    }

    window.location.href = '/search/anime' + queryParams;
});

document.getElementById('filter-form').addEventListener('click', (e) => {
    e.stopPropagation();
});


