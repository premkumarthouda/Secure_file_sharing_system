
document.querySelectorAll(".tab-button").forEach(button => {
  button.addEventListener("click", () => {
    const tab = button.getAttribute("data-tab");

    document.querySelectorAll(".tab-button").forEach(btn => btn.classList.remove("active"));
    button.classList.add("active");

    document.querySelectorAll(".form").forEach(form => form.classList.remove("active"));
    document.getElementById(`${tab}Form`).classList.add("active");
  })
  });

const backend = "http://localhost:8000";
// Register
document.getElementById("registerForm").onsubmit = async (e) => {
    e.preventDefault();
    const email = document.getElementById("registerEmail").value;
    const password = document.getElementById("registerPassword").value;
    const role = document.getElementById("registerRole").value;
  
    const res = await fetch(`${backend}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, role })
    });
    const data = await res.json();
    alert(data.message);
  };
  
  // Login
  document.getElementById("loginForm").onsubmit = async (e) => {
    e.preventDefault();
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;
  
    const res = await fetch(`${backend}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password })
    });
  
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem("email", email);
      localStorage.setItem("role", data.role);
      window.location.href = "dashboard.html";
    } else {
      alert(data.detail);
    }
  };
