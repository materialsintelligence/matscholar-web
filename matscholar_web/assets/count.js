
function animatedCount(id, duration) {
    var radix = 10
    var obj = document.getElementById(id);
    var countTo = obj.innerHTML.replace(/,/g, "")
    var countTo = parseInt(countTo, radix)
//    var countTo = 10000

    // assumes integer values for start and end
    var start = 0 * countTo;
    var end = countTo;

    var range = end - start;
    // no timer shorter than 50ms (not really visible any way)
    var minTimer = 50;
    // calc step time to show all interediate values
    var stepTime = Math.abs(Math.floor(duration / range));

    // never go below minTimer
    stepTime = Math.max(stepTime, minTimer);

    // get current time and calculate desired end time
    var startTime = new Date().getTime();
    var endTime = startTime + duration;
    var timer;

    function run() {
        var now = new Date().getTime();
        var remaining = Math.max((endTime - now) / duration, 0);
        var value = Math.round(end - (remaining * range));
        var formattedValue = value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        obj.innerHTML = formattedValue
        if (value == end) {
            clearInterval(timer);
        }
    }

    timer = setInterval(run, stepTime);
    run();
}


var waitTime = 1000;
var countTime = 3000;

//function ifLoop(id, countTime){
//    var obj = document.getElementById(id)
//    for (i = 0; i < 1000; i++)
//        if ($(obj).is(":visible")){
//            animatedCount(id, countTime);
//            break;
//        }
//        else {
//            setTimeout(function (){}, 100)
//        }
//}
//
//function runOnLoad(id){
//    window.onload = function() {
//    if (window.jQuery) {
//        // jQuery is loaded
//        var container = document.getElementById("stats-container")
//        var obj = document.getElementById(id)
//
//        $(obj).ready(function(id, countTime){
//        animatedCount(id, countTime);
//        }
//        );
//
//    } else {
//        // jQuery is not loaded
//        alert("Doesn't Work");
//    }
//
//}
//}
//
//
//runOnLoad("count-materials")


