function addParticipant() {

    const table = $('#participantsTable')

    const fieldDiv = $("<tr>").append(
        $('<td>').append($('<input>')
            .attr('type', 'checkbox')
            .attr('class', 'check_participant')
        ),
        $('<td>').text(""),
        $('<td>')
            .attr('class', 'email')
            .text($('#participant_email').val())
    )

    table.append(fieldDiv)
}

function deleteSelected() {
    console.log('selected')

    let counter = 0;

    $('.check_participant').each(function (index) {

        if ($(this).prop('checked') == true) {

            const updated_index = index - counter + 1
            document.getElementById("participantsTable").deleteRow(updated_index);
            counter++;
        }
    })
}

function setAll(e) {
    $('.check_participant').prop('checked', e.checked);
}

function submitGroup() {

    const emails = [];

    $('.email').each(function (index) {
        emails.push($(this).text())
    })

    const group = {
        name: $('#group_name').val(),
        members: emails,
    }

    alert(JSON.stringify(group));
    return false;
}

function submitFrom() {

    const emails = [];

    $('.email').each(function (index) {
        emails.push($(this).text())
    })

    var deadline = ""
    var checkbox = $("#form-deadline-checkbox");
    var picker = $("#form-deadline-input")

    if (checkbox.is(":checked")) {
        deadline = picker.val();
    }

    const group = {
        name: $('#group_name').val(),
        template: $("#form_template").val(),
        participants: emails,
        deadline: deadline
    }

    alert(JSON.stringify(group));
    return false;
}