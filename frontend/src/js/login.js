function loginSubmit(){
	var login = $("#input-login").val();
	var password = $("#input-password").val();
	var jsonString = JSON.stringify({login: login, password:password});
	alert(jsonString);
	return false;
}