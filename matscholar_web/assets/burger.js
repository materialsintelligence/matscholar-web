// Javascript for running the hamburger menu
// Not called directly, only by Clientside callback in clientside.js

function animateBurgerOnClick(activateId, triggerNClicks) {
    // See https://stackoverflow.com/questions/54848094/bulma-navbar-hamburger-menu-doesnt-expand
    // Get all "navbar-burger" elements
    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
    // Check if there are any navbar burgers
    if ($navbarBurgers.length > 0) {
        // Add a click event on each of them
        $navbarBurgers.forEach( el => {
            // Get the target from the "data-target" attribute
            target = el.dataset.target;
            console.log(target)
            $target = document.getElementById(target);
            console.log($target)

            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            el.classList.toggle('is-active');
            $target.classList.toggle('is-active');
        });
    }


}