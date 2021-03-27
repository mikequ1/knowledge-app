//this file handles all Google Firebase related actions by our website

const firebaseConfig = {
    apiKey: "AIzaSyDaqo9sjBY6NWoH4sTe8udyc2yB9sgRToA",
    authDomain: "knowledge-9efc6.firebaseapp.com",
    databaseURL: "https://knowledge-9efc6-default-rtdb.firebaseio.com",
    projectId: "knowledge-9efc6",
    storageBucket: "knowledge-9efc6.appspot.com",
    messagingSenderId: "872496344449",
    appId: "1:872496344449:web:1e56e4097dca8e6737cc80",
    measurementId: "G-LM9K85ED21"
};


firebase.initializeApp(firebaseConfig);
firebase.analytics();

var database = firebase.database();

var reqKeyArr = [];
var reqStrArr = [];
var getPostsDone = false;


myStorage = window.localStorage;
var myKey;
var myReq;


//=========================================
// FUNCTIONS
//=========================================

//some notes:
//"taele" input is the HTML element of the text box, NOT the direct string value

//Clear (delete) current request
function clearReq() 
{
    myKey = null;
    myReq = null;
    myStorage.clear();
    document.getElementById("request").value = "";
    document.getElementById("description").innerHTML = "Write a post!";
    document.getElementById("request").disabled = false;
    const myNode = document.getElementById("replies");
    while (myNode.firstChild) {
      myNode.removeChild(myNode.lastChild);
    }
}


//Initialize "need help" interface (on page load)
//A user's request is stored client-side on his/her computer
function initReq() 
{
    myKey = myStorage.keyy;
    myReq = myStorage.msg;
    //TODO: Disply myReq, with HTML
    if(myReq == null)
    {
        document.getElementById("description").innerHTML = "Write a post!";
        document.getElementById("request").value = "";
    }
    if (myKey != null && myReq != null) 
    {
        document.getElementById("request").value = myReq;
        document.getElementById("request").disabled = true;
        document.getElementById("description").innerHTML = "Comment submitted! Now wait for the replies!";
        getResponses(myKey);
    }
    window.setInterval(function(){
        if (myKey != null && myReq != null) 
        {
            document.getElementById("request").value = myReq;
            document.getElementById("request").disabled = true;
            document.getElementById("description").innerHTML = "Comment submitted! Now wait for the replies!";
            getResponses(myKey);
        }
    },1000);
}


//Initialize "help others" interface (on page load)
function initHelp() 
{
    getPosts();
}


//writes a new post
function writeNewPost(taele)
{
    if (myStorage.keyy != null && myStorage.msg != null)
        return;
    var str = taele.value;
    var postData = {req: str,};

    var newPostKey = firebase.database().ref().child('posts').push().key; //makes a new (anonymous) key that stores the post
    var updates = {};
    updates['/posts/' + newPostKey] = postData;

    firebase.database().ref().update(updates);
    
    localStorage.setItem('keyy', newPostKey); //remember my key
    localStorage.setItem('msg', str); //remember my post
    localStorage.setItem("submit_msg", "Post Submitted: " + str);
    console.log("Wrote a new post");

    initReq();
}

//ADMIN: write a new post to firebase (not constrained by user limitations)
function writeNewPostStr(str)
{
    var postData = {req: str,};

    var newPostKey = firebase.database().ref().child('posts').push().key; //makes a new (anonymous) key that stores the post
    var updates = {};
    updates['/posts/' + newPostKey] = postData;

    firebase.database().ref().update(updates);
}

//Generates a post randomly
//TODO: display this post in a card with HTML/JS magic
function getAPost()
{
  var randint = Math.floor(Math.random() * reqKeyArr.length);
  var mykey = reqKeyArr[randint];
  console.log(mykey);
  console.log(reqKeyArr);
  var myStr = reqStrArr[randint];
  //console.log(mykey); 
  console.log(myStr);
  //alert(String(myKey)); //try this function maybe
  //alert(myStr);
  var keey = mykey;
  var value = myStr;
  
  return {keey, value};
}

//Gets a request string given its key (only applies to "i need help" posts)
function getReq(key)
{
  var ref = firebase.database().ref("posts");
  ref.on("value", function(snapshot) {
  var childData = snapshot.val();         
  console.log(childData[key].req);
  });
}

//Removes a request given its key
function removeReq()
{
  var ref = firebase.database().ref('posts/' + myStorage.keyy);
  ref.remove()
  .then(function() {
    clearReq();
    console.log("Remove succeeded.")
  })
  .catch(function(error) {
    console.log("Remove failed: " + error.message)
  });
  return false;
}


//gets all posts
function getPosts() 
{
    getPostsDone = false;
    var numberOfRequests = 0; 
    var leadRef = firebase.database().ref('posts');
    leadRef.on("value", function(snapshot) 
    {
        if(!getPostsDone){
        reqKeyArr = [];
        reqStrArr = [];
        snapshot.forEach(function(childSnapshot) 
        {   
            var childData = childSnapshot.val();
            numberOfRequests++;
            var requestStr = childData.req;                                     // HOLDS "need help" messages
			var requestKey = Object.keys(snapshot.val())[numberOfRequests - 1]; // HOLDS key to the above "need help message"
			            
            //console.log(requestKey);
            reqKeyArr.push(requestKey); //pushes "need help" key to request Key Array
            //console.log(requestStr);
            reqStrArr.push(requestStr); //pushes "need help" string to request String Array (parallel Array with reqKeyArr)
        });
        getPostsDone = true;
    }
    });
}

//allows a user to write a response
function writeResponse(key, taele) 
{
    if (key == null)
        return;
    str = taele.value;
    var newres = firebase.database().ref('posts/' + key).push();
    console.log("Response written");
    newres.set(str);
}

//allows a user to receive the responses to their originally-written post
function getResponses(key) 
{
    parentDiv = document.getElementById("replies");
    
    //remove all child elements before polling for new responses
    while(parentDiv.childElementCount > 0){
        parentDiv.lastChild.remove();
    }
    
    var leadRef = firebase.database().ref('posts/' + key);
    leadRef.on("value", function(snapshot) 
    {
        var ctr = 0;
        snapshot.forEach(function(childSnapshot) 
        {
            var responseStr = childSnapshot.val();        //Retrieves responses
            var responseKey = Object.keys(snapshot.val())[ctr]; //Retrieves the key to that^ response
            if (responseKey == "req") return;
            console.log(responseStr);
            
            var childDiv = document.createElement("div");
            childDiv.style.marginLeft = 20;
            var userImg = document.createElement("img");
            userImg.class = "x";
            userImg.src="https://i.imgur.com/A7whIBi.png";
            userImg.style.cssFloat = "left";
            userImg.height = 70;
            userImg.width = 70;
            childDiv.setAttribute("class", "replies");
            var text = document.createElement("p");
            text.innerHTML = responseStr;
            text.style.textAlign = "center";
            text.style.lineHeight = "3";
            childDiv.appendChild(userImg);
            childDiv.appendChild(text);
            parentDiv.appendChild(childDiv);
            ctr++;
        });
    });
}
