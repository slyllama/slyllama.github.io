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
    mobileMenuBtn = document.getElementById("mobile-menu-btn");
    mobileMenuBtnImg = document.getElementById("header-menu-btn-img");
    mobileMenu.style.display = "none";

    domLoaded = true;

    mobileMenuBtn.addEventListener("keydown", (e) => {
        const { key } = e
        if (key === 'Enter') {
          e.preventDefault();
          toggleMobileMenu();
        }
    });
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
    var menuElements = mobileMenu.getElementsByTagName("a");

    if (mobileMenu.style.display == "none") {
        mobileMenu.style.display = "block";
        for (var m = 0; m < menuElements.length; m++) {
            menuElements[m].removeAttribute('tabindex');
        }
    } else {
        mobileMenu.style.display = "none";
        for (var m = 0; m < menuElements.length; m++) {
            menuElements[m].tabIndex = -1;
        }
    }
}
