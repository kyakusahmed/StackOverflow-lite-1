
function createNode(element){
    return document.createElement(element);
}

function append(parent, element){
    return parent.appendChild(element)
}

let alertMessage = (message) => {
    let alert = document.getElementById('alert');
    alert.style.display = 'block';
    alert.style.padding = '10px';
    alert.innerHTML = message;
    setTimeout(() => alert.style.display = 'none', 6000);
}


function signUp(){
    // e.preventDefault();
    let username = document.getElementById('username').value;
        email = document.getElementById('email').value;
        password = document.getElementById('password').value;
        repeat_password = document.getElementById('repeat_password').value;
        signUpData = {
            username,
            email,
            password,
            repeat_password
        };

    console.log(`${signUpData}`);
    if (document.title=="StackOverflow-lite-signup")
        fetch('http://localhost:5000/api/v1/auth/signup', {
            method: "POST",
            mode: "cors",
            headers: {"content-type": "application/json"},
            body: JSON.stringify(signUpData) 
        })
        .then(res => res.json())
        .then(json => {
            console.log(json);
            console.log(json.status_code)
            console.log(JSON.stringify(json));
            let subimt = document.getElementById('submit');
            if ("message" in json){
                submit.href = '#';
                alertMessage(json.message);
            }
            if ("success" in json){
                alertMessage(json.success);
                window.location.replace('./login.html');
                console.log('this runs');
            }
        })
        .catch(error => console.log(error));
    }


    function login(){
        let username = document.getElementById('username').value;
            password = document.getElementById('password').value;
            loginData = {
                username,
                password,
            };
    
        console.log(`${loginData}`);
        if (document.title=="StackOverflow-lite-login")
            fetch('http://localhost:5000/api/v1/auth/login', {
                method: "POST",
                mode: "cors",
                headers: {"content-type": "application/json"},
                body: JSON.stringify(loginData) 
            })
            .then(res => res.json())
            .then(json => {
                console.log(json);
                console.log(json.status_code)
                console.log(JSON.stringify(json));
                let subimt = document.getElementById('submit');
                if ("message" in json){
                    submit.href = '#';
                    alertMessage(json.message);
                }
                if ("access_token" in json){
                    console.log(json['access_token']);
                    localStorage.setItem('access', json['access_token']);
                    localStorage.setItem('user', username);
                    // window.localStorage.setItem('qtn_author',QuestAuthor);
                    window.location.replace('./index.html');
                    console.log('this runs');
                }
            })
            .catch(error => console.log(error));
        }