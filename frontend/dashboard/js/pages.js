var pages = {
	"nav-login": "login-page",
	"nav-generator": "generator-page"
};

function switchPage(page){
	for (var i in pages) {
		setPageVisibility(pages[i], false);
	}
	setPageVisibility(page, true);
}

function setPageVisibility(page, display){
	$("#"+page).css("display",display?"block":"none");
	console.log(page,display?"block":"none");
}

$(document).ready(function () {
	$(".nav-link").click(function (element) {
		var clicked = element.target.id
		switchPage(pages[clicked]);
		
	});

	switchPage("login-page");
});