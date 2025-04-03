function showLogin(){
    document.getElementById("loginForm").style.display = "block";
}

function showSignup(){
    document.getElementById("signupForm").style.display = "block";
}

function closeModal(){
    document.getElementById("loginForm").style.display = "none";
    document.getElementById("signupForm").style.display = "none";
}

function login(){
    let email = document.getElementById("loginEmail").value;
    let password = document.getElementById("loginPassword").value;
    alert("prijavljen kot: " + email)
    closeModal();
}

function signup()