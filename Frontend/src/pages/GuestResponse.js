import React, { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";

export default function GuestResponse() {
  const location = useLocation();
  const [status, setStatus] = useState("");

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const response = params.get("status");
    setStatus(response);

    fetch("http://localhost:8000/api/guest-response", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        email: "guest@example.com", // Thay bằng email thật nếu bạn truyền qua query hoặc lưu localStorage
        status: response === "accept" ? "Đồng ý" : "Không tham gia",
      }),
    });
  }, [location.search]); // Đảm bảo chạy khi URL thay đổi

  return (
    <div style={{ padding: "50px", textAlign: "center" }}>
      {status === "accept" && <h2>Cảm ơn bạn đã xác nhận tham gia!</h2>}
      {status === "decline" && <h2>Chúng tôi rất tiếc vì bạn không thể tham gia.</h2>}
      {!status && <h2>Phản hồi không hợp lệ.</h2>}
    </div>
  );
}

