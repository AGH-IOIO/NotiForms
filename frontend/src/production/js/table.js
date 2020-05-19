function loadFormGenerator() {
    loadSelectForm('#form-template-dropdown', window.glob.templates, t => t.title);
    loadSelectForm('#form-team-dropdown', window.glob.teams, t => t);
}

function loadSelectForm(id, values, fetch) {
    const addOption = (t) => $(id).append($('<option>', {value: fetch(t), text: fetch(t)}));
    if (values) {
        values.map(t => addOption(t));
    }
}

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

    const owner = localStorage.getItem("username");

    if (!owner)
        return false;

    $('.email').each(function (index) {
        emails.push($(this).text())
    })

    const group = {
        name: $('#group_name').val(),
        members: emails,
        owner: owner
    }

    const groupJson = JSON.stringify(group);

    alert(groupJson);

    const {backend} = window.glob;

    $.ajax({
        type: "POST",
        url: `${backend}/teams/create_team/`,
        data: groupJson,
        contentType: "application/json",
        dataType: "json",
        success: function (data) {
            alert("udalo sie utworzyc grupe");
            location.href = "/dashboard";
        },
        failure: function (errMsg) {
            console.log(errMsg);
        },
    });

    return false;
}

function submitForm() {

    const team = $("#form-team-dropdown").val();
    const template = $("#form-template-dropdown").val();
    const owner = localStorage.getItem("username");
    const token = localStorage.getItem("token");
    const {backend} = window.glob;

    if (!(owner && token && backend))
        return false;

    const formJson = JSON.stringify({
        team: team,
        owner: owner,
        template_title: template,
        deadline: ""
    });

    alert(formJson);


    // $.ajax({
    //     type: "POST",
    //     url: `${backend}/templates/assign/`,
    //     data: formJson,
    //     headers: {
    //         "Authorization": token
    //     },
    //     contentType: "application/json",
    //     dataType: "json",
    //     success: function (data) {
    //         alert("udalo sie utworzyc grupe");
    //         location.href = "/dashboard";
    //     },
    //     failure: function (errMsg) {
    //         console.log(errMsg);
    //     },
    // });

    return false;
}

function refreshNavbar() {
    token = localStorage.getItem("token");
    username = localStorage.getItem("username");
    teamsApiCall(username, token);
    templatesApiCall(username, token);
}

function teamsApiCall(username, token) {

    const {backend} = window.glob;

    if (token && username && backend) {
        $.ajax({
            type: "GET",
            url: `${backend}/users/get_teams/${username}/`,
            headers: {
                "Authorization": token
            },
            success: function (data) {
                if (data.teams) {
                    window.glob.teams = data.teams;
                    refreshTeams(data.teams);
                }
            },
            failure: function (errMsg) {
                console.log(errMsg);
            },
        });
    }
}

function templatesApiCall(username, token) {

    const {backend} = window.glob;

    $.ajax({
        type: "GET",
        url: `${backend}/templates/get_templates/${username}/`,
        headers: {
            "Authorization": token
        },
        contentType: "application/json",
        dataType: "json",
        success: function (data) {
            if (data.templates) {
                window.glob.templates = data.templates
                refreshTemplates(data.templates);
            }
        },
        failure: function (errMsg) {
            console.log(errMsg);
        },
    });
}

function refreshTemplates(templates) {
    $('#template-list').empty();
    templates.map(t => addNavBarTemplate(t));
}

function addNavBarTemplate(t) {
    $('#template-list').append(
        $('<li>').append(
            $('<a>')
                .text(t.title)
        )
    );
}

function refreshTeams(teams) {
    $('#group_list > .custom').remove();
    teams.map(t => addNavBarItem(t));
}

function addNavBarItem(teamName) {
    const li = $('#list_template').clone(true, true);
    li.css('display', '');
    li.addClass('custom');
    li.find('#title').text(teamName);
    $("#group_list").append(li);
}