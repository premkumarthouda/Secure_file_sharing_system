const backend = "http://localhost:8000";

const dashEmail = localStorage.getItem("email");
const dashRole = localStorage.getItem("role");
document.getElementById("roleHeader").innerText = `Logged in as ${dashRole}`;

async function setupDashboard() {
  if (dashRole === "ops") {
    document.getElementById("opsSection").style.display = "block";
    document.getElementById("uploadForm").onsubmit = async (e) => {
      e.preventDefault();
      const fileInput = document.getElementById("uploadFile");
      const clientEmail = document.getElementById("clientEmail").value;
      const formData = new FormData();
      formData.append("file", fileInput.files[0]);
      formData.append("client_email", clientEmail);

      const res = await fetch(`${backend}/upload?email=${dashEmail}`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      alert(data.message);
    };
  } else if (dashRole === "client") {
    document.getElementById("clientSection").style.display = "block";

    const res = await fetch(`${backend}/files?email=${dashEmail}`);
    const files = await res.json();
    const list = document.getElementById("fileList");
    list.innerHTML = ""; // Clear previous entries

    files.forEach((file) => {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.innerText = file.filename;
      a.href = `${backend}/files/download/${file.id}?email=${dashEmail}`;
      a.download = file.filename;
      li.appendChild(a);
      list.appendChild(li);
    });
  }
}

setupDashboard();
