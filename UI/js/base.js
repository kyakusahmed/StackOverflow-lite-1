
// require("es6-promise").polyfill();
// require("isomorphic-fetch");
// var fetch = require("node-fetch")

let alertMessage = (message) => {
    let alert = document.getElementById('alert');
    alert.style.display = 'block';
    alert.style.padding = '10px';
    alert.innerHTML = message;
    setTimeout(() => alert.style.display = 'none', 6000);
}
 

function handleErrors(response) {
    if (!response.ok) throw Error(response.status);
    return response;
}

function createNode(element){
    return document.createElement(element);
}

function append(parent, element){
    return parent.appendChild(element);
}


function onFetchAnswers(){
    console.log(document.title == "StackOverflow-lite-question");
    if (document.title == "StackOverflow-lite-question"){
        questionId = window.localStorage.getItem('questionId');
        let submit2 = document.getElementById('submit2');

        submit2.addEventListener('click', postAns => {
            postAnswer(questionId);
            // window.localStorage.setItem('questionId', questionId);
            // window.location.reload();
        })
        console.log(questionId);

        if(!document.title == "StackOverflow-lite-question" || !document.title == "StackOverflow-lite-index"){
            window.localStorage.removeItem('questionId');
        }
        
        fetch(`http://127.0.0.1:5000/api/v1/questions/${questionId}/answers`, {
            mode: "cors",
        })
        .then(res => res.json())
        .then(json =>{
            console.log(json);
            let Question = document.getElementById('Question');
                h3 = createNode('h3');
                li = createNode('li');
                span1 = createNode('span');
                span2 = createNode('span')
                
            fetch(`http://localhost:5000/api/v1/questions/${questionId}`)
            .then(res => res.json())
            .then(json=>{
                console.log(json);
                h3.innerHTML = `${json.body}`;
                span1.innerHTML = `<strong>Author: </strong>${json.author}`;
                span2.innerHTML = `<strong>Topic: </strong>${json.topic}`;
                // li.style['max-width'] = `${Math.max(json.body.length, 400)}px`;
                append(li, span2);
                append(li, h3);
                append(li, span1);
                append(Question, li);
            })
            
            if ("message" in json){
                console.log(json.message);
                let Qtns2 = document.getElementById('Qtns2');
                    Qtn = createNode('p');
    
                Qtn.innerHTML = `${json.message}`
                append(Qtns2, Qtn)

            }
            if ("answers" in json){
                console.log(json);
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
                        append(Qtns2, Qtn);
                    }
                    if (answer.prefered == false){
                        span.innerHTML = ` <strong>Author:</strong> ${answer.author}`;
                        span2.innerHTML = `${answer.body} <br>`;
                        append(li, span2);
                        append(li, span);
                        append(Qtn, li);
                        // append(a, Qtn);
                        append(Qtns2, Qtn);
                        
                    }
                }
            }
        });
    }
    
    }

function onDocumentReady(){
    console.log(document.title=="StackOverflow-lite-index");
    if (document.title=="StackOverflow-lite-index"){
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
                for (let question of json.questions){
                    console.log(question);
                    
                    let li = createNode('li'),
                        space = createNode('h3');
                        span = createNode('span'),
                        span2 = createNode('span'),
                        span3 = createNode('span');
                        a = createNode('a');
                        Qtn = createNode('p');
                        Qtns = document.getElementById('Qtns');
                    

                    console.log(1, document.title=="StackOverflow-lite-index");
                    if (document.title=="StackOverflow-lite-index"){
                        a.setAttribute('href', 'question.html');
                        a.setAttribute('class', 'question_link');
                        console.log("href registerd");
                        console.log(document.title);
                        a.onclick = link =>{
                            window.localStorage.setItem('questionId', question.questionId);
                            window.location.replace('./question.html')
                        }
                        let submit = document.getElementById('submit');
                        span.innerHTML = ` <strong>Author:</strong> ${question.author}`;
                        span2.innerHTML = `${question.body} <br>`;
                        span3.innerHTML = ` <strong>Topic:</strong> ${question.topic} <br>`;
                        a.innerHTML = 'view answers';
        //                 Qtn.innerHTML = li
                        append(li, span3);
                        append(li, span2);
                        append(li, span);
                        append(li, a);
                        append(Qtn, li);
                        append(Qtns, Qtn);
                        submit.addEventListener('click', post=>{
                            postQuestion();
                        })
                    }
                }
            }
        })

        .catch(error => console.log(error));
    }
    
}
    
function postQuestion(){
    let topic = document.getElementById('topic').value;
        body = document.getElementById('body').value;
        postData = {
            topic,
            body,
        };

    console.log(`${postData}`);
    if (document.title=="StackOverflow-lite-index")
        fetch('http://localhost:5000/api/v1/questions', {
            method: "POST",
            mode: "cors",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem('access')}`,
                "content-type": "application/json"},
            body: JSON.stringify(postData) 
        })
        .then(res => res.json())
        .then(json => {
            console.log(json);
            console.log(json.status_code);
            console.log(JSON.stringify(json));

            if ("message" in json || "msg" in json){
                alertMessage(json.message);
                alertMessage(json.msg);
            }
            if ("success" in json){
                window.location.reload();
                console.log('this runs');
            }
        })
        .catch(error => console.log(error));
    }

function postAnswer(questionId){
    let body = document.getElementById('body').value;
        postData = {
            body
        };

    console.log(`${postData}`);
    if (document.title=="StackOverflow-lite-question")
        fetch(`http://localhost:5000/api/v1/questions/${questionId}/answers`, {
            method: "POST",
            mode: "cors",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem('access')}`,
                "content-type": "application/json"},
            body: JSON.stringify(postData) 
        })
        .then(res => res.json())
        .then(json => {
            console.log(json);
            console.log(json.status_code);
            console.log(JSON.stringify(json));

            if ("message" in json || "msg" in json){
                alertMessage(json.message);
                alertMessage(json.msg);
            }
            if ("success" in json){
                window.location.reload();
                console.log('this runs');
            }
        })
        .catch(error => console.log(error));
    }

