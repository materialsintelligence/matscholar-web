function runExampleSearches(id, exampleSearchesStringId, rotationTime){
    var obj = document.getElementById(id);
    var exampleSearchesString = document.getElementById(exampleSearchesStringId).innerHTML;
    var exampleSearches = exampleSearchesString.split(" | ");

    console.log(exampleSearches)
    console.log(exampleSearches[0])

    // recursive function for iterating through array with delay,
    // hacky, but works
    nRotations = 100
    function log(i){
        console.log(exampleSearches[i]);
        if (i < nRotations){
           setTimeout(function(){
               i++;
               var evaluation = parseInt(exampleSearches.length)
               var internalIndex = i % evaluation;
               var exampleSearch = exampleSearches[internalIndex];
               obj.innerHTML = exampleSearch;
               log(i);

           }, rotationTime);
        }
    }
    log(0);
}
