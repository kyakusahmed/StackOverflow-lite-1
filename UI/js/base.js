/* Resgister new user */
// let signUp = (e)
var fetch = require("node-fetch")


fetch('http://localhost:5000/api/v1/questions/1')
.then(res => res.json())
// .then(json => console.log(json));
.then(json => console.log(JSON.stringify(json)))
