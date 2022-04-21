function post(url, params={}){
    var params_post = []
    for(const key in params){
        params_post.push(`${key}=${params[key]}`)
    }
    var xhr = new XMLHttpRequest();
    xhr.open("POST", url, false);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded')
    xhr.send(params_post.join("&"))
    return JSON.parse(xhr.responseText)
}

function login(){
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var result = post("/api/login", {"username":username, "password":password});

    if(result["logged_in"]){
        document.location.replace("/challenges/")
    }
    else{
        document.getElementById("message").innerText = "Identifiants invalides";
        document.getElementById("message").style.color = "red";
    }
}

function register(){
    var first_name = document.getElementById("first_name").value;
    var last_name = document.getElementById("last_name").value;
    var username = document.getElementById("username").value;
    var password = document.getElementById("password").value;
    var result = post(
        "/api/register", 
        {
            "first_name":first_name,
            "last_name":last_name,
            "username":username,
            "password":password
        }
    )

    if(result["registered"]){
        document.location.replace("/challenges/")
    }
    else{
        document.getElementById("message").innerText = result["message"];
        document.getElementById("message").style.color = "red";
    }
}

function submit_flag(chall_id){
    var input = document.getElementById(`input${chall_id}`);
    var points_displayed = document.getElementById("points_displayed");
    var span = document.getElementById(`result${chall_id}`);

    var flag_submitted = input.value;

    var result = post("/api/flag", {"chall_id":parseInt(chall_id), "flag":flag_submitted})

    var validated = result["validated"]
    var color = result["color"];
    var text = result["message"];
    var earned_points = result["earned_points"]
    
    var current_points = parseInt(points_displayed.innerText.split(" ")[0])

    points_displayed.innerText = `${earned_points + current_points} Points`
    input.style.border = "1px solid " + color;
    span.innerText = text;
    span.style.color = color;

    if(validated){
        var panel = document.getElementById(`panel${chall_id}`);
        var title = document.getElementById(`title${chall_id}`);
        panel.classList.add("panel-solved")
        panel.classList.remove("panel-default")
        title.classList.add("title-solved")
        title.classList.remove("title-default")
    }

    setTimeout(function(){
        input.style.border = null;
        span.innerText = null;
    }, 2000);
}

function get_leaderboard(){
    var leaderboard = post("/api/leaderboard");
    var table_body = document.getElementById("leaderboard_body");
    table_body.innerHTML = "";
    for(let i = 0; i < leaderboard.length; i++){
        var tr = document.createElement("tr");
        table_body.appendChild(tr);

        var th = document.createElement("th");
        th.setAttribute("scope", "row");
        th.innerText = leaderboard[i][0]
        tr.appendChild(th);
        
        var td1 = document.createElement("td");
        td1.innerText = leaderboard[i][1]
        tr.appendChild(td1);

        var td2 = document.createElement("td");
        td2.innerText = leaderboard[i][2]
        tr.appendChild(td2);
    }
}