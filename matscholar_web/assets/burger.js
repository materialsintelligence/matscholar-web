// Javascript for running the hamburger menu

function animateBurgerOnClick(activateId, triggerNClicks) {

    console.log("inside animateBurgerOnClick");

// See https://stackoverflow.com/questions/54848094/bulma-navbar-hamburger-menu-doesnt-expand
    // Get all "navbar-burger" elements
      const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);


      console.log($navbarBurgers)

      // Check if there are any navbar burgers
      if ($navbarBurgers.length > 0) {
        console.log("the length is more than zero")
        // Add a click event on each of them
        $navbarBurgers.forEach( el => {
//          el.addEventListener('click', () => {
//            console.log("inside event listener")
            console.log("clicking")

            // Get the target from the "data-target" attribute
            target = el.dataset.target;
            console.log(target)
            $target = document.getElementById(target);
            console.log($target)

            // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
            el.classList.toggle('is-active');
            $target.classList.toggle('is-active');

//          });
        });
      }

//    target = document.getElementById(activateId)
//    if (target != null) {
//        if (triggerNClicks > 0){
//            target.classList.toggle('is-active')
//        }
//
//    }

//    navbarBurger = document.getElementById(triggerId)
//
//    if (navbarBurger != null) {
//        console.log(navbarBurger)
//        navbarBurger.addEventListener('click', () => {
//            target = document.getElementById(activateId)
//            console.log("Im getting clickeD!!!")
//            target.classList.toggle('is-active')
//        })
//    }

}