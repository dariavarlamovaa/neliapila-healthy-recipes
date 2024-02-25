const menuNav = document.getElementsByClassName('main-nav-menu')

document.querySelector('.burger-menu').addEventListener('click', function () {
    this.classList.toggle('active');
    document.querySelector('.navigation').classList.toggle('open');
    document.querySelector('.main-nav-menu').classList.toggle('active-menu');
})