fields = {
    "title": "Would you please answer some questions about the meeting", "questions":
        [{"type": "open_text", "title": "What is the best time for you to meet?", "answer": ""},
            {"type": "open_text", "title": "question2", "answer": ""}]
};

questionDivId = 0;

let form = {};

function loadForm() {
    const {pathname} = window.location;
    const id = pathname.split("/").pop()

    if (id) {
        if (window.glob.forms) {
            form = window.glob.forms.find(t => t._id === id);
            fields.title = form.template.title;
            fields.questions = form.template.questions;
            generate();
        } else {
            const {backend} = window.glob;
            const token = localStorage.getItem("token");
            const username = localStorage.getItem("username");

            if (backend && token && username) {
                $.ajax({
                    type: "GET",
                    url: `${backend}/forms/pending/${username}/`,
                    headers: {
                        "Authorization": token
                    },
                    contentType: "application/json",
                    dataType: "json",
                    success: function (data) {
                        if (data.forms) {
                            form = data.forms.find(t => t._id === id);
                            fields.title = form.template.title;
                            fields.questions = form.template.questions;
                            generate();
                        }
                    },
                    failure: function (errMsg) {
                        console.log(errMsg);
                    },
                });
            }
        }
    }
}

function generate() {
    if (Object.keys(fields).length !== 0) {
        //clear content of previous form
        questionDivId = 0;
        $("#inquiry-fields").html("");
        $("#form_title").html("");


        var title = fields.title;
        var form_name = $("<h2>")
            .addClass("title_left")
            .attr("for", "input-form-name")
            .text(title);
        $("#form_title").append(form_name);

        fields.questions.forEach(question => {
            var question_title = (questionDivId + 1).toString(10) + ". " + question.title;
            var questionDiv = $("<div>")
                .addClass("row")
                .addClass("item")
                .addClass("form-group")
            var label_question_title = $("<h4>")
                .addClass("title_left")
                .attr("for", "input-form-name")
                .text(question_title);
            var inputDiv = $("<div>")
                .addClass("row")
                .attr("id", questionDivId);


            var input = $("<input>")
                .attr("type", "text")
                .addClass("form-control")
                .attr("placeholder", "Answer")
                .attr("id", questionDivId)
                .attr("required", "required")
                .attr("padding-bottom", "50px");

            questionDiv.append(label_question_title);
            inputDiv.append(input);
            inputDiv.css("padding-bottom", "15px");
            $("#inquiry-fields").append(questionDiv).append(inputDiv);
            questionDivId++;
        });
    }
}


function formSubmit() {
    for (var i = 0; i < questionDivId; i++) {
        fields.questions[i].answer = $("#" + i).find("input[type='text']").val();
    }

    const answers = fields.questions.map(q => q.answer);
    const username = localStorage.getItem("username");

    const answerJson = JSON.stringify({
        form_id: form._id,
        answers: answers,
        recipient: username
    });
    //alert(answerJson);

    const {backend} = window.glob;
    const token = localStorage.getItem("token");

    if (backend && token) {
        $.ajax({
            type: "POST",
            url: `${backend}/forms/fill/`,
            data: answerJson,
            headers: {
                "Authorization": token
            },
            contentType: "application/json",
            dataType: "json",
            success: function (data) {
                refreshNavbar();
                window.location.href = "/dashboard";
            },
            failure: function (errMsg) {
                console.log(errMsg);
            },
            error: function (errMsg) {
                console.log(errMsg);
            },
        });
    }
    return false;

}

