fields = []
let checked = []

console.log("TEST");
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
	
	var check = $("<input>")
		.attr("type", "checkbox")
		.attr("id",fieldID);
	
	check.change(function () {
            const parent_id = $(this).parent().attr("id")
            if ($(this).is(":checked")) {
                checked.push(parent_id);
            } else {
                const index = checked.indexOf(parent_id);
                if (index > -1) {
                    checked.splice(index, 1);
                }
            }
        }
    )
	
	inputDiv.append(field);
	fieldDiv.append(inputDiv);
	fieldDiv.append(check);
	

	$("#inquiry-fields").append(fieldDiv);

}

const removeField = () => {
	checked.forEach(fieldID => {
		$("#" + fieldID).remove();
        delete fields[fieldID];
    })

    checked = []
}

console.log(checked);

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