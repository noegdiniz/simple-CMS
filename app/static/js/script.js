// script.js
const mobileMenu = document.getElementById('mobile-menu');
const navbarMenu = document.querySelector('.navbar-menu');

mobileMenu.addEventListener('click', () => {
  mobileMenu.classList.toggle('active');
  navbarMenu.classList.toggle('active');
});