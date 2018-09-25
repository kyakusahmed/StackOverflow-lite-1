
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

let alertMain = (message) => {
    let alert = document.getElementById('alert2');
    alert.style.display = 'block';
    alert.style.padding = '10px';
    alert.innerHTML = message;
    setTimeout(() => alert.style.display = 'none', 6000);
}



function createNode(element){
    return document.createElement(element);
}

function append(parent, element){
    return parent.appendChild(element);
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
                        a2 = createNode('a');
                        a3 = createNode('a');
                        Qtn = createNode('p');
                        Qtns = document.getElementById('Qtns');
                        L = document.getElementById('L');
                        P = document.getElementById('P');
                        S = document.getElementById('S');
                        span4 = createNode('span');
                    

                    console.log(1, document.title=="StackOverflow-lite-index");
                    if (document.title=="StackOverflow-lite-index"){
                        a.setAttribute('href', 'question.html');
                        a.setAttribute('class', 'question_link');
                        a2.setAttribute('href', 'updateQuestion.html');
                        a2.setAttribute('class', 'question_link');
                        a3.setAttribute('class', 'delete_link');
                        console.log("href registerd");
                        console.log(document.title);
                        console.log(question.questionId);
                        a.onclick = link =>{
                            window.localStorage.setItem('questionId1', question.questionId);
                            window.location.replace('./question.html');

                        }
                        a2.onclick = link =>{
                            window.localStorage.setItem('questionId-edit', question.questionId);
                            window.location.replace('./updateQuestion.html');
                        }
                        a3.onclick = link =>{
                            deleteQuestion(question.questionId);
                            
                        }
                        qtn_author = question.author;
                        console.log('qtn auth', qtn_author, typeof(qtn_author));
                        console.log(window.localStorage.getItem('user'));
                        let submit = document.getElementById('submit');
                            condition5 = window.localStorage.getItem('user') == qtn_author;
                            condition6 = window.localStorage.getItem('user') == null;

                        console.log('cond 5', condition5);
                        if (!condition6 && condition5){
                            L.style.display = 'none';
                            S.style.display = 'none';
                            P.style.display = 'list-item';
                            console.log('then this hsould run');
                            span.innerHTML = ` <strong>Author:</strong> ${question.author}`;
                            span2.innerHTML = `${question.body} <br>`;
                            span3.innerHTML = ` <strong>Topic:</strong> ${question.topic} <br>`;
                            a.innerHTML = 'view answers';
                            a2.innerHTML = 'edit question';
                            a3.innerHTML = 'delete';
                            append(li, span3);
                            append(li, span2);
                            append(li, span);
                            append(span4, a);
                            append(span4, a2);
                            append(span4, a3);
                            append(li, span4);
                            append(Qtn, li);
                            append(Qtns, Qtn);
                        }

                        if (!condition5 || condition6){
                            P.style.display = 'none';
                            S.style.display = 'list-item';
                            L.style.display = 'list-item';
                            console.log('this runs?');
                            span.innerHTML = ` <strong>Author:</strong> ${question.author}`;
                            span2.innerHTML = `${question.body} <br>`;
                            span3.innerHTML = ` <strong>Topic:</strong> ${question.topic} <br>`;
                            a.innerHTML = 'view answers';
                           
                            append(li, span3);
                            append(li, span2);
                            append(li, span);
                            append(li, a);
                            append(Qtn, li);
                            append(Qtns, Qtn);
                        }
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
                if (json.msg == 'Token has expired' || json.msg == 'Not enough segments'){
                    alertMessage('Please login to continue!, redirecting to login page...');
                    setTimeout(() => window.location.replace('./login.html'), 3000);
                }
                // alertMessage(json.msg);
            }
            if ("success" in json){
                
                window.location.reload();
                console.log('this runs');
            }
        })
        .catch(error => console.log(error));
    }


function updateQuestion(questionId){
    let topic = document.getElementById('topic').value;
        body = document.getElementById('body').value;
        postData = {
            topic,
            body,
        };
    console.log(`${postData}`);
    if (document.title=="StackOverflow-lite-edit")
        fetch(`http://localhost:5000/api/v1/questions/${questionId}`, {
            method: "PATCH",
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
                console.log('this rubs here')
                if (json.msg == 'Token has expired' || json.msg == 'Not enough segments'){
                    alertMessage('Please login to continue!, redirecting to login page...');
                    setTimeout(() => window.location.replace('./login.html'), 3000);
                }
                // alertMessage(json.msg);
            }
            if ("success" in json){
                alertMessage('Success, question updated!');
                setTimeout(() => window.location.replace('./index.html'), 3000);
                
                console.log('this runs');
            }
        })
        .catch(error => console.log(error));
    }



function deleteQuestion(questionId){
    console.log(questionId);
    if (document.title=="StackOverflow-lite-index"){
        fetch(`http://localhost:5000/api/v1/questions/${questionId}`, {
            method: "DELETE",
            mode: "cors",
            headers: {
                "Authorization": `Bearer ${localStorage.getItem('access')}`,
                "content-type": "application/json"}
        })
        .then(res => res.json())
        .then(json => {
            console.log(json);
            console.log(json.status_code);
            console.log(JSON.stringify(json));

            if ("message" in json || "msg" in json){
                alertMain(json.message);
                if (json.msg == 'Token has expired' || json.msg == 'Not enough segments'){
                    alertMain('Please login to continue!, redirecting to login page...');
                    setTimeout(() => window.location.replace('./login.html'), 3000);
                }
                // alertMessage(json.msg);
            }
            if ("success" in json){
                alertMain(json.success);
                window.location.reload();
                console.log('this runs');
            }
        })
        .catch(error => console.log(error));
    }
}

function onEditQuestion(){
    questionId = window.localStorage.getItem('questionId-edit');
    console.log('questionId', questionId);
    
    if (document.title == "StackOverflow-lite-edit"){
        let Question = document.getElementById('oldQuest');
            submit = document.getElementById('submit');
            h3 = createNode('h3');
            li = createNode('li');
            span1 = createNode('span');
            span2 = createNode('span')
            a = createNode('a');
            b = createNode('b');
        
        fetch(`http://localhost:5000/api/v1/questions`)
        .then(res => res.json())
        .then(json=>{
            console.log(json);
            if ('questions' in json){
                for (let question of json.questions){
                    if (question.questionId == questionId){
                        h3.innerHTML = `${question.body}`;
                        span1.innerHTML = `<strong>Author: </strong>${question.author}`;
                        span2.innerHTML = `<strong>Topic: </strong>${question.topic}`;
                        
                        append(li, span2);
                        append(li, h3);
                        append(li, span1);
                        append(Question, li);
                        submit.addEventListener('click', edit =>{
                            updateQuestion(questionId);
                        })

                    }
                    
                }
            }
            if(!document.title == 'StackOverflow-lite-index' || !document.title=='StackOverflow-lite-edit'){
                window.localStorage.removeItem('questionId-edit');
            }
        })
    }

}

