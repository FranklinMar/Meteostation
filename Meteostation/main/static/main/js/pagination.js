let entries = document.getElementById("entries");
let parsedUrl = new URL(window.location.href);
let limit = parsedUrl.searchParams.get("limit"),
    sort = parsedUrl.searchParams.get("sort"),
    order = parsedUrl.searchParams.get("order"),
    page = parsedUrl.searchParams.get("page");
if (limit != null) {
    entries.selectedIndex = Array.from(document.querySelectorAll("#entries option"))
        .findIndex(option => option.value === parsedUrl.searchParams.get("limit"));
}
limit = entries.options[entries.selectedIndex].value;
if (parsedUrl.searchParams.get("limit") == null) {
    parsedUrl.searchParams.set("limit", limit);
}
if (sort == null) {
    sort = "date"
    parsedUrl.searchParams.set("sort", sort);
}
if (order == null) {
    order = "asc"
    parsedUrl.searchParams.set("order", order);
}

entries.onchange = function() {
    //rows_tr = document.querySelectorAll("tbody tr");

   limit = entries.options[entries.selectedIndex].value;
    page = 1;
    parsedUrl.searchParams.set("page", page);
    parsedUrl.searchParams.set("limit", limit);

    /*let links = document.querySelectorAll("option a[href]");
    for (let i = 0; i < links.length; i++){
        links[i].setAttribute("href", links[i].getAttribute("href") + `&limit=${entry_num}`);
    }*/
    //window.location.href = parsedUrl.toString();
    window.location.replace(parsedUrl);
};

let links = document.querySelectorAll("li a[href]");
for (let i = 0; i < links.length; i++) {
    links[i].setAttribute("href", links[i].getAttribute("href") + `&limit=${limit}&sort=${sort}&order=${order}`);
}
let tr = document.querySelector("tbody tr");
if (tr == null) {
        let row = document.createElement("tr");
        document.getElementsByTagName('tbody')[0].appendChild(row);
        row.classList.add("filler");
        //row.classList.add("last");
        row.innerHTML = `<td colspan='${document.getElementsByTagName("th").length}'>No data available in table</td>`;
        let show = document.querySelector("#show");
        show.innerText = "Showing 0 to 0 of 0 entries"
} /*else {
    tr_array[tr_array.length - 1].setAttribute("class", "last");
}*/

let th_sort = document.querySelector(`th[data-sort='${parsedUrl.searchParams.get("sort")}']`);
th_sort.setAttribute("class", "sorting-" + parsedUrl.searchParams.get("order"));
let a = document.createElement("a");
a.href = `?page=${page}&limit=${limit}&sort=${sort}&order=${(order === "asc" ? "desc" : "asc")}`;
th_sort.parentNode.insertBefore(a, th_sort);
a.appendChild(th_sort);
let th_array = document.querySelectorAll("th:not([class])");
th_array.forEach(th => {
    let data_sort = th.getAttribute("data-sort");
    let a = document.createElement("a");
    a.href = `?page=${page}&limit=${limit}&sort=${data_sort}&order=asc`
    th.parentNode.insertBefore(a, th);
    a.appendChild(th);
})
/*document.querySelectorAll("th").forEach(th => th.onclick={
    let th_array
})*/