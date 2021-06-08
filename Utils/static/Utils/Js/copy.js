function myFunction() {
  /* Get the text field */
  var copyText = document.getElementById("myInput");

  /* Select the text field */
  copyText.select();
  copyText.setSelectionRange(0, 99999); /* For mobile devices */

  /* Copy the text inside the text field */
  document.execCommand("copy");
  alert("Copied To ClipBoard!!");
}

$(document).ready(function () {
  $("#copy").click(function () {
    $(this).attr("title", "Copied");
  });
});

$(document).ready(function () {
  $("#copy").click(function (e) {
    e.preventDefault();
    e.stopPropagation();
    e.stopImmediatePropagation();
    return false;
  });
});
