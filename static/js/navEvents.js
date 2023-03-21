
function toggleBurgerButton() {
    var burgerButton = document.getElementById('burger-btn');
    var navDrop = document.getElementById('nav-dropdown');
    burgerButton.classList.toggle('is-active');
    navDrop.classList.toggle('show');
}
