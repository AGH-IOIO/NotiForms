function showGenerator(){
    $("#main").empty();
    $("#main").load("/production/generator.html");

    if(location.pathname !== "/dashboard")
        location.pathname = "/dashboard"
}

function showGroupGenerator(){
    $("#main").empty();
    $("#main").load("/production/groupgenerator.html");

    if(location.pathname !== "/dashboard")
        location.pathname = "/dashboard"
}

function showFormGenerator(){
    $("#main").empty();
    $("#main").load("/production/formgenerator.html");

    if(location.pathname !== "/dashboard")
        location.pathname = "/dashboard"
}

function showSummary(e){
	window.summaryJson = '{\
		"not_filled_yet": ["user1", "user2"],\
		"questions":[{"type": "open_text", "title": "Pytanie 1"},{"type": "open_text", "title": "Pytanie 2"}],\
		"answers": [{"username": "user3", "answers": ["Odp 1", "Odp 2"]},{"username": "user4", "answers": ["Odp 3", "Odp 4"]} ]\
	}';

	for(var i=0; i< window.glob.ownedForms.length; i++){
		console.log(window.glob.ownedForms[i])
		if(window.glob.ownedForms[i]["_id"] == e.id){
			window.summaryJson = JSON.stringify(window.glob.ownedForms[i])
			break;
		}
	}

    $("#main").empty();
    $("#main").load("/production/summary.html");
    if(location.pathname !== "/dashboard")
        location.pathname = "/dashboard"
}

function showMain(){
    $("#main").empty();
    $("#main").load("/production/main.html");

    if(location.pathname !== "/dashboard")
        location.pathname = "/dashboard"
}

function showForm(id) {
    $("#main").empty();
    $("#main").load("/production/uploadForm.html");
}