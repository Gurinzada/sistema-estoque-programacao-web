const form = document.getElementById("loginForm");

const errorMessages = {
  user_not_found:
    "Usuário não cadastrado. O login com Google é permitido apenas para contas existentes.",
  auth_failed: "Falha na autenticação. Tente novamente.",
  generic_error: "Ocorreu um erro. Por favor, tente novamente.",
};

const urlParams = new URLSearchParams(window.location.search);
const errorKey = urlParams.get("error");

if (errorKey && errorMessages[errorKey]) {
  const errorDiv = document.getElementById("auth-error");
  errorDiv.textContent = errorMessages[errorKey];
  errorDiv.style.display = "block";
  history.replaceState(null, "", window.location.pathname);
}

if (window.location.hash.includes("#token=")) {
  const hash = window.location.hash.substring(1);
  const params = new URLSearchParams(hash);
  const token = params.get("token");

  if (token) {
    localStorage.setItem("token", token);
    window.location.hash = "";
    window.location.href = "/dashboard";
  }
}

if (form) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (email.trim() === "" || password.trim() === "") return;

    const response = await fetch("/api/login", {
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ email, password }),
      method: "POST",
    });

    const data = await response.json();

    if (response.ok) {
      localStorage.setItem("token", data.access);
      localStorage.setItem("refresh", data.refresh);
      window.location.href = "/dashboard";
    } else {
      console.error("Login failed:", data);
    }
  });
}
