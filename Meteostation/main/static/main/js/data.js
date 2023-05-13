const st = {};

st.flap = document.querySelector('#flap');
st.toggle = document.querySelector('.toggle');

const menu = document.querySelector('.menu-slide-in');
st.choice1 = document.querySelector('#choice1');
st.choice2 = document.querySelector('#choice2');
const Interpolations = JSON.parse(
  document.currentScript.previousElementSibling.textContent
);
st.flap.addEventListener('transitionend', () => {

    if (st.choice1.checked) {
        menu.classList.remove('active');
        st.toggle.style.transform = 'rotateY(-15deg)';
        setTimeout(() => st.toggle.style.transform = '', 400);
    } else {
        menu.classList.add('active');
        st.toggle.style.transform = 'rotateY(15deg)';
        setTimeout(() => st.toggle.style.transform = '', 400);
    }
    let choice = document.querySelector('input[name="choice"]:checked');
    Areas.forEach(area => {
        Interpolations.forEach(interpolation =>{
            if (choice.value === 'raw'){
                area.href = area.href.replace(interpolation, 'raw');
            } else {
                let interpolation_name = document.querySelector('input[name="interpolation"]:checked').value;
                area.href = area.href.replace('raw', interpolation_name);
                area.href = area.href.replace(interpolation, interpolation_name);
            }
        })
    });
})

let Areas = document.querySelectorAll('area');
let Inputs = document.querySelectorAll('input[type="radio"]')
st.clickHandler = (e) => {
    if (e.target.tagName === 'LABEL') {
        setTimeout(() => {
            st.flap.children[0].textContent = e.target.textContent;
            // console.log(e.target.control.getAttribute('value'));
            // st.flap.children[0].setAttribute("data-value", e.target.value);
        }, 250);

    }
}

document.addEventListener('DOMContentLoaded', () => {
    st.flap.children[0].textContent = st.choice2.nextElementSibling.textContent;
    //st.flap.children[0].setAttribute("data-value", st.choice2.nextElementSibling.value);
});

document.addEventListener('click', (e) => st.clickHandler(e));
menu.classList.add('active');
let Input_interpol = document.querySelectorAll('.menu-slide-in.active label input[type="radio"]');
Input_interpol[0].checked = 'checked'

Input_interpol.forEach(Input => Input.onchange = function(){
    let Value = document.querySelector('.menu-slide-in.active label input[type="radio"]:checked').value;
    Areas.forEach(Area =>
        Interpolations.forEach(Interpolation =>
        Area.href = Area.href.replace(Interpolation, Value)));
});