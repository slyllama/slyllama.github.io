/*
 * scripts.js
 * Various scripts for Slyllama
 */

var domLoaded = false;
var headerLogo;
var mobileMenu;
var mobileMenuBtn;
var mobileMenuBtnImg;

function loadDOM() {
    // Load and configure DOM elements
    headerLogo = document.getElementById("header-logo");
    mobileMenu = document.getElementById("mobile-menu");
    mobileMenuBtn = document.getElementById("header-menu-btn");
    mobileMenuBtnImg = document.getElementById("header-menu-btn-img");
    mobileMenu.style.display = "none";

    // Change the colour of the title when hovered
    headerLogo.addEventListener("mouseover", (e) => {
        headerLogo.src = "https://slyllama.net/test/assets/logo-hover.svg";
    });
    headerLogo.addEventListener("mouseout", (e) => {
        headerLogo.src = "https://slyllama.net/test/assets/logo.svg";
    });

    // Change the colour of the mobile menu when hovered
    mobileMenuBtn.addEventListener("mouseover", (e) => {
        mobileMenuBtnImg.src = "https://slyllama.net/test/assets/mobile-menu-btn-hover.svg";  
    });
    mobileMenuBtn.addEventListener("mouseout", (e) => {
        mobileMenuBtnImg.src = "https://slyllama.net/test/assets/mobile-menu-btn.svg";
    });

    domLoaded = true;
}

addEventListener("resize", (e) => {
    mobileMenu.style.display = "none";
});

// Use the hamburger to show and hide the mobile menu
function toggleMobileMenu() {
    if (domLoaded == false) { return; }
    if (mobileMenu.style.display == "none") {
        mobileMenu.style.display = "block";
    } else {
        mobileMenu.style.display = "none";
    }
}