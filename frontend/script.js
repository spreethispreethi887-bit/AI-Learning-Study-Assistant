document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const message = document.getElementById("message");

    if (name === "" || email === "" || password === "") {
        message.textContent = "Please fill in all fields.";
        return;
    }

    if (password.length < 6) {
        message.textContent = "Password must be at least 6 characters.";
        return;
    }

    localStorage.setItem("studentName", name);

    message.textContent = "Login successful! Welcome " + name + " 🎉";

    setTimeout(function() {
     window.location.href = "http://localhost:8501/?name=" + encodeURIComponent(name);
    }, 1000);
});