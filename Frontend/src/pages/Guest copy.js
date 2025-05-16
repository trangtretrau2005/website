import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import "../styles/sidebar-style.css";
import "../styles/staff-style.css"; // dùng lại CSS chung

const routes = [
  { path: "/events/staffs", name: "Quản lý nhân sự" },
  { path: "/events/guests", name: "Quản lý khách mời" },
];

export default function Guest() {
  const [guest, setGuest] = useState([
    { ten: "Nguyen Van A", email: "anv@gmail.com", status: "Đồng ý" },
    { ten: "Le Van B", email: "le@gmail.com", status: "Chưa phản hồi" },
  ]);
  const [showAddForm, setShowAddForm] = useState(false);
  const [newGuest, setNewGuest] = useState({ ten: "", email: "", status: "" });
  const [showConfirm, setShowConfirm] = useState(false); // Xác nhận gửi

  const handleInputChange = (e) => {
    const { id, value } = e.target;
    setNewGuest((prev) => ({ ...prev, [id]: value }));
  };

  const addGuest = async () => {
    if (newGuest.ten && newGuest.email && newGuest.status) {
      try {
        // Gọi API để lưu vào DB
        const response = await fetch("http://localhost:8000/create", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            name: newGuest.ten,
            email: newGuest.email,
            check_status: newGuest.status,
            event_id: 1  // 👈 nếu bạn có event_id cụ thể
          }),
        });
  
        if (response.ok) {
          const savedGuest = await response.json();
          setGuest([...guest, {
            ten: savedGuest.name,
            email: savedGuest.email,
            status: savedGuest.check_status
          }]);
          setNewGuest({ ten: "", email: "", status: "" });
          setShowAddForm(false);
        } else {
          alert("❌ Không thể thêm khách mời vào cơ sở dữ liệu");
        }
      } catch (error) {
        console.error("Lỗi:", error);
        alert("❌ Lỗi kết nối backend");
      }
    } else {
      alert("Vui lòng điền đầy đủ thông tin!");
    }
  };
  
  

  const deleteGuest = (index) => {
    const updated = [...guest];
    updated.splice(index, 1);
    setGuest(updated);
  };

  const logout = () => {
    localStorage.removeItem("userInfo");
    window.location.href = "/login";
  };

  const reloadPage = () => {
    window.location.reload();
  };

  const sendInvitations = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/send-invitations", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ guests: guest }),
      });

      if (response.ok) {
        alert("✅ Gửi lời mời thành công!");
      } else {
        alert("❌ Gửi thất bại. Vui lòng thử lại.");
      }
    } catch (error) {
      console.error("Lỗi khi gửi lời mời:", error);
      alert("❌ Đã xảy ra lỗi.");
    }
  };

  return (
    <div className="sidebar-container">
      <Sidebar routes={routes} />

      <div className="main-container">
        <div className="header">
          <h2>Quản lí khách mời</h2>
          <div className="user">
            <span className="user-name">Xin chào, {localStorage.getItem("userInfo")}</span>
            <button className="reload-btn" onClick={reloadPage}>⟳</button>
            <button className="logout-btn" onClick={logout}>Đăng xuất</button>
          </div>
        </div>

        <div className="actions">
          <label>
            <button onClick={() => document.getElementById("guestFileInput").click()}>
              Tải danh sách khách mời
            </button>
            <input
              type="file"
              id="guestFileInput"
              accept=".json,.csv"
              style={{ display: "none" }}
              onChange={(event) => {
                const file = event.target.files[0];
                const reader = new FileReader();

                reader.onload = (e) => {
                  const content = e.target.result;

                  if (file.name.endsWith(".json")) {
                    try {
                      const data = JSON.parse(content);
                      if (Array.isArray(data)) {
                        setGuest(data);
                      } else {
                        alert("File JSON không hợp lệ.");
                      }
                    } catch (err) {
                      alert("Lỗi khi đọc file JSON: " + err.message);
                    }
                  } else if (file.name.endsWith(".csv")) {
                    try {
                      const lines = content.trim().split("\n");
                      const data = lines.slice(1).map((line) => {
                        const values = line.split(",");
                        return {
                          ten: values[0].trim(),
                          email: values[1].trim(),
                          status: values[2].trim(),
                        };
                      });
                      setGuest(data);
                    } catch (err) {
                      alert("Lỗi khi đọc file CSV: " + err.message);
                    }
                  } else {
                    alert("Vui lòng tải lên file .json hoặc .csv");
                  }
                };

                reader.readAsText(file);
              }}
            />
          </label>

          <button onClick={() => setShowAddForm(true)}>Thêm khách mời</button>
          <button style={{ marginLeft: "10px", background: "#10b981" }} onClick={() => setShowConfirm(true)}>
            Gửi lời mời
          </button>
        </div>

        {showConfirm && (
          <div style={{
            position: "fixed",
            top: 0, left: 0,
            width: "100%", height: "100%",
            backgroundColor: "rgba(0,0,0,0.5)",
            display: "flex", justifyContent: "center", alignItems: "center",
            zIndex: 1000
          }}>
            <div className="modal-confirm" style={{
              background: "white",
              padding: "30px",
              borderRadius: "10px",
              textAlign: "center",
              boxShadow: "0 4px 12px rgba(0,0,0,0.3)"
            }}>
              <h3>Bạn có chắc chắn muốn gửi lời mời cho tất cả khách mời?</h3>
              <div style={{ marginTop: "20px" }}>
                <button
                  style={{ marginRight: "10px", padding: "8px 16px" }}
                  onClick={() => {
                    sendInvitations();
                    setShowConfirm(false);
                  }}
                >
                  Có, gửi ngay
                </button>
                <button
                  style={{ padding: "8px 16px" }}
                  onClick={() => setShowConfirm(false)}
                >
                  Hủy
                </button>
              </div>
            </div>
          </div>
        )}

        {showAddForm && (
          <div className="addForm" style={{ marginTop: "20px", background: "#f1f5f9", padding: "20px", borderRadius: "8px" }}>
            <h3 style={{ marginBottom: "15px", fontSize: "20px", fontWeight: 600 }}>Thêm khách mời mới</h3>
            <label>Tên khách mời:</label>
            <input
              type="text"
              id="ten"
              placeholder="Nhập tên khách mời..."
              value={newGuest.ten}
              onChange={handleInputChange}
              required
            />

            <label>Email:</label>
            <input
              type="text"
              id="email"
              placeholder="Nhập email..."
              value={newGuest.email}
              onChange={handleInputChange}
              required
            />

            <label>Trạng thái:</label>
            <input
              type="text"
              id="status"
              placeholder="Nhập trạng thái..."
              value={newGuest.status}
              onChange={handleInputChange}
              required
            />

            <button onClick={addGuest}>Xác nhận thêm</button>
          </div>
        )}

        <table id="guestTable">
          <thead>
            <tr>
              <th>Tên khách mời</th>
              <th>Email</th>
              <th>Trạng thái</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {guest.map((ev, index) => (
              <tr key={index}>
                <td>{ev.ten}</td>
                <td>{ev.email}</td>
                <td>{ev.status}</td>
                <td><button onClick={() => deleteGuest(index)}>Xóa</button></td>
              </tr>
            ))}
          </tbody>
          <tbody>
  {guest.map((ev, index) => (
    <tr key={index}>
      <td>{ev.ten}</td>
      <td>{ev.email}</td>
      <td>{ev.status}</td>
      <td>
        <button
          onClick={() => {
            setNewGuest(ev);        // đổ dữ liệu khách mời đang chọn vào form
            setShowAddForm(true);   // bật form lên để sửa
          }}
          style={{ marginRight: "8px" }}
        >
          Sửa
        </button>
        <button onClick={() => deleteGuest(index)}>Xóa</button>
      </td>
    </tr>
  ))}
</tbody>

        </table>
      </div>
    </div>
  );
}
