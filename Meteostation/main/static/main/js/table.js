
let submit = document.getElementById("submit");
let entries = document.getElementById("entries");
let show = document.getElementById("show");

let data_table = document.getElementById("dataTable");

// let paginator = document.getElementById("paginator");
let paginator_buttons = document.getElementById("paginator-buttons");
let prev = document.getElementById("prev");
let next = document.getElementById("next");


show.change_show = function (from, to, entries, filter=null) {
    this.innerText = `Showing ${from} to ${to} of ${entries} entries ${filter == null ? "" : filter}`;
};

let page = 0;
let entry_num = 10;
let rows_tr = document.querySelectorAll("tbody tr.filler")//document.querySelectorAll("tbody tr");


function hideRows() {
    let rows = document.querySelectorAll("tbody tr:not(.filler) ");

    for (let i = page * entry_num; i < Math.min((page + 1) * entry_num, rows.length); i++) {
        rows[i].removeAttribute("style");
    }
    /*let last = document.querySelector("tbody .last")
    if (last) {
        last.classList.remove("last");
    }*/
    document.querySelector("tbody .last")?.classList.remove("last");
}

function check() {
    //rows_tr = document.querySelectorAll("tbody tr");
    let array = document.querySelectorAll("tbody tr.filler")
    if (document.querySelectorAll("tbody tr:not(.filler)").length === 0) {
        let array = document.querySelectorAll("tbody tr.filler");
        console.log("What?");
        for (let i = 0; i < array.length; i++) {
            array[i].parentNode.removeChild(array[i]);
        }
        let row = document.createElement("tr");
        data_table.getElementsByTagName('tbody')[0].appendChild(row);
        row.classList.add("filler");
        row.classList.add("last");
        row.innerHTML = `<td colspan='${data_table.getElementsByTagName("th").length}'>No data available in table</td>`;
        return false;
    }
    return true;
}

function revealRows() {
    rows_tr = document.querySelectorAll("tbody tr");
    if (rows_tr.length !== 0) {
        let rows_num = Math.min((page + 1) * entry_num, rows_tr.length);
        for (let i = page * entry_num; i < rows_num; i++) {
            rows_tr[i].style.display = "table-row";
        }
        rows_tr[rows_num - 1].classList.add("last");
        let rows = document.querySelectorAll("tbody tr:not(.filler) ");

        show.change_show((rows.length) === 0 ? 0 : (page * entry_num) + 1, Math.min((page + 1) * entry_num, rows.length), rows.length);
    }
}

function changePaginatorButtons() {
    //rows_tr = document.querySelectorAll("tbody tr");
    let array = paginator_buttons.querySelectorAll("li");
    let last_page = Math.ceil(rows_tr.length / entry_num);
    for (let i of array) {
        i.removeAttribute("class");
    }
    if (last_page > 7) {
        if (page < 4) {
            for (let i = 1; i <= 7 - 2; i++) {
                array[i - 1].innerText = i.toString();
                if (page === i - 1) {
                    array[i - 1].classList.add("active");
                }
            }

            array[5].innerText = "...";
            array[5].classList.add("disabled");
        } else if (page >= (last_page - 4)) {

            for (let i = last_page - 4, j = 2; j < 7; i++, j++) {
                array[j].innerText = i.toString();
                if (page === (i - 1)) {
                    array[j].classList.add("active");
                }
            }
            array[1].innerText = "...";
            array[1].classList.add("disabled");
        } else {
            array[1].innerText = "...";
            array[1].classList.add("disabled");
            array[5].innerText = "...";
            array[5].classList.add("disabled");

            array[2].innerText = page.toString();
            array[3].innerText = (page + 1).toString();
            array[3].classList.add("active");
            array[4].innerText = (page + 2).toString();
        }
    } else {
        for (let i = 1; i <= array.length; i++) {
            array[i - 1].innerText = i.toString();
            if (page === (i - 1)) {
                array[i - 1].classList.add("active");
            }
        }
    }

    if (last_page === 1) {
        next.classList.add("disabled");
        prev.classList.add("disabled");
    } else {
        if (page !== last_page - 1) {
            next.classList.remove("disabled");
        } else {
            next.classList.add("disabled");
        }

        if (page !== 0) {
            prev.classList.remove("disabled");
        } else {
            prev.classList.add("disabled");
        }
    }
}

function paginateHandler() {
    //rows_tr = document.querySelectorAll("tbody tr");
    hideRows();
    page = Number(this.innerText) - 1;
    revealRows();
    changePaginatorButtons();
}

entries.onchange = function() {
    //rows_tr = document.querySelectorAll("tbody tr");
    hideRows();
    page = 0;
    entry_num = this.options[this.selectedIndex].value;
    if (check()) {
        revealRows();
    }

    paginator_buttons.innerHTML = "";
    let buttons_num = rows_tr.length / entry_num;
    if (buttons_num === 0) {
        next.classList.add("disabled");
    } else {
        let li = null;
        for (let i = 1; i <= Math.min(Math.ceil(buttons_num), 7); i++) {
            li = document.createElement("li");
            if (i === 1) {
                li.innerText = i.toString();
            }
            li.onclick = paginateHandler;
            paginator_buttons.appendChild(li);
        }
        li.innerText = Math.ceil(buttons_num).toString();
        changePaginatorButtons();
    }
};


prev.onclick = function() {
    //rows_tr = document.querySelectorAll("tbody tr");
    if (page !== 0) {
        hideRows()
        page--;
        revealRows();
        changePaginatorButtons();
    }
}

