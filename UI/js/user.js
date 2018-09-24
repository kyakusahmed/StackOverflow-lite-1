
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
                // window.location.reload();
                console.log('this runs');
            }
        })
        .catch(error => console.log(error));
    }
