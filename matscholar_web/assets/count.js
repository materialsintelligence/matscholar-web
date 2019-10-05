function animatedCount(id, duration) {
    var radix = 10
    var obj = document.getElementById(id);
    var countTo = parseInt(obj.innerHTML, radix)
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

var waitTime = 1000
var countTime = 3000
// Start counting after asynchronously waiting to avoid plotly javascript being
// put BEFORE the page content. This script must be run after the page content
// has loaded in order to work.
window.setTimeout(animatedCount, waitTime, "count-materials", countTime);
window.setTimeout(animatedCount, waitTime, "count-abstracts", countTime);
window.setTimeout(animatedCount, waitTime, "count-entities", countTime);