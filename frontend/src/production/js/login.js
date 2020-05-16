function loginSubmit() {
  var login = $("#login-input-login").val();
  var password = $("#login-input-password").val();
  var jsonString = JSON.stringify({
    username: login,
    password: password,
  });

  const {backend} = window.glob;

  $.ajax({
    type: "POST",
    url: `http://${backend}/token/`,
    data: jsonString,
    contentType: "application/json",
    dataType: "json",
    success: function (data) {
      console.log(data["token"]);
      localStorage.setItem("token", data["token"]);
      localStorage.setItem("username", login);
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

  const {backend} = window.glob;

  $.ajax({
    type: "POST",
    url: `http://${backend}/users/`,
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
