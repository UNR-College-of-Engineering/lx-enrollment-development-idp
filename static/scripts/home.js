specialChars = "<>@!#$%^&*()_+[]{}?:;|'\"\\,./~`-="
var form = document.getElementById("username");
var special = document.getElementById("special");
var space = document.getElementById("space");
var len3 = document.getElementById("len3");
var uniq = document.getElementById("uniq");
var startnum = document.getElementById("startnum");

function validateForm() {
    var username = form.value;
    let specialInString = username.split("").some(c => specialChars.includes(c))
    let spaceInString = username.includes(" ");
    let len3InString = username.length < 3;
    let startsWithNum = username.match(/^\d/);
    if (specialInString) {
        special.setAttribute("class", "badge bg-danger smooth")
    } else {
        special.setAttribute("class", "badge bg-success smooth")
    }
    if (spaceInString) {
        space.setAttribute("class", "badge bg-danger smooth")
    } else {
        space.setAttribute("class", "badge bg-success smooth")
    }
    if (len3InString) {
        len3.setAttribute("class", "badge bg-danger smooth")
    } else {
        len3.setAttribute("class", "badge bg-success smooth")
    }
    if (startsWithNum) {
        startnum.setAttribute("class", "badge bg-danger smooth")
    }
    else {
        startnum.setAttribute("class", "badge bg-success smooth")
    }
}

function checkUnique() {
    console.log("uniq");
}