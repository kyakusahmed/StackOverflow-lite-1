
// require("es6-promise").polyfill();
// require("isomorphic-fetch");
// var fetch = require("node-fetch")
 
 

function handleErrors(response) {
    if (!response.ok) throw Error(response.status);
    return response;
}

function createNode(element){
    return document.createElement(element);
}

function append(parent, element){
    return parent.appendChild(element)
}

// fetch("http://127.0.0.1:5000/api/v1/questions")
// .then(res=> res.json())
// // .then(res => res.json())
// .then(json => {
//     console.log(json)
// })
// .catch(error => console.error(error));


function onDocumentReady(){
    let url = 'http://127.0.0.1:5000/api/v1/questions'
    fetch(url, {
        mode: "cors",
    })
    .then(res => res.json())
    // .then(json => console.log(json));
    .then(json => {
        console.log(  json.questions[0]);
        let Qtns = document.getElementById('Qtns');
            Qtn = createNode('p');
            console.log(Qtns, Qtn)

        // if (Array.from(json).length !== 0) {
            
        //     Qtn.innerHTML = Array.from(json).toString()
        // }
        if (Array.from(json).length == 0 && "message" in json){
            console.log(json.message);
            Qtn.innerHTML = Array.from(json).toString()
        }
        if (Array.from(json).length == 0 && "questions" in json){
//             console.log(json.questions);
            console.log(Array.from(json.questions));
            let ids = [];
       
            for (let question of json.questions){
                ids.push(question.questionId);
                let a = createNode('a');

                console.log(question);
                console.log(ids)
                let li = createNode('li'),
                    span = createNode('span'),
                    span2 = createNode('span'),
                    span3 = createNode('span');
       
                span.innerHTML = ` <strong>Author:</strong> ${question.author}`;
                span2.innerHTML = `${question.body} <br>`;
                span3.innerHTML = ` <strong>Topic:</strong> ${question.topic} <br>`;
//                 Qtn.innerHTML = li
                append(li, span3);
                append(li, span2);
                append(li, span);
                append(Qtn, li);
                append(Qtns, Qtn);

        

            }
        }
    })
    .catch(error => console.error(error));
}





// let data = {
//     "body": "blah blah blah kwemda"
// }

// if(Array.from(data)) console.log(Array.from(data).length==0);