function runExampleSearches(id, exampleSearchesStringId, rotationTime){
    var obj = document.getElementById(id);
    var exampleSearchesString = document.getElementById(exampleSearchesStringId).innerHTML;
    var exampleSearches = exampleSearchesString.split();
    for (i = 0; i < 1000; i++){
        var internalIndex = i % exampleSearches
        setTimeout(function(){
            console.log
            obj.innerHTML = exampleSearches[internalIndex]
        })
    }
}