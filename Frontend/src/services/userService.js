import API_BASE_URL from "../config.js";

// Register a new user
async function register(username, password) {
  try {
    const response = await fetch(`${API_BASE_URL}/user/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      throw new Error("Failed to register user");
    }

    const data = await response.json();
    return data; // Return the registered user data
  } catch (err) {
    console.error("Error during registration:", err);
    throw err;
  }
}

// Login a user
async function login(username, password) {
  try {
    const response = await fetch(`${API_BASE_URL}/user/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
      },
      body: JSON.stringify({ username, password }),
    });

    if (!response.ok) {
      throw new Error("Failed to login");
    }

    const data = await response.json();
    // localStorage.setItem("authToken", data.token); // Save token to localStorage
    return data; // Return the logged-in user data (e.g., token or user info)
  } catch (err) {
    console.error("Error during login:", err);
    throw err;
  }
}

// Logout a user
function logout() {
  try {
    localStorage.removeItem("authToken"); // Remove token from localStorage
    console.log("User logged out successfully");
  } catch (err) {
    console.error("Error during logout:", err);
    throw err;
  }
}

export default { register, login, logout };