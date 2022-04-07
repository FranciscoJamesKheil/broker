// select option others
function changeFuncToilet() {
  var selectBox = document.getElementById("uiToilet");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  if (selectedValue == "others")
    document.getElementById("uiTextToilet").style.display = "block";
  else document.getElementById("uiTextToilet").style.display = "none";
}

function changeFuncPlumbing() {
  var selectBox = document.getElementById("uiPlumbing");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  if (selectedValue == "others")
    document.getElementById("uiTextPlumbing").style.display = "block";
  else document.getElementById("uiTextPlumbing").style.display = "none";
}

function changeFuncConduit() {
  var selectBox = document.getElementById("uiConduit");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  if (selectedValue == "others")
    document.getElementById("uiTextConduit").style.display = "block";
  else document.getElementById("uiTextConduit").style.display = "none";
}

function changeFuncWallFinish() {
  var selectBox = document.getElementById("uiWallFinish");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  if (selectedValue == "others")
    document.getElementById("uiTextWallFinish").style.display = "block";
  else document.getElementById("uiTextWallFinish").style.display = "none";
}

function changeFuncWindows() {
  var selectBox = document.getElementById("uiWindows");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  if (selectedValue == "others")
    document.getElementById("uiTextWindows").style.display = "block";
  else document.getElementById("uiTextWindows").style.display = "none";
}

function changeFuncCeiling() {
  var selectBox = document.getElementById("uiCeiling");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  if (selectedValue == "others")
    document.getElementById("uiTextCeiling").style.display = "block";
  else document.getElementById("uiTextCeiling").style.display = "none";
}

function changeFuncDoors() {
  var selectBox = document.getElementById("uiDoors");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  if (selectedValue == "others")
    document.getElementById("uiTextDoors").style.display = "block";
  else document.getElementById("uiTextDoors").style.display = "none";
}

function changeFuncFlooring() {
  var selectBox = document.getElementById("uiFlooring");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  if (selectedValue == "others")
    document.getElementById("uiTextFlooring").style.display = "block";
  else document.getElementById("uiTextFlooring").style.display = "none";
}

function changeFuncExtWalls() {
  var selectBox = document.getElementById("uiExtWalls");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  if (selectedValue == "others")
    document.getElementById("uiTextExtWalls").style.display = "block";
  else document.getElementById("uiTextExtWalls").style.display = "none";
}

function changeFuncRoofing() {
  var selectBox = document.getElementById("uiRoofing");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  if (selectedValue == "others")
    document.getElementById("uiTextRoofing").style.display = "block";
  else document.getElementById("uiTextRoofing").style.display = "none";
}

function changeFuncFraming() {
  var selectBox = document.getElementById("uiRoofFraming");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  if (selectedValue == "others")
    document.getElementById("uiTextRoofFraming").style.display = "block";
  else document.getElementById("uiTextRoofFraming").style.display = "none";
}

function changeFuncClassification() {
  var selectBox = document.getElementById("uiClassification");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  if (selectedValue == "others")
    document.getElementById("uiTextClassification").style.display = "block";
  else document.getElementById("uiTextClassification").style.display = "none";
}

function changeFuncBrgy() {
  var selectBox = document.getElementById("uiBrgy");
  var selectedValue = selectBox.options[selectBox.selectedIndex].value;
  if (selectedValue == "others")
    document.getElementById("uiTextBrgy").style.display = "block";
  else document.getElementById("uiTextBrgy").style.display = "none";
}
