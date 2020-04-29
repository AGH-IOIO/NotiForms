const fields = {}
let checked = []

let index = 0

function addTextField() {

    const fieldIndex = index;
    const fieldID = "field" + fieldIndex;
    

    fields[fieldID] = {
        type: "open_text",
        question: ""
    };

    const field = $("<input>")
        .attr("type", "text")
        .addClass("form-control")
        .attr("placeholder", "Question")
        .attr("required", "required");


    const box = $("<div>").addClass("box").attr("id", fieldID)

    const check = $("<input>").attr("type", "checkbox")

    check.change(function () {
            const parent_id = $(this).parent().attr("id")
            if ($(this).is(":checked")) {
                checked.push(parent_id)
            } else {
                const index = checked.indexOf(parent_id);
                if (index > -1) {
                    checked.splice(index, 1);
                }
            }
        }
    )

    box.append(check)
    box.append(field)

    $("#inquiry-fields").append(box);

    index++
}

const removeField = () => {
	checked.forEach(fieldID => {
        $("#" + fieldID).remove();
        delete fields[fieldID];
    })

    checked = []
}

const generatorSubmit = () => {

    Object.keys(fields).forEach(function (key) {
        if (this[key].type === "open_text")
            this[key].question = $("#" + key).find("input[type='text']").val();
    }, fields);

    const inquiryName = $("#input-inquiry-name").val();
    const inquiry = {
        name: inquiryName,
        questions: fields
    };


    alert(JSON.stringify(inquiry));
    return false;
}