next.onclick = function() {
    //rows_tr = document.querySelectorAll("tbody tr");
    if (page !== Math.ceil(rows_tr.length / entry_num - 1)) {
        hideRows()
        page++;
        revealRows();
        changePaginatorButtons();
    }
}
let ths = data_table.querySelectorAll("thead tr th");
//console.log(ths);

function sortHandler() {
    let order = true;
    if (this.classList.contains("sorting-asc")) {
        this.classList.remove("sorting-asc");
        this.classList.add("sorting-desc");
        order = false;
    } else if (this.classList.contains("sorting-desc")) {
        this.classList.remove("sorting-desc");
        this.classList.add("sorting-asc");
    } else {
        data_table.querySelector("thead tr th.sorting-asc")?.classList.remove("sorting-asc");
        data_table.querySelector("thead tr th.sorting-desc")?.classList.remove("sorting-desc");
        this.classList.add("sorting-asc");
    }
    //hideRows();
    sort(rows_tr, order, Number(this.getAttribute("data-column")));
    //revealRows();
}

function swap(items, leftIndex, rightIndex) {
    /*let temp = items[leftIndex];
    items[leftIndex] = items[rightIndex];
    items[rightIndex] = temp;*/
    let temp = items[leftIndex].innerHTML;
    items[leftIndex].innerHTML = items[rightIndex].innerHTML;
    items[rightIndex].innerHTML = temp;
    //items[leftIndex].parentNode.insertBefore(items[rightIndex], items[leftIndex]);
}
let regex = new RegExp("[0-9]{2} [A-Za-z]{3} [0-9]{4} [0-9]{2}:[0-9]{2}");
function partition(items, left, right, order, column_num) {
    let pivot = items[Math.floor((right + left) / 2)].getElementsByTagName("td")[column_num],
        i = left,
        j = right,
        templ,
        tempr;
    while (i <= j) {
        //if (order) {
            while (true) {
                templ = items[i].getElementsByTagName("td")[column_num].innerText;
                tempr = pivot.innerText;
                if (regex.test(templ) || regex.test(tempr)) {
                    templ = Date.parse(templ);
                    tempr = Date.parse(tempr);
                }
                if ((templ < tempr && order) || (templ > tempr && !order)) {
                    i++;
                } else {
                    break;
                }
            }
        /*} else {
            while (true) {
                if (Date.parse(items[i].getElementsByTagName("td")[column_num].innerText) > Date.parse(pivot.innerText)) {
                    i++;
                } else {
                    break;
                }
            }
        }*/

        //if (order) {
            while (true) {
                templ = items[j].getElementsByTagName("td")[column_num].innerText;
                tempr = pivot.innerText;
                if (regex.test(templ) || regex.test(tempr)) {
                    templ = Date.parse(templ);
                    tempr = Date.parse(tempr);
                }
                if ((templ > tempr && order) || (templ < tempr && !order)) {
                    j--;
                } else {
                    break;
                }
            }
        /*} else {
            while (true) {
                if (Date.parse(items[j].getElementsByTagName("td")[column_num].innerText) < Date.parse(pivot.innerText)) {
                    j--;
                } else {
                    break;
                }
            }
        }*/

        if (i <= j) {
            /*console.log(`Pivot: ${pivot}, leftIndex: ${i}, rightIndex: ${j}, leftIndexValue: ${
                items[i].getElementsByTagName("td")[column_num].innerText}, rightIndexValue ${items[j].getElementsByTagName("td")[column_num].innerText}`)*/
            swap(items, i, j);
            i++;
            j--;
        }
    }
    return i;
}

function quickSort(items, left, right, order, column_num) {
    let index;

    if (items.length > 1) {
        index = partition(items, left, right, order, column_num);

        if (left < index - 1) {
            quickSort(items, left, index - 1, order, column_num);
        }

        if (index < right) {
            quickSort(items, index, right, order, column_num);
        }
    }

    //return items;
}

function sort(array, order, column_num) {
    //console.log(column_num);
    //console.log(order);
    page = 0;
    quickSort(array, 0, array.length - 1, order, column_num)
    //console.log(array);
}

/*function sort(column_num, order) {
    let switching = true, should_switch, rows, x, y, i;
    rows = data_table.querySelectorAll("tbody tr");

    while (switching) {
        switching = false;

        for (i = 0; i < (rows.length - 1); i++) {
            should_switch = false;

            x = rows[i].getElementsByTagName("td")[column_num];
            y = rows[i + 1].getElementsByTagName("td")[column_num];
            if ((!order && x.innerText.toLowerCase() > y.innerText.toLowerCase()) ||
                (order && x.innerText.toLowerCase() < y.innerText.toLowerCase())) {
                should_switch = true;
                break;
            }
        }
        if (should_switch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            let temp = rows[i];
            rows[i] = rows[i + 1];
            rows[i + 1] = temp;
        }
    }
}*/

for (let i = 0; i < ths.length; i++) {
    ths[i].setAttribute('data-column', i.toString());
    ths[i].onclick = sortHandler;
}

//ths[0].classList.add("sorting-asc");
//sort(0, false);
entries.onchange(null);
ths[0].onclick(null);
/*let array = [1, 4, 7, 2, 6];
console.log(array);
console.log(quickSort(array, 0, array.length - 1, true));
console.log(quickSort(array, 0, array.length - 1, false));*/
/*for (let i of data_table.querySelectorAll("thead tr th")) {
    i.innerHTML += down_arrow + up_arrow;
}*/
