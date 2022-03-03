// https://docs.github.com/en/rest/guides/traversing-with-pagination

var req = require('request');
var fs = require('fs')

targetUser = "mahee96";

currPage = 1

var targetUrl = "https://api.github.com/users/" + targetUser + "/repos?per_page=3&page=" + currPage;

const options = {
    url: targetUrl,
    headers : { 'User-Agent': 'bla-bla'},
};

last_page = currPage

// clear it out
fs.writeFileSync('public_repos.txt', '');

var callback = async (err, resp, body)=>{
    if(err){
        console.log(err);
        return;
    }
    if (last_page == 1){
        var link = resp.headers.link;                   // next and last page link is here
        //var next = link.split(',')[0].split(';')[0].trim()
        //targetUrl = next
        var last = link.split(',')[1].split(';')[0].trim()
        last = last.substr(1, (last.length-1)-1)   // strip off < and >
        params = last.split('?')[1].split('&')          //filter out query params
        per_page = params[0].split('=')[1]
        last_page = params[1].split('=')[1]    
    }
    var json   = JSON.parse(body);
    var pretty = JSON.stringify(json, null, "  ");
    // fs.writeFileSync('public_repos.json', pretty);
    json.forEach(element => {
        repo_url = element['html_url']
        fs.appendFileSync('public_repos.txt', "\"" + repo_url + "\"\n")
    });
}

for (let i = currPage; i <= last_page; i++) {
    req(options, callback)
    currPage ++;
}
