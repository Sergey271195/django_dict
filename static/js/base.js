$(function () {
    console.log("Entry request");
    $.ajax({
        url: '/',
        type:'get',
        data: 'on_load_request',
        success: (data) => onPageEntry(data),
        dataType: 'json'
      });
});

function onPageEntry(data)
{   
    let rows = '';
    data.words.forEach(word => 
        {
        word_capitilize = word[0].toUpperCase() + word.substr(1);
        rows += `
        <div class = 'row border my-1' id = '${word}'>
        <a class="nav-link" style = 'color: orange' href= '/?word=${word}' role="tab" aria-controls="v-pills-home" aria-selected="false">${word_capitilize}</a>
        <button class= 'btn btn-dark ml-auto deleteBtn' value = ${word} data= ${word} >-</button>
        </div>
        `;
    });
    $( "#local_history" ).append(rows);
    $('.deleteBtn').each((i, elm) => {
        $(elm).on("click",  (e) => {
            removeEntry(elm.value)
        })
  
    })
}

function newEntry(data) {

    word_capitilize = data.word[0].toUpperCase() + data.word.substr(1);
    let row = `<div class = 'row border my-1' id = '${data.word}'>
    <a class="nav-link" style = 'color: orange' href= '/?word=${data.word}' role="tab" aria-controls="v-pills-home" aria-selected="false">${word_capitilize}</a>
    <button class= 'btn btn-dark ml-auto deleteBtn' value = ${data.word} data= ${data.word}>-</button>
    </div>`;
    $( "#local_history" ).append(row);
    $('.deleteBtn').each((i, elm) => {
            $(elm).on("click",  (e) => {
            removeEntry(elm.value)
        })
    })
}

function removeEntry(data) {
    $.ajax({
        url: '/',
        type:'get',
        data: {delete: data},
        dataType: 'json'
      });
    
    $( "#local_history" ).find(`#${data}`).remove();
}

$( "#add_button" ).click(function() {
    $.ajax({
        url: '/',
        type:'get',
        data: {to_local_history: $(this).attr("name")},
        success: (data) => newEntry(data),
        dataType: 'json'
      });
    $(this).remove()
    let div = "<div class = 'h3 text-center py-2 px-4 align-self-center ml-4'>Added</div>"
    $( "#main_info" ).append(div);
  });