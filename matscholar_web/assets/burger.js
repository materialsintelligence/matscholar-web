// Javascript for running the hamburger menu

function animateBurgerOnClick(activateId, triggerId) {

    console.log("inside animateBurgerOnClick");

    // Get all "navbar-burger" elements
//    const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);
//
//    console.log($navbarBurgers)
//
//    // Check if there are any navbar burgers
//    if ($navbarBurgers.length > 0) {
//
//    // Add a click event on each of them
//    $navbarBurgers.forEach( el => {
//        el.addEventListener('click', () => {
//            console.log("clicking!!")
//
//            // Get the target from the "data-target" attribute
////            const target = el.dataset.target;
//            const $target = document.getElementById(id);
//
//            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
//            el.classList.toggle('is-active');
////            $target.classList.toggle('is-active');
//
//            });
//        });


    navbarBurger = document.getElementById(triggerId)
    navbarBurger.addEventListener('click', () => {
        target = document.getElementById(activateId)
        console.log("Im getting clickeD!!!")
        target.classList.toggle('is-active')


    })
}