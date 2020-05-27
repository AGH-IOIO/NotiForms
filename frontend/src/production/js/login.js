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
    url: `${backend}/token/`,
    data: jsonString,
    contentType: "application/json",
    dataType: "json",
    success: function (data) {
      console.log(data["token"]);
      localStorage.setItem("token", data["token"]);
      localStorage.setItem("username", login);
      location.href = "/dashboard";
      showLoginInfo("Logged in", false);
    },
    error: function (data){
      showLoginInfo(data.responseJSON.error, true);
    },
    failure: function (errMsg) {
      showLoginInfo("Login error: "+errMsg, true);
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
    url: `${backend}/users/`,
    data: jsonString,
    contentType: "application/json",
    dataType: "json",
    success: function (data) {
      showLoginInfo("Registration completed successfully, please check your email", false);
      $("#register-input-login").val("");
      $("#register-input-password").val("");
      $("#register-input-email").val("");
    },
    failure: function (errMsg) {
      console.log(errMsg);
    },
    error: function (data) {
      showLoginInfo(data.responseJSON.error, true);
    }
  });

  return false;
}

function showLoginInfo(message, isError){
  $(".alert").remove();
  let box = $("<div>").addClass("alert")
    .css("position", "absolute")
    .css("top", 0).css("left", 0).css("right", 0)
    .append($("<strong>").text(message).css("color","white"));

  if(isError){
    box.addClass("alert-danger");
  }else{
    box.addClass("alert-success");
  }
  box.hide();
  $("body.login").prepend(box);
  box.fadeIn(300);

  setTimeout(function () { box.fadeOut(300); }, 3000)
}
