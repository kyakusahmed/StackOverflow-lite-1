
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

function fetchAnswers(questionId){
    console.log(document.title == "StackOverflow-lite-question");
    if (document.title == "StackOverflow-lite-question"){
        fetch(`http://127.0.0.1:5000/api/v1/questions/${questionId}/answers`, {
            mode: "cors",
        })
        .then(res => res.json())
        .then(json =>{
            console.log(json);
            if ("message" in json){
                console.log(json.message);
                let Qtns2 = document.getElementById('Qtns2');
                    Qtn = createNode('p');
    
                Qtn.innerHTML = `${json.message}`
                append(Qtns2, Qtn)
            }
            if ("answers" in json){
                for (let answer of  json.answers){
                    let li = createNode('li'),
                        span = createNode('span'),
                        span2 = createNode('span'),
                        strong = createNode('strong');
                        
                        Qtns2 = document.getElementById('Qtns2');
                        Qtn = createNode('p');
                    

                    if (answer.prefered == true){
                        strong.classList.add("prefered");
                        span.innerHTML = ` <strong>Author:</strong> ${answer.author}`;
                        span2.innerHTML = `${answer.body} <br>`;
                        strong.innerHTML = "Prefered answer";
                        append(li, span2);
                        append(li, span);
                        append(li, strong);
                        append(Qtn, li);
                        // append(a, Qtn);
                        append(Qtns, Qtn);
                    }
                    if (answer.prefered == false){
                        span.innerHTML = ` <strong>Author:</strong> ${answer.author}`;
                        span2.innerHTML = `${answer.body} <br>`;
                        append(li, span2);
                        append(li, span);
                        append(Qtn, li);
                        // append(a, Qtn);
                        append(Qtns, Qtn);
                    }
                }
            }
        });
    }
    
    }
    

function onDocumentReady(){
    console.log(document.title=="StackOverflow-lite-index");
    if (document.title=="StackOverflow-lite-index" || document.title=="StackOverflow-lite-question"){
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
                    a.setAttribute('href', 'question.html')
                    
                    a.onclick = fetchAnswers(question.questionId);
                    
    
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
                    append(a, Qtn);
                    append(Qtns, a);
                }
            }
        
        })

        .catch(error => console.error(error));
    }
}
    
