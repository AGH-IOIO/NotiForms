function loginSubmit() {
  var login = $("#input-login").val();
  var password = $("#input-password").val();
  var jsonString = JSON.stringify({
    username: login,
    password: password,
  });

  $.ajax({
    type: "POST",
    url: "http://localhost:8080/token/",
    data: jsonString,
    contentType: "application/json",
    dataType: "json",
    success: function (data) {
      console.log(data["token"]);
      localStorage.setItem("token", data["token"]);
    },
    failure: function (errMsg) {
      alert(errMsg);
    },
  });

  return false;
}
