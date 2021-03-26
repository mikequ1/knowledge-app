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
    keys.length = 0;
    myFunc();
    for(var i = 0; i < 4; i++){
      var userReq = document.getElementById("header" + (i + 1));
      console.log(x);
      var req = x;
    var newTitle = "Article title: " + req[i];
    userReq.innerHTML = newTitle;

    var linkReq = document.getElementById("link"+(i+1));
    linkReq.href = y[i];
    }
}