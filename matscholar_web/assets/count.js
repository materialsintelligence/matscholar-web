// The file for animating counts.
// Not called directly, only by Clientside callback in clientside.js


function animatedCount(id, hiddenId, duration) {
    // Count up to a number with animation
    // id (String): Id of the element which to animate
    // hiddenId (String): Id of the element from which to draw the max
    //      value for counting. Should be hidden, probably
    // duration (Integer): The duration of the animation; longer means
    //      slower animation
    var radix = 10;
    var srcValue = document.getElementById(hiddenId).innerHTML;
    var countTo = srcValue.replace(/,/g, "")
    var countTo = parseInt(countTo, radix)

    var obj = document.getElementById(id);

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
