var pages = {
  "nav-login": "login.html",
  "nav-register": "register.html",
  "nav-generator": "generator.html",
};

function switchPage(page) {
  $("#main").empty();
  $("#main").load(page);
}


$(document).ready(function () {
  $(".nav-link").click(function (element) {
    var clicked = element.target.id;
    switchPage(pages[clicked]);
  });


  var path = location.href.replace(location.origin,'');

  if(path == "/"){
    if(localStorage.getItem("logged") != "ok"){
      console.log("not logged")
      location.href="/login";
    }else{
      console.log("logged")
      location.href="/dashboard";
    }
  }
  else if(path == "/login"){
    switchPage("/login.html");
  }
  else if(path == "/register"){
    switchPage("/register.html");
  }
  else if (path == "/dashboard"){
    switchPage("/generator.html");
  }
});
