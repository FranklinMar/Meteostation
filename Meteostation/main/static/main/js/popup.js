let text = "No file selected";
let form = document.getElementById("form");
let file = document.getElementById("file");

file.onchange = function() {
    let label = document.getElementById("label");

    if (this.files.length > 0) {
        label.innerHTML = `File name${ this.files.length > 1 ? "s" : "" }:&nbsp;`;
        for (let i = 0; i < this.files.length; i++) {
            label.innerHTML += `${this.files[i].name}`;
            if (this.files.length - i - 1 > 0) {
                label.innerHTML += ";&nbsp;&nbsp;"
            }
        }
        submit.style.display = "flex";
    } else {
        label.innerHTML = text;
    }
};

form.onsubmit = function() {
    file.disabled = "disabled";
    $('#label').fadeOut();
    $('#submit').fadeOut();
    $('.lds-dual-ring').fadeIn();//.style.display = "inline-block";
    document.querySelector(".lds-dual-ring").style.display = "inline-block";
    // this.submit();
};