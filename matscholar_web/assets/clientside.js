// For running clientside callbacks in plotly dash
// This is the top level file for all custom js functions.


var rotationTime = 2000;  // the time between rotating example searches in the bar
var countTime = 1500;  // the time needed to count up to all numbers in the app animations


if(!window.dash_clientside) {window.dash_clientside = {};}
window.dash_clientside.clientside = {
    // Animate the about page stats
    // See count.js for more details
    countStatsClientsideFunction: function (pathname, id1, id2, id3, hiddenId1, hiddenId2, hiddenId3) {
        if (pathname == "/about"){
            animatedCount(id1, hiddenId1, countTime)
            animatedCount(id2, hiddenId2, countTime)
            animatedCount(id3, hiddenId3, countTime)
        }
    },

    // Animate the search bar abstracts
    // see count.js for more details
    countSearchClientsideFunction: function (pathname, id, hiddenId) {
        if (pathname == "/search" || pathname =="/" || pathame == null){
            animatedCount(id, hiddenId, countTime)
        }
    },

    // Cycle/rotate through example searches
    // see exampleSearches.js for more details
    cycleExampleSearchesClientsideFunction: function (pathname, id, exampleSearchesStringId) {
        if (pathname == "/search" || pathname =="/" || pathame == null){
            runExampleSearches(id, exampleSearchesStringId, rotationTime)
        }
    },

    // Animate the burger menu on mobile
    // see burger.js for more detials.
    animateBurgerOnClickClientsideFunction: function (activateId, triggerNClicks) {
        animateBurgerOnClick(activateId, triggerNClicks);
        return ""
    }

}