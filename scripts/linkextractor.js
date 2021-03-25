
var searchArr = ['New_England_Patriots','Universities','Immigration','Coronavirus','Math','Computing'
,'Literature','History','2008_Financial_Crisis'];
var x = []
var y = []
var data;
var dataArr = []


for(var j = 0; j < searchArr.length; j++){
    var xhr = new XMLHttpRequest();
    var url = "https://en.wikipedia.org/w/api.php?action=query&origin=*&format=json&generator=search&gsrnamespace=0&gsrlimit=5&gsrsearch=" +searchArr[j];
    xhr.open('GET', url, true);


    xhr.onload = function() {
        dataArr.push(JSON.parse(this.response));
        //console.log(data);
    
        // Log the page objects
       // console.log(data.query.pages);
    
        //var stringArr = []
    
        //for (var i in data.query.pages) 
        //{
         //   console.log(data.query.pages[i].title);
            //stringArr.push(i);
            
        //}
    
       // for(var j = 0; j < 4; j++){
           // var index = Math.floor(Math.random() * stringArr.length);
           // x.push(data.query.pages[stringArr[index]].title);
        //}
    }
    xhr.send();

}




function myFunc(){
    // Log the page objects
    //console.log(data.query.pages);
    


    var stringArr = []
    var categoryArr = []
    for(var m = 0; m < searchArr.length; m++){
        for (var i in dataArr[m].query.pages) 
        {
            console.log(dataArr[m].query.pages[i].title);
            console.log(dataArr[m].query.pages[i]);
            stringArr.push(i);
            categoryArr.push(m);
        }
    }
    
    x = [];
    y = [];
    for(var j = 0; j < 4; j++){
        var index = Math.floor(Math.random() * stringArr.length);
        
        x.push(dataArr[categoryArr[index]].query.pages[stringArr[index]].title);
        var titleurl = dataArr[categoryArr[index]].query.pages[stringArr[index]].title;
        titleurl = titleurl.replace(" ","_");
        titleurl = "https://en.wikipedia.org/wiki/" + titleurl;
        y.push(titleurl);
    }
}


const container = document.querySelector("#mw-pages");
var x = container.querySelectorAll("a");
var myarray = []

for (var i = 0; i < x.length; i++)
{
    var nametext = x[i].textContent;
    var cleantext = nametext.replace(/\s + /g, ' ').trim();
    var cleanlink = x[i].href;
    console.log(cleanlink);
        myarray.push([cleantext,cleanlink]);
};

function make_table() {
    var table = '<table><thead><th>Name</th><th>Links</th></thead><tbody>';
    for (var i = 0; i < myarray.length; i++) 
    {
        table += '<tr><td>'+ myarray[i][0] + '</td><td>'+myarray[i][1]+'</td></tr>';
    };
    var w = window.open("");
w.document.write(table); 
}


make_table()