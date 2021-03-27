//Open and close the sidebar
function openNav() {
    document.getElementById("mySidenav").style.width = "250px"; // width of the menu bar is 250 px
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
}

//Element disappearing animation
function removeCard(elem) {
    //TODO:
}

function populateArticles(){
    loadJSON();
    for(var i = 0; i < 4; i++){
        var thisArticle = getArticle();
        var thisTitle = thisArticle.Title;
        var thisSummary = thisArticle.Summary;
        if (thisSummary.length > 250){
            thisSummary = thisSummary.substr(0,250);
            thisSummary += "...";
        }
        var thisLink = thisArticle.Url;
        var thisImg = thisArticle.Pictures;
        
        document.getElementById("header" + (i + 1)).innerHTML = thisTitle;
        document.getElementById("img" + (i+1)).src = thisImg;
        document.getElementById("summary" + (i+1)).innerHTML = thisSummary;
        document.getElementById("link"+(i+1)).href = thisLink;
    }
}