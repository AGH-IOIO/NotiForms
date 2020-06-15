fields = {};
checked = [];
optionIndexes = [];

let index = 0;

function addTextField(){

	var fieldIndex = index;
	var fieldID = "field"+fieldIndex;
	var fieldDivID = "fieldDiv"+fieldIndex;

	
	fields[fieldDivID] = {
        type: "open_text",
		title: ""
	};

	var fieldDiv = $("<div>")
		.addClass("item")
		.addClass("form-group")
		.attr("id", fieldDivID);

	var label = $("<label>")
		.addClass("col-form-label")
		.addClass("col-md-3")
		.addClass("col-sm-3")
		.addClass("label-align")
		.attr("for", fieldID)
		.text("Question *");
	fieldDiv.append(label);

	var inputDiv = $("<div>")
		.addClass("col-md-6")
		.addClass("col-sm-6");
	
	var field = $("<input>")
		.attr("type", "text")
		.addClass("form-control")
		.attr("placeholder", "Question")
		.attr("id",fieldID)
		.attr("required","required");
	
	var check = $("<input>")
		.addClass("item")
		.attr("type", "checkbox")
		.attr("id",fieldID);


	var optionListDiv = $("<div>")
		.attr("id", "OptionListDiv" + fieldIndex);

	var optionControlDiv = $("<div>")
		.addClass("item")
		.addClass("form-group")
		.attr("id", "OptionControlDiv" + fieldIndex);


	var buttonDiv = $("<div>")
		.addClass("col-md-2")
		.addClass("col-sm-2")
		.addClass("offset-md-1");

	var addButton = $("<button>")
		.addClass("btn btn-primary")
		.attr("onclick", "addAnswerOption(this.id)")
		.attr("id", "addOptionButton" + fieldIndex);
	addButton.html("add");

	buttonDiv.append(addButton);

	var choiseSelect = $("<select>")
		.addClass("form-control")
		.addClass("col-md-2")
		.addClass("col-sm-2")
        .addClass("offset-md-5")
        .attr("font", "16px")
		.attr("id", "choiseSelect" + fieldIndex);



	choiseSelect.html("Select type");

    var choiseOption1 = $("<option>");
    choiseOption1.html("Open text");

	var choiseOption2 = $("<option>");
	choiseOption2.html("Single-choice");

	var choiseOption3 = $("<option>");
	choiseOption3.html("Multiple-choice");


	choiseSelect.append(choiseOption1);
	choiseSelect.append(choiseOption2);
    choiseSelect.append(choiseOption3);

    choiseSelect.change (function () {
            const id = $(this).attr("id").slice("choiseSelect".length);
            if (document.getElementById("choiseSelect" + id).value === "Open text") {
                $("#OptionListDiv" + id).html("");
            }
        });

	optionControlDiv.append(choiseSelect);
    optionControlDiv.append(buttonDiv);

	check.change(function () {
            const parent_id = $(this).parent().attr("id");
            if ($(this).is(":checked")) {
                checked.push(parent_id);
            } else {
                const index = checked.indexOf(parent_id);
                if (index > -1) {
                    checked.splice(index, 1);
                }
            }
        }
    );
	
	inputDiv.append(field);
	fieldDiv.append(inputDiv);
	fieldDiv.append(check);
	

	$("#inquiry-fields").append(fieldDiv);
	$("#inquiry-fields").append(optionListDiv);
	$("#inquiry-fields").append(optionControlDiv);

	optionIndexes.push(0);
	index++;


}

const removeField = () => {
	checked.forEach(fieldID => {
		if(fieldID.includes("fieldDiv")){
			$("#" + fieldID).remove();
			fieldID =  fieldID.slice("fieldDiv".length);
			$("#OptionListDiv" + fieldID).remove();
			$("#OptionControlDiv" + fieldID).remove();
		}
		else if(fieldID.includes("OptionInputDiv")){
			$("#" + fieldID).remove();
		}
    });
    checked = [];
};

