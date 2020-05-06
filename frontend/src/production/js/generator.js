fields = {}
checked = []

let index = 0;


function addTextField(){

	var fieldIndex = index;
	var fieldID = "field"+fieldIndex;
	var fieldDivID = "fieldDiv"+fieldIndex;

	
	fields[fieldDivID] = {
        type: "open_text",
		title: "",
		answer: ""
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
	index++;
}

const removeField = () => {
	checked.forEach(fieldID => {
		$("#" + fieldID).remove();
		var id = parseInt(fieldID.slice(8));
		delete fields[fieldID];
    })

    checked = []
}

function generatorSubmit(){
	var fieldsArr = [];
	Object.keys(fields).forEach(function (key) {
        if (this[key].type === "open_text"){
            this[key].title = $("#" + key).find("input[type='text']").val();
			fieldsArr.push(this[key])
		}
    }, fields);

    const inquiryName = $("#input-form-name").val();
    const inquiry = {
        title: inquiryName,
        questions: fieldsArr
    };


    alert(JSON.stringify(inquiry));
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

