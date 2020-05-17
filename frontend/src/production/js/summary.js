function insertQuestionResults(index){
	//alert(summaryData.questions[index].type)
	let entry = $('<a class="panel-heading" role="tab" id="heading'+index+'" data-parent="#collapse'+index+'" href="javascript:;" aria-expanded="true" aria-controls="collapseNotYet" onclick="collapse(this)">\
      <h4 class="panel-title">'+summaryData.questions[index].title+'</h4>\
    </a>\
\
      <div id="collapse'+index+'" class="panel-collapse collapse in" role="tabpanel" aria-labelledby="headingOne">\
      <div class="panel-body">\
        <table class="table table-bordered">\
           <thead>\
              <tr>\
                 <th>Username</th>\
                 <th>Odpowiedź</th>\
              </tr>\
           </thead>\
           <tbody id="table'+index+'">\
              \
           </tbody>\
        </table>\
     </div>\
    </div>');

    let answerTable = entry.find("#table"+index);
    for(var i=0; i<summaryData.answers.length; i++){
    	let row = $("<tr>");
    	let username = $("<td>");
    	let answer = $("<td>");
    	username.text(summaryData.answers[i].username);
    	answer.text(summaryData.answers[i].answers[index]);

    	row.append(username);
    	row.append(answer);
    	answerTable.append(row);
    }

	summaryDiv.append(entry);

}

function collapse(elem) {
	let id = $(elem).attr("data-parent");
	$(id).toggleClass("show");
}

let summaryDiv = $("#summary");
let summaryData = JSON.parse(window.summaryJson);

if(summaryData.not_filled_yet.length > 0){
	let notYetTable = $("#notYetTable");
	for(var i=0; i<summaryData.not_filled_yet.length; i++){
		let row = $("<tr>");
		let col = $("<td>");
		col.text(summaryData.not_filled_yet[i]);
		row.append(col);
		notYetTable.append(row);
	}
}else{

	$("#headingNotYet").remove();
	$("#collapseNotYet").remove();
}

if(summaryData.answers.length > 0){
	for(var i=0; i<summaryData.questions.length; i++){
		insertQuestionResults(i);
	}
}
