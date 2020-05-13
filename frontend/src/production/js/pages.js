function showGenerator(){
    $("#main").empty();
    $("#main").load("/production/generator.html");
}

function showGroupGenerator(){
    $("#main").empty();
    $("#main").load("/production/groupgenerator.html");
}

function showFormGenerator(){
    $("#main").empty();
    $("#main").load("/production/formgenerator.html");
}

function showSummary(e){
	window.summaryJson = '{\
		"not_filled_yet": ["user1", "user2"],\
		"questions":[{"type": "open_text", "title": "Pytanie 1"},{"type": "open_text", "title": "Pytanie 2"}],\
		"answers": [{"username": "user3", "answers": ["Odp 1", "Odp 2"]},{"username": "user4", "answers": ["Odp 3", "Odp 4"]} ]\
	}';

    $("#main").empty();
    $("#main").load("/production/summary.html");
}