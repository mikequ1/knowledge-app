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

function pickCardBackground(i){
    var bgArr = [];
    bgArr.push("url(https://image.freepik.com/free-photo/abstract-pink-tone-lights-background-blurred-background_3248-2991.jpg)");
    bgArr.push("url(https://countryclubhills.org/wp-content/uploads/2018/09/Background-Images-2.jpg)")
    bgArr.push("url(https://thewallpaper.co/wp-content/uploads/2020/07/light-green-abstract-wallpaper-hd-background-wallpapers-free-amazing-tablet-smart-phone-4k-high-definition-1920x1080-1.jpg)");
    bgArr.push("url(https://i.ytimg.com/vi/X8FVsLUvWTY/maxresdefault.jpg)");
    bgArr.push("url(https://eskipaper.com/images/light-blue-backgrounds-7.jpg)");
    bgArr.push("url(https://i.pinimg.com/originals/34/04/8d/34048d8aa063b17d2ac45510a4fc6466.jpg)");
    bgArr.push("url(https://www.wallpaperbetter.com/wallpaper/797/61/130/light-abstract-smoke-1080P-wallpaper.jpg)");
    bgArr.push("url(https://www.wallpapertip.com/wmimgs/149-1491561_sky-blue-hd-background-image-for-banner-light.jpg)");
    bgArr.push("url(https://i.pinimg.com/originals/ef/9d/1a/ef9d1a5386d76e1a202034b3c1e92117.png)");

    var yep = "url(https://imgur.com/a/uK3YjwC)"

    var index = Math.floor(Math.random() * bgArr.length);
    document.getElementById("card" + (i + 1)).style.backgroundImage = bgArr[index];
}