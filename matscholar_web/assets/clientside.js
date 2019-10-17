var rotationTime = 3000;
var countTime = 3000;


if(!window.dash_clientside) {window.dash_clientside = {};}
window.dash_clientside.clientside = {
    // Animate the about page stats
    countStats: function (pathname, id1, id2, id3, hiddenId1, hiddenId2, hiddenId3) {
        if (pathname == "/about"){
            animatedCount(id1, hiddenId1, countTime)
            animatedCount(id2, hiddenId2, countTime)
            animatedCount(id3, hiddenId3, countTime)
        }
    },

    // Animate the search bar abstracts
    countSearch: function (pathname, id, hiddenId) {
        if (pathname == "/search" || pathname =="/" || pathame == null){
            animatedCount(id, hiddenId, countTime)
        }
    },

    // Cycle through example searches
    cycleExampleSearches: function (pathname, id, exampleSearchesStringId) {
        if (pathname == "/search" || pathname =="/" || pathame == null){
            runExampleSearches(id, exampleSearchesStringId, rotationTime)
        }
    },

    // Animate the burger menu on mobile
    animateBurgerOnClickCSCallback: function (activateId, triggerId) {
        animateBurgerOnClick(activateId, triggerId);
    }

}