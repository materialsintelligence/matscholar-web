// The file for rotating example searches.
// Not called directly, only by Clientside callback in clientside.js


function runExampleSearches(id, exampleSearchesStringId, rotationTime){
    // Put an example search into an input textbox as placeholder
    //
    // id (String): The id of the input for which the placeholder needs to be updated
    // exampleSearchesStringId (String): The id of the hidden div which contains the
    //      example searches as a string separated by " | "
    // rotationTime (Integer): The time between rotating placeholder text

    var obj = document.getElementById(id);
    var exampleSearchesString = document.getElementById(exampleSearchesStringId).innerHTML;
    var exampleSearchesUnfiltered = exampleSearchesString.split(" | ");
    var exampleSearches = exampleSearchesUnfiltered.filter(
        function (e){
            return e != ""
        }
    )

    // recursive function for iterating through array with delay,
    // hacky, but works
    nRotations = 100
    function log(i){
        if (i < nRotations){
           setTimeout(function(){
               i++;
               var evaluation = parseInt(exampleSearches.length)
               var internalIndex = i % evaluation;
               var exampleSearch = exampleSearches[internalIndex];
               obj.placeholder = exampleSearch;
               log(i);

           }, rotationTime);
        }
    }
    log(0);
}
