function openAuthModal() {
    document.getElementById("authModal").classList.remove("hidden");
    showEmailStep();
}

function closeAuthModal() {
    document.getElementById("authModal").classList.add("hidden");
}

async function showPasswordStep() {
    const identifier = document.getElementById("authIdentifier").value.trim();

    if (!identifier) {
        alert("Please enter your email or mobile number.");
        return;
    }

    const response = await fetch("/accounts/check-user/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCSRFToken(),
        },
        body: new URLSearchParams({
            identifier: identifier
        })
    });

    const data = await response.json();

    if (data.exists) {
        document.getElementById("loginUsername").value = identifier;

        document.getElementById("emailStep").classList.add("hidden");
        document.getElementById("passwordStep").classList.remove("hidden");
    } else {
        window.location.href = "/accounts/signup/";
    }
}

function showEmailStep() {
    document.getElementById("passwordStep").classList.add("hidden");
    document.getElementById("emailStep").classList.remove("hidden");
}

function togglePassword(id, el) {
    const input = document.getElementById(id);

    if (input.type === "password") {
        input.type = "text";
        el.innerText = "Hide";
    } else {
        input.type = "password";
        el.innerText = "Show";
    }
}

function getCSRFToken() {
    const name = "csrftoken";
    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {
        cookie = cookie.trim();

        if (cookie.startsWith(name + "=")) {
            return cookie.substring(name.length + 1);
        }
    }

    return "";
}
