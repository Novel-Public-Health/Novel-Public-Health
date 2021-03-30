window.addEventListener('load', (event) => {
    mobileMenuList.style.transition = "transform 0.5s cubic-bezier(0.77, 0.2, 0.05, 1.0)";
});

var mobileMenuList = document.getElementById('mobileMenuList');
var mobileBtn = document.getElementById('mobileBtn');
// Click on any area on mobile to close the side menu.
document.body.addEventListener("click", () => {
    if (openMenu) {
        mobileBtn.checked = false;
    }
}, false);
// Avoid closing the mobile side menu when clicking the list area.
mobileMenuList.addEventListener("click", (ev) => {
    if (openMenu) {
        ev.stopPropagation();
    }
}, false);

var mobileMenuTransition = false;
var openMenu = false;
mobileMenuList.addEventListener('transitionstart', () => {
    mobileMenuTransition = true;
    openMenu = (mobileBtn.checked) ? true : false;
});
mobileMenuList.addEventListener('transitionend', () => {
    mobileMenuTransition = false;
});