function loginSubmit() {
  var login = $("#login-input-login").val();
  var password = $("#login-input-password").val();
  var jsonString = JSON.stringify({
    username: login,
    password: password,
  });

  localStorage.setItem("username", login);

  $.ajax({
    type: "POST",
    url: "http://localhost:8080/token/",
    data: jsonString,
    contentType: "application/json",
    dataType: "json",
    success: function (data) {
      console.log(data["token"]);
      localStorage.setItem("token", data["token"]);
      alert("udalo sie zalogowac");
      location.href = "/dashboard";
    },
    failure: function (errMsg) {
      console.log(errMsg);
    },
  });

  return false;
}

function registerSubmit() {
  var login = $("#register-input-login").val();
  var password = $("#register-input-password").val();
  var email = $("#register-input-email").val();
  var jsonString = JSON.stringify({
    username: login,
    password: password,
    email: email,
  });

  $.ajax({
    type: "POST",
    url: "http://localhost:8080/users/",
    data: jsonString,
    contentType: "application/json",
    dataType: "json",
    success: function (data) {
      alert("Udalo sie zarejestrowac");
    },
    failure: function (errMsg) {
      console.log(errMsg);
    },
  });

  return false;
}
