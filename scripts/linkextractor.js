var data;
var topicToday = "Communism";

//load in python-generated JSON file
var xhr = new XMLHttpRequest();
var url = "https://mikequ1.github.io/wiki_info.json";
xhr.open('GET', url, true);

xhr.onload = function() {
    data = JSON.parse(this.response);
    console.log(data);
}
xhr.send();


var entries = new Array(2);
function loadJSON()
{
    var dataArray = data.Topics;
    for (var i = 0; i < dataArray.length; i++)
    {
        if (dataArray[i].Topic == topicToday)
            entries.push(dataArray[i].Site[0]);
        //console.log(entries[i]);
    }
}

function getArticle()
{
    var index = Math.floor(Math.random() * entries.length);
    return entries[index];
}