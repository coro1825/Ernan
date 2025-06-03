document.addEventListener("DOMContenLoaded", function (){

    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
        const usernameInput = document.getElementById("username");
        const passwordInput = document.getElementById("password");
        const errorBox = document.getElementById("loginError");


        const zadnji = localStorage.getItem("zadnjiUporabnik");
        if (zadnji) usernameInput.value = zadnji;

        loginForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const username = usernameInput.value.trim();
            const password = passwordInput.value.trim();

            if (!username || !password) {
                errorBox.textContent = "Vsa polja morajo biti izpolnjena!";
                return;
            }

            errorBox.textContent = "Prijavljam...";

            fetch("/login", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams({ username, password })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success) {
                    localStorage.setItem("zadnjiUporabnik", username);
                    window.location.href = "/";
                } else {
                    errorBox.textContent = data.error;
                    errorBox.style.color = "red";
                    errorBox.style.animation = "blink 0.4s ease-in-out 3";
                }
            })
            .catch(error => {
                console.error("Napaka pri prijavi:", error);
                errorBox.textContent = "Strežniška napaka!";
            });
        });
    }


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

    function preklic(event, id) {
        event.preventDefault();        
        fetch("/api/preklici-rezervacijo", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id }) 
        })
        .then(res => res.json()) 
        .then(data => {
            if (data.success) {
                location.reload();
            } else {
                alert("Napaka pri preklicu rezervacije: " + (data.error || "Neznana napaka."));
            }
        })
        .catch(err => {
            alert("Napaka pri povezovanju s strežnikom.");
            console.error(err);
        });
    }

});