function _fetch(url, method, body, refresh = true) {
    fetch(url, {
    method: method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  })
    .then((response) => response.text)
    .then((data) => {
      console.log("Server response:", data);
      if (refresh) {
            window.location.href = '/';
      }
    })
    .catch((error) => console.error("Error:", error));
}


function setDefaultUser(userID) {
  _fetch("selected-user", "PUT", {id: userID});
}

function deleteUser(userID) {
  _fetch(`/users/${userID}`, "DELETE");
}

function updateUser(userID) {
    const name = document.getElementById("username").value.trim();
    const token = document.getElementById("token").value.trim();
  _fetch(`/users/${userID}`, "PUT", {name, token});
}

function newUser() {
    const name = document.getElementById("username").value.trim();
    const token = document.getElementById("token").value.trim();
  _fetch(`/users/new`, "PUT", {name, token});
}