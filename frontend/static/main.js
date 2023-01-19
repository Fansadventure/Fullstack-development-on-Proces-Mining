/**
 * switch the dark and light theme 
 */

let localData = localStorage.getItem("theme");
const themeToggle = document.getElementById("theme-toggle");
(localData == "dark") ? enableDarkMode():enableLightMode();
themeToggle.addEventListener("click", () => {
    localData = localStorage.getItem("theme");
    (localData == "dark") ? enableLightMode():enableDarkMode();
  });
function enableDarkMode() {
  document.body.classList.remove("light-theme");
  document.body.classList.add("dark-theme");
  themeToggle.setAttribute("aria-label", "Light Mode");
  localStorage.setItem("theme", "dark");
}
function enableLightMode() {
  document.body.classList.remove("dark-theme");
  document.body.classList.add("light-theme");
  themeToggle.setAttribute("aria-label", "Dark Mode");
  localStorage.setItem("theme", "light");
}

/**
 * indicate the active page the user is located
 */

document.querySelectorAll('nav a').forEach
(link => {
    if(link.href === window.location.href){
        link.setAttribute('aria-current','active-page')
    }
})

/**
 * Toggle button
 */
const toggleButton = document.getElementsByClassName("toggle-button")[0]
const navbar = document.getElementsByClassName("nav")[0]
toggleButton.addEventListener('click', ()=> {
  navbar.classList.toggle('active')
})

/**
 * Animation on scroll
 */
function aos_init() {
  AOS.init({
    duration: 1000,
    easing: "ease-in-out",
    once: true,
    mirror: false
  });
}
window.addEventListener('load', () => {
  aos_init();
});

/**
 * Hide the back-to-top button
 */
const toTop = document.querySelector(".back-to-top");
window.addEventListener("scroll", () => {
  if (window.pageYOffset > 110) {
    toTop.classList.add("active");
  } else {
    toTop.classList.remove("active");
  }
})