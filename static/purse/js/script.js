// AJAX для загрузки подкатегории
var type = document.getElementById('id_type');
var category_block = document.getElementById('category').style.display = 'none';
var categories_select = document.getElementById('id_category')

type.addEventListener('change', function(event) {
    category_block = document.getElementById('category').style.display = 'none';
    var response = [];
    var type_select = type.value
    console.log(type_select)
    categories_select.options.length = 0;
    const request = new XMLHttpRequest();
    const url = 'http://127.0.0.1:8000/api/ajax/categories/' + type_select;
    request.open('GET', url);
    request.addEventListener('readystatechange', () => {
        if (request.readyState == 4 && request.status == 200) {
            response = JSON.parse(request.responseText);
            response = response['details']
            console.log(response)
            for (i=0; i<response.length; i++) {
                categories_select.options[i] = new Option(response[i]['name']);
            }
            category_block = document.getElementById('category').style.display = 'flex';
        }
    })
    request.send();
})
