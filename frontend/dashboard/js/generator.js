fields = []

function addTextField(){

	var fieldIndex = fields.length;
	var fieldID = "field"+fieldIndex;

	fields.push({
		type: "open_text",
		question: ""
	});

	var field = $("<input>")
		.attr("type", "text")
		.addClass("form-control")
		.attr("placeholder", "Question")
		.attr("id",fieldID)
		.attr("required","required");

	$("#inquiry-fields").append(field);

}

function removeField(){
	if(fields.length > 0){
		var fieldID = "field"+(fields.length-1);
		$("#"+fieldID).remove();
		fields.pop();
	}
}

function generatorSubmit(){
	if(fields.length > 0){

		//set questions
		for(var i=0; i<fields.length; i++){
			if(fields[i].type == "open_text"){
				fields[i].question = $("#field"+i).val();
			}
		}

		var inquiryName = $("#input-inquiry-name").val();
		var inquiry = {
			name: inquiryName,
			questions: fields
		};

		alert(JSON.stringify(inquiry));
	}
	return false;
}

$(document).ready(function (){

	$("#button-add-text").click(addTextField);
	$("#button-remove-field").click(removeField);
});