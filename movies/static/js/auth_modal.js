function openAuthModal() {
    const modal = document.getElementById("authModal");

    if (!modal) return;

    modal.classList.remove("hidden");
    document.body.style.overflow = "hidden";
}

function closeAuthModal() {
    const modal = document.getElementById("authModal");

    if (!modal) return;

    modal.classList.add("hidden");
    document.body.style.overflow = "";
}

function togglePassword(id, element) {
    const input = document.getElementById(id);

    if (!input) return;

    if (input.type === "password") {
        input.type = "text";
        element.textContent = "Hide";
    } else {
        input.type = "password";
        element.textContent = "Show";
    }
}

document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        closeAuthModal();
    }
});