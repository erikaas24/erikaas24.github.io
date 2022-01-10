const ToggleButton = document.querySelector("#toggle_button")
const NavbarRight = document.querySelector(".navbar_right")

ToggleButton.addEventListener('click',() => {
    NavbarRight.classList.toggle('active')
})