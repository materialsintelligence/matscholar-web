if(!window.dash_clientside) {window.dash_clientside = {};}
window.dash_clientside.clientside = {
    countStats: function (pathname, id1, id2, id3, hiddenId1, hiddenId2, hiddenId3) {
        if (pathname == "/about"){
                animatedCount(id1, hiddenId1, countTime)
                animatedCount(id2, hiddenId2, countTime)
                animatedCount(id3, hiddenId3, countTime)
        }
    },
    countSearch: function (pathname, id, hiddenId) {
        if (pathname == "/search"){
                animatedCount(id, hiddenId, countTime)
        }
    }
}