function addAnswerOption(buttonID){
	buttonID = buttonID.slice("addOptionButton".length);

	if(document.getElementById("choiseSelect" + buttonID).value === "Open text"){
        document.getElementById("choiseSelect" + buttonID).value = "Single-choice";
    }

	var label = $("<label>")
		.addClass("col-form-label")
		.addClass("col-md-4")
		.addClass("col-sm-4")
		.addClass("label-align")
		.text("Option *");

	var optionInputDiv = $("<div>")
		.addClass("item")
		.addClass("form-group")
		.addClass("offset-md-3")
		.attr("id", "OptionInputDiv" + buttonID + "_" + optionIndexes[buttonID]);

	optionIndexes[buttonID] = optionIndexes[buttonID] + 1;

	var inputDiv = $("<div>")
			.addClass("col-md-5")
			.addClass("col-sm-5");

	var optionField = $("<input>")
		.attr("type", "text")
		.addClass("form-control")
		.attr("placeholder", "Option")
		.attr("required","required");

	var check = $("<input>")
		.addClass("item")
		.attr("type", "checkbox");


	check.change(function () {
			const parent_id = $(this).parent().attr("id");
			if ($(this).is(":checked")) {
				checked.push(parent_id);
			} else {
				const index = checked.indexOf(parent_id);
				if (index > -1) {
					checked.splice(index, 1);
				}
			}
		}
	);

	inputDiv.append(optionField);
	optionInputDiv.append(label).append(inputDiv).append(check);


	$("#OptionListDiv" + buttonID).append(optionInputDiv);
}

function generatorSubmit(){

	var fieldsArr = [];
	Object.keys(fields).forEach(function (key) {
        if (this[key].type === "open_text"){
            this[key].title = $("#" + key).find("input[type='text']").val();
			fieldsArr.push(this[key]);
		}
    }, fields);

	var questions = [];
	for(var questionID = 0; questionID < index; questionID++){
		if(document.getElementById("fieldDiv" + questionID) !== null) {
			let type;
			let options  = [];
			for(var optionID = 0; optionID < optionIndexes[questionID]; optionID++){
				if(document.getElementById("OptionInputDiv" + questionID + "_" + optionID) !== null) {
					var option = $("#OptionInputDiv" + questionID + "_" + optionID).find("input[type='text']").val();
					options.push(option);
				}
			}
			if (options.length === 0){
				type = "open_text";
			}
			else{
				type = document.getElementById("choiseSelect" + questionID).value;
				if(type === "Single-choice"){
				    type = "single_choice";
                }
				else if(type === "Multiple-choice"){
                    type = "multiple_choice";
                }
                else if(type === "Open text"){
                    type = "open_text";
                }

			}
			var title = $("#fieldDiv" + questionID ).find("input[type='text']").val();
			question = {
				type: type,
				title: title,
				options: options
			};

			questions.push(question);
		}
	}

    const inquiryName = $("#input-form-name").val();

	const {backend} = window.glob;
	const owner = localStorage.getItem("username");
	const token = localStorage.getItem("token");



	if(!(owner && token && backend))
		return false;

	const inquiryJson = JSON.stringify({
		owner: owner,
		title: inquiryName,
		questions: questions
	});

	alert(inquiryJson);


	$.ajax({
		type: "POST",
		url: `${backend}/templates/create/`,
		data: inquiryJson,
		headers: {
			"Authorization": token
		},
		contentType: "application/json",
		dataType: "json",
		success: function (data) {
			refreshNavbar();
			console.log("template has been added with success ");
		},
		failure: function (errMsg) {
			console.log(errMsg);
		},
	});

    return false;
}

// function not used
function showDeadlinePicker(){
	var checkbox = $("#form-deadline-checkbox");
	var picker = $("#form-deadline-picker");

	if(checkbox.is(":checked")){
		picker.css("display", "block");
		$('#datetimepicker1').datetimepicker({format: "DD-MM-YYYY HH:mm"});
	}else{
		picker.css("display", "none");
	}
}

