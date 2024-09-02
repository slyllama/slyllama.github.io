/*
 * scripts.js
 * Various scripts for Slyllama
 */

var domLoaded = false;
var headerLogo;
var imgViewer;
var imgViewerImg;
var mobileMenu;
var mobileMenuBtn;
var mobileMenuBtnImg;

function loadDOM() {
    // Load and configure DOM elements
    imgViewer = document.getElementById("img-view-container");
    imgViewerImg = document.getElementById("img-view-img");
    mobileMenu = document.getElementById("mobile-menu");
    mobileMenuBtn = document.getElementById("mobile-menu-btn");
    mobileMenuBtnImg = document.getElementById("header-menu-btn-img");

    imgViewer.style.display = "none"; // so its known to the script
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
// We also add/remove `tabindex`es so accessibility order works properly
function toggleMobileMenu() {
    if (domLoaded == false) { return; }
    var menuElements = mobileMenu.getElementsByTagName("a");
    var mCount = 0;

    if (mobileMenu.style.display == "none") {
        mobileMenu.style.display = "block";
        for (var m = 0; m < menuElements.length; m++) {
            menuElements[m].removeAttribute('tabindex');
            ++mCount;
        }
    } else {
        mobileMenu.style.display = "none";
        for (var m = 0; m < menuElements.length; m++) {
            menuElements[m].tabIndex = -1;
            ++mCount;
        }
    }
}

/* Image viewer functions */

function viewImg(url, alt = "Image.") {
    imgViewerImg.src = url;
    imgViewerImg.alt = alt;
    document.body.style.overflowY = "hidden";
    imgViewer.style.display = "block";
}

function closeImg() {
    document.body.style.overflowY = "initial";
    imgViewer.style.display = "none";
}
