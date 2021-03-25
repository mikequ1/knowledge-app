var xhr = new XMLHttpRequest();
var url = "https://en.wikipedia.org/w/api.php?action=query&origin=*&format=json&generator=search&gsrnamespace=0&gsrlimit=5&gsrsearch='New_England_Patriots'";
xhr.open('GET', url, true);
xhr.onload = function() {
    var data = JSON.parse(this.response);
    console.log(data);

    // Log the page objects
    console.log(data.query.pages)

    for (var i in data.query.pages) 
    {
        console.log(data.query.pages[i].title);
    }
}
xhr.send();


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