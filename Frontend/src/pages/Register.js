import React, { useState } from "react";
import "../styles/style.css";
import userService from "../services/userService";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false); // Add loading state

  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent the default form submission behavior
    setLoading(true); // Set loading to true when API call starts

    try {
      const newUser = await userService.register(username, password);
      setMessage(`Tài khoản đã được tạo thành công! ID: ${newUser.id}`);
      setUsername("");
      setPassword("");
      window.location.href = "/login";
    } catch (err) {
      console.error("Error during registration:", err);
      setMessage("Đã xảy ra lỗi khi tạo tài khoản. Vui lòng thử lại.");
    } finally {
      setLoading(false); // Set loading to false when API call ends
    }
  };

  return (
    <div className="container">
      <h2>Tạo tài khoản mới</h2>
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

        <button className="register" type="submit" disabled={loading}>
          {loading ? "Đang xử lý..." : "Đăng ký"}
        </button>
      </form>
      {message && <p style={{ color: "red", marginTop: "6px" }}>{message}</p>}
      <div className="login-link">
        Đã có tài khoản? <a href="/login">Đăng nhập</a>
      </div>
    </div>
  );
}

export default Register;