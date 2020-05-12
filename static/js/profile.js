let questions_answered
let quiz_dict = {}
let score = 0


function removeEntry(data) {

    $.ajax({
        url: '/profile/',
        type:'get',
        data: {delete: data},
        dataType: 'json'
      });
    
    $( "#entries" ).find(`#${data}`).remove();
}

function filterHistory(data) {
    $('#entries').empty();
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
    $( "#entries" ).append(rows);
    $('.deleteBtn').each((i, elm) => {
        $(elm).on("click",  (e) => {
            removeEntry(elm.value)
        })
    })
}



function checkResult(value, key, index, length) {

    let correct;

    (value.toLowerCase().trim() === key) ? (correct = true, score+=1, $(`#link_${key}`).addClass('right')) 
    : (correct = false,  $(`#link_${key}`).addClass('wrong'))

    $(`input[name= '${key}']`).remove()

    quiz_dict[index] = [key, value, correct]

    let nextIndex = Number(index)+1
    questions_answered += 1;

    if (questions_answered == length) {
        $('#question_content').find(`:nth-child(${index})`).removeClass('active show');
        $('#question_number').find(`:nth-child(${index})`).removeClass('active show');
        let result_index = questions_answered + 1
        let link = `<a class="nav-link text-dark border-bottom border-dark active show"  data-toggle="pill" href="#quiz_result" id='link_quiz_result' name = '${result_index}' role="tab">Result</a>`;
        let div = `<div class="tab-pane fade active show" id="quiz_result" role="tabpanel">
        <div class = 'container-fluid'><ul class = 'p-0' id = "ul_quiz_result"></ul></div></div>`
        $('#question_number').append(link);
        $('#question_content').append(div);

        let rows = ''
        for (const key of Object.keys(quiz_dict)) {
            let message
            let correct_answer = quiz_dict[key][0]
            let user_answer = quiz_dict[key][1]
            let is_correct = quiz_dict[key][2]
            is_correct ? message = 'Well done' : message = 'Wrong'
            rows += `
                    <li class = 'my-2' id = 'li_${key}'>
                        Test ${key}. Correct answer: ${correct_answer}. Your answer: ${user_answer}. ${message}
                    </li>
                    `;
            
        }

        let par = `<p class = 'my-2'>Your score is ${score}/${length}</p>`
        let button = '<button class =  "btn btn-dark mt-2" id = "end_quiz">End quiz</button>'
        
        $(`#ul_quiz_result`).append(rows);
        $(`#quiz_result`).append(par);
        $(`#quiz_result`).append(button);

        $('#end_quiz').click(function() {
            $('#question_number').empty();
            $('#question_content').empty();
            $( "#start_quiz" ).show()
            $( "#settings_search" ).show()
        })

        quiz_dict = {}
        questions_answered = 0;
        score = 0;
    }


    else if (nextIndex < length + 1) {
        $('#question_number').find(`:nth-child(${index})`).removeClass('active show');
        $('#question_number').find(`:nth-child(${nextIndex})`).addClass('active show');


        $('#question_content').find(`:nth-child(${index})`).removeClass('active show');
        $('#question_content').find(`:nth-child(${nextIndex})`).addClass('active show');
    }

    
}


function createQuiz(data) {
    questions_answered = 0;
    $('#question_number').empty()
    let keys = Object.keys(data.words)
    let length = keys.length
    let links = '';
    let index = 1;
    for (const key of keys) {
        let rows = '';
        links += `<a class="nav-link text-dark border-bottom border-dark"  data-toggle="pill" href="#${key}" id='link_${key}' name = '${index}' role="tab">Test ${index}</a>`;
        let div = `<div class="tab-pane fade" id="${key}" role="tabpanel">
        <div class = 'container-fluid'><ul class = 'p-0' id = "ul_${key}"></ul></div></div>`
        $('#question_content').append(div)
        


                data.words[key].forEach( definition => {
                    rows += `
                    <li class = 'my-2' id = 'li_${key}'>
                        ${definition}
                    </li>
                    `;
                });


        $(`#ul_${key}`).append(rows);
        let input = `<div class = 'mt-auto w-50'><input class="form-control" type='text' id = '${index}' name = '${key}'></div>`
        $(`#${key}`).append(input);
        $(`input[name= '${key}']`).change(function() {
            let index = $(this).attr('id');
            let val = $(this).val();
            checkResult(val, `${key}`, index, length);
        });

        index += 1; 

    }
    $('#question_number').append(links);
    $( "#question_number").children(":first").addClass("active show");
    $('#question_content').children(":first").addClass("show active");

}


$(document).ready(function(){

    $('.deleteBtn').each((i, elm) => {
        $(elm).on("click",  (e) => {
            removeEntry(elm.value)
        })
    })

  $( ".myInput" ).on('input', function() {
    let value = $(this).val();
    $.ajax({
        url: '/profile/',
        type:'get',
        data: {filter: value},
        success: (data) => filterHistory(data),
        dataType: 'json'
      });
  });

  $( "#start_quiz" ).click(function() {
    $( "#start_quiz" ).hide()
    $( "#settings_search" ).hide()
    $.ajax({
        url: '/profile/',
        type:'get',
        data: 'start',
        success: (data) => createQuiz(data),
        dataType: 'json'
      });
  });


})
