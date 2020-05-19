// test data
fields2 = {"title":"This is a new  form name","questions":
		[{"type":"open_text","title":"question1","answer":""},
			{"type":"open_text","title":"question2","answer":""}]};

fields = {"title":"Would you please answer some questions about the meeting","questions":
        [{"type":"open_text","title":"What is the best time for you to meet?","answer":""},
            {"type":"open_text","title":"question2","answer":""}]};

questionDivId = 0;

function loadForm() {
	const {pathname} = window.location;
	const id = pathname.match("(\\d+)");
	if(id) {
		console.log(id)
		// TODO: set fields
		generate();
	}
}

function generate(){
	console.log("TESTIK");
	if (Object.keys(fields).length !== 0){
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
			console.log(question.title)
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
				.attr("id",questionDivId)
				.attr("required","required")
                .attr("padding-bottom", "50px");

            questionDiv.append(label_question_title);
			inputDiv.append(input);
            inputDiv.css("padding-bottom","15px");
            $("#inquiry-fields").append(questionDiv).append(inputDiv);
			questionDivId++;
		});
	}
}


function formSubmit(){
	for (var i = 0; i < questionDivId; i++) {
        fields.questions[i].answer = $("#" + i).find("input[type='text']").val();
    }

    const answerJson = JSON.stringify(fields);
	alert(answerJson);

	// const {backend} = window.glob;
	//
	// $.ajax({
	// 	type: "POST",
	// 	url: `${backend}/users/`,
	// 	data: answerJson,
	// 	contentType: "application/json",
	// 	dataType: "json",
	// 	success: function (data) {
	// 		alert("Udalo sie wypelnic anikete");
	// 	},
	// 	failure: function (errMsg) {
	// 		console.log(errMsg);
	// 	},
	// });
}

