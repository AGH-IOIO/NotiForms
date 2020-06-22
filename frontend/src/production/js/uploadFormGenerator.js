fields = {"owner":"admin","title":"Ankieta 1",
    "questions":[{"type":"single_choice","title":"This is single-choice question1?","options":["This is option 1.","This is option 2.","This is option 3."]},
        {"type":"open_text","title":"This is a text question2?","options":[]},
        {"type":"open_text","title":"This is a text question3?","options":[]},
        {"type":"multiple_choice","title":"This is multiple-choice question1?","options":["This is option 1.","This is option 2.","This is option 3.","This is option 4."]},
        {"type":"multiple_choice","title":"This is multiple-choice question1?","options":["This is option 1.","This is option 2.","This is option 3."]}]};

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
			var questionType = question.type;
			var questionDiv = $("<div>")
                .addClass("row")
				.addClass("item")
				.addClass("form-group");
            var label_question_title = $("<h4>")
                .addClass("title_left")
				.attr("for", "input-form-name")
				.text(question_title);

            questionDiv.append(label_question_title);
            $("#inquiry-fields").append(questionDiv);
            if(questionType === "open_text"){
                addTextAnswerInput(questionDivId);
            }
            else if(questionType === "single_choice"){
                addSingleChoiceAnswerInput(questionDivId);
            }
            else if(questionType === "multiple_choice"){
                addMultipleChoiceAnswerInput(questionDivId);
            }
			questionDivId++;
		});
	}
}

function addTextAnswerInput(questionID){

    var inputDiv = $("<div>")
        .addClass("row")
        .attr("id", "answerDiv" + questionID);


    var input = $("<input>")
        .attr("type", "text")
        .addClass("form-control")
        .attr("placeholder", "Answer")
        .attr("id","textAnswer" + questionID)
        .attr("required","required")
        .attr("padding-bottom", "50px");

    inputDiv.append(input);
    inputDiv.css("padding-bottom","15px");

    $("#inquiry-fields").append(inputDiv);
}

function addSingleChoiceAnswerInput(questionID){
    var inputDiv = $("<div>")
        .attr("id", "answerDiv" + questionID);

    var options = fields.questions[questionID].options;
    let radioID = 0;
    options.forEach(option => {
        var radioDiv = $("<div>")
            .addClass("row")
            .addClass("item")
            .addClass("form-group")
            .attr("id", "answerRadioDiv" + questionID);

        var radio = $("<input>")
            .attr("type", "radio")
            .attr("checked", "checked")
            .attr("name", "radio" + questionID)
            .attr("id", "radio" + radioID);

        radio.css({width: "25px", height: "17px"});


        var label = $("<label>")
            .attr("for", "radio" + questionID)
            .html(option);


        radioDiv.append(radio);
        radioDiv.append(label);
        inputDiv.append(radioDiv);

        radioID++;
    });

    inputDiv.css("padding-bottom","15px");

    $("#inquiry-fields").append(inputDiv);
}

function addMultipleChoiceAnswerInput(questionID){
    var inputDiv = $("<div>")
        .attr("id", "answerDiv" + questionID);

    var options = fields.questions[questionID].options;
    var checkIndex = 0;
    options.forEach(option => {
        var checkDiv = $("<div>")
            .addClass("row")
            .addClass("item")
            .addClass("form-group")
            .attr("id", "answerCheckDiv" + questionID);

        var check = $("<input>")
            .attr("type", "checkbox")
            .attr("id", "check" + checkIndex);

        check.css({width: "25px", height: "17px"});

        var label = $("<label>")
            .attr("for", "check" + questionID)
            .html(option);


        checkDiv.append(check);
        checkDiv.append(label);
        inputDiv.append(checkDiv);

        checkIndex++;
    });

    inputDiv.css("padding-bottom","15px");

    $("#inquiry-fields").append(inputDiv);
}



function formSubmit(){
    let answers = [];

	for (var questionID = 0; questionID <  questionDivId; questionID++) {
        var questionType = fields.questions[questionID].type;
        if(questionType === "open_text"){
            answers.push($("#answerDiv" + questionID).find("input[type='text']").val());
        }
        else if(questionType === "single_choice"){
            var optionID = $("#answerDiv" + questionID).find($("input[type='radio']:checked")).attr("id");
            optionID = optionID.slice("radio".length);
            answers.push(optionID);
        }
        else if(questionType === "multiple_choice"){
            let checkedOption = [];
            $.each($("#answerDiv" + questionID).find("input[type='checkbox']:checked"), function(){
                var checkID = $(this).attr("id");
                checkID = parseInt(checkID.slice("check".length));
                checkedOption.push(checkID);
            });
            answers.push(checkedOption);
        }
    }

	const username = localStorage.getItem("username");

	const answerJson = JSON.stringify({
		form_id: form._id,
		answers: answers,
		recipient: username
	});
	alert(answerJson);

	//TODO delete
	//return;

	const {backend} = window.glob;
	const token = localStorage.getItem("token");

	if(backend && token) {
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
				//console.log("success");
			},
			failure: function (errMsg) {
				console.log(errMsg);
			},
		});
	}
}

