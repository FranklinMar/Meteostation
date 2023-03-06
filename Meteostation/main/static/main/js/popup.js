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

/*form.onsubmit = function() {
    file.disabled = "disabled";
    $('#label').fadeOut();
    $('#submit').fadeOut(function (){
        $('.lds-dual-ring').fadeIn();//.style.display = "inline-block";
        document.querySelector(".lds-dual-ring").style.display = "inline-block";
    });
    *if (window.FormData !== undefined) {
        event.preventDefault();
        let formData = new FormData(this);
        let xhr = new XMLHttpRequest();
        xhr.open('POST', $(this).attr('action'), true);
        xhr.setRequestHeader('X-REQUESTED-WITH', 'XMLHttpRequest')
        xhr.onreadystatechange = function() {
            if(xhr.readyState === 4) {
                if(xhr.status === 200) {
                    result = JSON.parse(xhr.responseText);
                    // Code for success upload
                }
                else {
                    // Code for error
                }
            }
        };
        xhr.send(formData);
    }*
    this.submit();
};*/