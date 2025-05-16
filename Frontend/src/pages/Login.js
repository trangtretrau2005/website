import React, { useState } from "react";
import "../styles/style.css";
import userService from "../services/userService"; // Import the userService for API calls

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false); // Add loading state

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent the default form submission behavior
    setLoading(true); // Set loading to true when API call starts

    try {
      const response = await userService.login(username, password); // Call the login API
      setMessage("Đăng nhập thành công!");
      localStorage.setItem("userInfo", response.user); // Save the token to localStorage
      window.location.href = "/events"; // Redirect to the dashboard or another page
    } catch (err) {
      console.error("Error during login:", err);
      setMessage("Đăng nhập thất bại. Vui lòng kiểm tra thông tin và thử lại.");
    } finally {
      setLoading(false); // Set loading to false when API call ends
    }
  };

  return (
    <div className="container">
      <h2>Đăng nhập vào hệ thống</h2>
      <form onSubmit={handleSubmit}>
        <label htmlFor="username">Tên người dùng</label>
        <input
          type="text"
          id="username"
          placeholder="Nhập tên người dùng"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />

        <label htmlFor="password">Mật khẩu</label>
        <input
          type="password"
          id="password"
          placeholder="Nhập mật khẩu"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />

        <button className="login" type="submit" disabled={loading}>
          {loading ? "Đang xử lý..." : "Đăng nhập"}
        </button>
      </form>
      {message && <p style={{ color: "red", marginTop: "6px" }}>{message}</p>}
      <div className="register-link">
        Chưa có tài khoản? <a href="/register">Đăng ký</a>
      </div>
    </div>
  );
}

export default Login;