const st = {};

st.flap = document.querySelector('#flap');
st.toggle = document.querySelector('.toggle');

st.choice1 = document.querySelector('#choice1');
st.choice2 = document.querySelector('#choice2');

st.flap.addEventListener('transitionend', () => {

    if (st.choice1.checked) {
        st.toggle.style.transform = 'rotateY(-15deg)';
        setTimeout(() => st.toggle.style.transform = '', 400);
    } else {
        st.toggle.style.transform = 'rotateY(15deg)';
        setTimeout(() => st.toggle.style.transform = '', 400);
    }

})

let Areas = document.querySelectorAll('area');
let Inputs = document.querySelectorAll('input[type="radio"]')
st.clickHandler = (e) => {

    if (e.target.tagName === 'LABEL') {
        setTimeout(() => {
            st.flap.children[0].textContent = e.target.textContent;
            console.log(e.target.control.getAttribute('value'));
            st.flap.children[0].setAttribute("data-value", e.target.value);
        }, 250);
        Areas.forEach(area =>
            Inputs.forEach(input =>
                area.href = area.href.replace(input.value, e.target.control.getAttribute('value'))))
    }
}

document.addEventListener('DOMContentLoaded', () => {
    st.flap.children[0].textContent = st.choice2.nextElementSibling.textContent;
    //st.flap.children[0].setAttribute("data-value", st.choice2.nextElementSibling.value);
});

document.addEventListener('click', (e) => st.clickHandler(e));

