const burgerMenu = document.getElementById('burger')
const navigationBlock = document.getElementById('navigation')
const menuNav = document.getElementById('main-nav-menu')

let isMainMenuActive = false

burgerMenu.addEventListener('click', function () {
    burgerMenu.classList.toggle('active');
    navigationBlock.classList.toggle('open');
    if (!isMainMenuActive) {
        menuNav.classList.add('active-menu');
    } else {
        menuNav.classList.remove('active-menu');
    }
    isMainMenuActive = !isMainMenuActive
})


document.addEventListener('DOMContentLoaded', function () {
    const menuNavMobile = document.getElementById('menu-nav-mobile');

    document.addEventListener('click', function (event) {
        if (isMainMenuActive) {
            let isClickInsideMenu = menuNavMobile.contains(event.target);
            if (!isClickInsideMenu && event.target !== document.querySelector('.burger-menu')) {
                menuNav.classList.remove('active-menu');
                burgerMenu.classList.toggle('active');
                navigationBlock.classList.toggle('open');
                isMainMenuActive = false;
            }
        }
    });
});
