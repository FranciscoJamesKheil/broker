function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/home";
  });
}

function logout_alert() {
  Swal.fire({
    text: "Confirmation to Signin out?",
    showCancelButton: true,
    confirmButtonText: "Confirm",
    confirmButtonColor: "#ce0000",
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.href = "/logout";
    }
  });
}

$(function () {
  $('[data-toggle="tooltip"]').tooltip();
});

function contact_alert(x) {
  Swal.fire({
    confirmButtonText: "OK",
    title: "Contact Number",
    text: x,
    confirmButtonColor: "#009db9",
  });
}

// https://youtu.be/etfECjhaP-g
// Dark Mode

let darkMode = localStorage.getItem("darkMode");
const darkModeToggle = document.querySelector("#dark");

const enableDarkMode = () => {
  //add class darkmode to the body
  document.body.classList.add("darkMode");
  //update darkmode in the localstorage
  localStorage.setItem("darkMode", "enabled");
};
const disableDarkMode = () => {
  //add class darkmode to the body
  document.body.classList.remove("darkMode");
  //update darkmode in the localstorage
  localStorage.setItem("darkMode", null);
};

if (darkMode === "enabled") {
  enableDarkMode();
  document.getElementById("sun").style = "display: block";
  document.getElementById("moon").style = "display: none";
} else {
  document.getElementById("sun").style = "display: none";
  document.getElementById("moon").style = "display: block";
}

darkModeToggle.addEventListener("click", () => {
  darkMode = localStorage.getItem("darkMode");
  if (darkMode != "enabled") {
    enableDarkMode();
    document.getElementById("sun").style = "display: block";
    document.getElementById("moon").style = "display: none";
  } else {
    disableDarkMode();
    document.getElementById("sun").style = "display: none";
    document.getElementById("moon").style = "display: block";
  }
});

// Show / Hide password
$(".toggle-password1").click(function () {
  $(this).toggleClass("fa-eye fa-eye-slash");
  var input = $($(this).attr("toggle"));
  if (input.attr("type") == "password") {
    input.attr("type", "text");
  } else {
    input.attr("type", "password");
  }
});

// Show / Hide password
$(".toggle-password2").click(function () {
  $(this).toggleClass("fa-eye fa-eye-slash");
  var input = $($(this).attr("toggle"));
  if (input.attr("type") == "password") {
    input.attr("type", "text");
  } else {
    input.attr("type", "password");
  }
});

/* when a user clicks, toggle the 'is-animating' class */
$(".heart").on("click touchstart", function () {
  $(this).toggleClass("is_animating");
});

/*when the animation is over, remove the class*/
$(".heart").on("animationend", function () {
  $(this).toggleClass("is_animating");
});

function isNumberKey(evt) {
  var charCode = evt.which ? evt.which : evt.keyCode;
  if (charCode != 46 && charCode > 31 && (charCode < 48 || charCode > 57))
    return false;

  return true;
}
