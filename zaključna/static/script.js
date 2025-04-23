document.addEventListener("DOMContentLoaded", function () {

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

    const signupForm = document.getElementById("signupForm");
    if (signupForm) {
        const newUsername = document.getElementById("newUsername");
        const newPassword = document.getElementById("newPassword");
        const signupError = document.getElementById("signupError");

        signupForm.addEventListener("submit", function (event) {
            event.preventDefault();

            const username = newUsername.value.trim();
            const password = newPassword.value.trim();

            if (!username || !password) {
                signupError.textContent = "Vsa polja morajo biti izpolnjena!";
                return;
            }

            fetch("/signup", {
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
                    signupError.textContent = data.error;
                    signupError.style.color = "red";
                    signupError.style.animation = "blink 0.4s ease-in-out 3";
                }
            })
            .catch(error => {
                console.error("Napaka pri registraciji:", error);
                signupError.textContent = "Napaka pri strežniku.";
            });
        });
    }

    const isciBtn = document.getElementById("isciVozila");
    if (isciBtn) {
        isciBtn.addEventListener("click", function () {
            const zacetek = document.getElementById(zacetek).value;
            const konec = document.getElementById("konec").value;

            if (!zacetek || !konec) {
                alert("izberi oba datuma!");
                return;
            }
        })
    }
});