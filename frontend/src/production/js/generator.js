fields = []

function addTextField(){

	var fieldIndex = fields.length;
	var fieldID = "field"+fieldIndex;
	var fieldDivID = "fieldDiv"+fieldIndex;

	fields.push({
		type: "open_text",
		title: "",
		answer: ""
	});

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
	inputDiv.append(field);
	fieldDiv.append(inputDiv);

	$("#inquiry-fields").append(fieldDiv);

}

function removeField(){
	if(fields.length > 0){
		var fieldID = "fieldDiv"+(fields.length-1);
		$("#"+fieldID).remove();
		fields.pop();
	}
}

function generatorSubmit(){
	if(fields.length > 0){

		//set questions
		for(var i=0; i<fields.length; i++){
			if(fields[i].type == "open_text"){
				fields[i].title = $("#field"+i).val();
			}
		}

		var inquiryName = $("#input-form-name").val();
		var inquiry = {
			title: inquiryName,
			questions: fields
		};

		alert(JSON.stringify(inquiry));
	}
	return false;
}

function showDeadlinePicker(){
	var checkbox = $("#form-deadline-checkbox");
	var picker = $("#form-deadline-picker")

	if(checkbox.is(":checked")){
		picker.css("display", "block");
		$('#datetimepicker1').datetimepicker({format: "DD-MM-YYYY HH:mm"});
	}else{
		picker.css("display", "none");
	}
}