function animateValue(id, countTo, duration) {
    var radix = 10
    var obj = document.getElementById(id);
    var countTo = parseInt(obj, radix)

    // assumes integer values for start and end
    var start = 0.75 * countTo;
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
        obj.innerHTML = value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
        if (value == end) {
            clearInterval(timer);
        }
    }

    timer = setInterval(run, stepTime);
    run();
}

window.setTimeout(animateValue, 1000, "jscount-materials", 298616, 5000);
window.setTimeout(animateValue, 1000, "jscount-entities", 298616, 5000);
window.setTimeout(animateValue, 1000, "jscount-abstracts", 298616, 5000);