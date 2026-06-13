function mouseDown(word) {
  if (document.getElementById("role")){
    document.getElementById("role").innerHTML = word;
  }
}

function mouseUp() {
  if (document.getElementById("role")){
    document.getElementById("role").innerHTML = "";
  }
}
