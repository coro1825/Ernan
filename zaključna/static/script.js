document.addEventListener("DOMContenLoaded", function (){
    document.getElementById("loginForm")?.addEventListener("submit",function(event){
        event.preventDefault();

        let username = document.getElementById("username").value;
        let password = document.getElementById("password").value;

        fetch("/login", {
            method: "POST",
            headers: {"Content-Type": "application/x-www-form-urlencoded"},
            body: new URLSearchParams({username: username, password: password})
        })
        .then(Response => Response.json())
        .then(data => {
            if(data.success) {
                window.location.href = "/";
            } else{
                document.getElementById("loginError")
            }
        })
        .catch(error => console.error("Napaka pri prijavi:",error));
    });

    document.getElementById("signupForm")?.addEventListener("submit", function (event) {
        event.preventDefault();

        let username = document.getElementById("newUsername").value;
        let password = document.getElementById("newPassword").value;

        fetch("/signup",{
            method: "POST",
            headers: {"Content-Type": "application/x-www-form-urlencoded"},
            body: new URLSearchParams({username: username,password: password})
        })
        .then(Response => Response.json())
        .then(data => {
            if(data.success) {
                window.location.href = "/";
            } else{
                document.getElementById("signupError").textContent = data.error;
            }
        })
        .catch(error => console.error("Napaka pri registraciji", error));
    });
});