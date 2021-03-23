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

var firebase = firebase.database();

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


//writes a new post
function writeNewPost(taele)
{
    var str = taele.value;
    var postData = {req: str,};

    var newPostKey = firebase.database().ref().child('posts').push().key; //makes a new (anonymous) key that stores the post
    var updates = {};
    updates['/posts/' + newPostKey] = postData;

    firebase.database().ref().update(updates);
    
    localStorage.setItem('keyy', newPostKey); //remember my key
    localStorage.setItem('msg', str); //remember my post

    initReq();
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
    str = taele.value;
    var newres = firebase.database().ref('posts/' + key).push();
    newres.set(str);
}

//allows a user to receive the responses to their originally-written post
function getResponses(key) 
{
    parentDiv = document.getElementById("replies");
    while(parentDiv.childElementCount > 1){
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
            //TODO: display each response using HTML on the page
            var childDiv = document.createElement("div");
            childDiv.setAttribute("class", "replies");
            var text = document.createElement("p");
            text.innerHTML = responseStr;
            childDiv.appendChild(text);
            parentDiv.appendChild(childDiv);
            ctr++;
        });
    });
}