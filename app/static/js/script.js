var mobileMenu = document.getElementById('mobile-menu');
var navbarMenu = document.querySelector('.navbar-menu');

mobileMenu.addEventListener('click', () => {
  mobileMenu.classList.toggle('active');
  navbarMenu.classList.toggle('active');
});
