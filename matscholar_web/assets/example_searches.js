function runExampleSearches(id, exampleSearchesStringId, rotationTime){
    var obj = document.getElementById(id);
    var exampleSearchesString = document.getElementById(exampleSearchesStringId).innerHTML;
    var exampleSearches = exampleSearchesString.split(" | ");

    console.log(exampleSearches)
    console.log(exampleSearches[0])

    for (let i = 0; i < 1000; i++){
        (function (i) {
            var internalIndex = i % exampleSearches.length;
            console.log(internalIndex)
            setTimeout(
                function(){
                    var exampleSearch = exampleSearches[internalIndex];
                    console.log(exampleSearch);
                    obj.innerHTML = exampleSearch;
                },
                rotationTime
            );
        })(i);
    };
};