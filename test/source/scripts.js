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
    mobileMenu = document.getElementById("mobile-menu");
    mobileMenuBtnImg = document.getElementById("header-menu-btn-img");
    mobileMenu.style.display = "none";

    domLoaded = true;
}

addEventListener("resize", (e) => {
    // Resize won't close the menu unless it passes the threshold
    if (window.outerWidth > 700) {
        mobileMenu.style.display = "none";
    }
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
