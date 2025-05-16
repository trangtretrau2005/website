import React, { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar";
import Modal from "react-modal";
import { useParams } from "react-router-dom";
import { fetchGuests, addGuest, addGuests, updateGuest, deleteGuest, sendInvitations } from "../services/GuestService";
import "../styles/sidebar-style.css";
import "../styles/staff-style.css"; // Reuse common styles

export default function Guest() {
  const { eventId } = useParams(); // Get eventId from the URL
  const [guestData, setGuestData] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [currentGuest, setCurrentGuest] = useState({ ten: "", email: "", status: "" });
  const [routes, setRoutes] = useState([]);
  const [isEditing, setIsEditing] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false); // Xác nhận gửi
  const [showSuccessDialog, setShowSuccessDialog] = useState(false); // Gửi thành công
  const [errorMessage, setErrorMessage] = useState("");
  const [showErrorDialog, setShowErrorDialog] = useState(false); // Gửi thất bại


  // Fetch guest data when the component mounts
  useEffect(() => {
    if (eventId) {
      loadGuests();
      setRoutes([
        { path: `/events/${eventId}/staffs`, name: "Quản lý nhân sự" },
        { path: `/events/${eventId}/guests`, name: "Quản lý khách mời" },
      ]);
    }
  }, [eventId]);

  const openModal = (guest = null) => {
    setIsEditing(!!guest);
    if (guest) {
      setCurrentGuest(guest);
    } else {
      setCurrentGuest({ ten: "", email: "", status: "" });
    }
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setCurrentGuest({ ten: "", email: "", status: "" });
  };

  const handleSave = async () => {
    try {
      if (currentGuest.ten && currentGuest.email) {
        if (guestData.some((guest) => guest.email === currentGuest.email)) {
          // Update existing guest
          await updateGuest(currentGuest.id, currentGuest, eventId);
          loadGuests();
        } else {
          // Add new guest
          await addGuest(currentGuest, eventId);
          loadGuests();
        }
        closeModal();
      } else {
        alert("Vui lòng điền đầy đủ thông tin!");
      }
    } catch (error) {
      console.error("Error saving guest:", error);
    }
  };

  const loadGuests = async () => {
    try {
      const data = await fetchGuests(eventId);
      setGuestData(data);
    } catch (error) {
      console.error("Error loading guest data:", error);
    }
  };

  const handleDelete = async (guestId) => {
    try {
      await deleteGuest(guestId);
      await loadGuests(); // Reload guest data after deletion
    } catch (error) {
      console.error("Error deleting guest:", error);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
  
    reader.onload = async function (e) {
      const content = e.target.result;
      let newGuest = [];
  
      if (file.name.endsWith('.json')) {
        try {
          const data = JSON.parse(content);
          if (Array.isArray(data)) {
            newGuest = data;
          } else {
            alert("File JSON không hợp lệ.");
          }
        } catch (err) {
          alert("Lỗi khi đọc file JSON: " + err.message);
        }
  
      } else if (file.name.endsWith('.csv')) {
        try {
          const lines = content.trim().split("\n");
          const headers = lines[0].split(";");
  
          newGuest = lines.slice(1).map(line => {
            const values = line.split(";");
            return {
              ten: values[0].trim(),
              email: values[1].trim(),
            };
          });  
        } catch (err) {
          alert("Lỗi khi đọc file CSV: " + err.message);
        }
      } else {
        alert("Vui lòng tải lên file .json hoặc .csv");
      }

      if (newGuest.length > 0) {
        const filterNewGuest = newGuest.filter(staff => {
          return !guestData.some(existingGuest => existingGuest.email === staff.email);
        });
        await addGuests(filterNewGuest, eventId);
        loadGuests();
      }
    };
  
    reader.readAsText(file, "UTF-8");
  };

  const renderTable = () => {
    return guestData.map((guest, index) => (
      <tr key={index}>
        <td>{guest.ten}</td>
        <td>{guest.email}</td>
        <td>{guest.status}</td>
        <td className="flex gap-2">
          <button
            onClick={() => openModal(guest)}
            className="text-sm bg-yellow-400 text-white px-3 py-1 rounded hover:bg-yellow-500"
          >
            Cập nhật
          </button>
          <button
            onClick={() => handleDelete(guest.id)}
            className="text-sm bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
          >
            Xóa
          </button>
        </td>
      </tr>
    ));
  };

  const handleSendInvitations = async () => {
    try {
      const result = await sendInvitations(guestData, eventId); // Call the sendInvitations function
      setShowSuccessDialog(true);
    } catch (error) {
      setErrorMessage(error.message || "Đã xảy ra lỗi khi gửi lời mời.");
      setShowErrorDialog(true); // Show error dialog
    }
  };

  return (
    <div className="sidebar-container">
      <Sidebar routes={routes} />

      <div className="main-container">
        <div className="header">
          <h2>Quản lý khách mời</h2>
        </div>

        <div className="actions">
          <label>
            <button
              onClick={() => document.getElementById("fileInput").click()}
              className="text-sm bg-gray-600 text-white px-6 py-2 mb-4 rounded-md shadow-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-all h-12"
            >
              Tải danh sách khách mời
            </button>
            <input
              type="file"
              id="fileInput"
              accept=".json,.csv"
              style={{ display: "none" }}
              onChange={handleFileUpload}
            />
          </label>
          <button
            onClick={() => openModal()}
            className="text-sm bg-indigo-600 text-white px-6 py-2 mb-4 rounded-md shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all h-12"
          >
            Thêm khách mời
          </button>
          <button
          className="text-sm px-6 py-2 mb-4 rounded-md shadow-md bg-green-600 hover:bg-green-800 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all h-12"
          onClick={() => setShowConfirm(true)}>
            Gửi lời mời
          </button>
        </div>

        <table id="guestTable">
          <thead>
            <tr>
              <th>Tên khách mời</th>
              <th>Email</th>
              <th>Trạng thái</th>
              <th>Thao Tác</th>
            </tr>
          </thead>
          <tbody>{renderTable()}</tbody>
        </table>

        {/* Modal Dialog */}
        {showModal && (
          <Modal
            isOpen={showModal}
            onRequestClose={closeModal}
            contentLabel="Edit Guest"
            style={{
              content: {
                top: "50%",
                left: "50%",
                right: "auto",
                bottom: "auto",
                marginRight: "-50%",
                transform: "translate(-50%, -50%)",
              },
            }}
          >
            <h2 className="text-xl font-semibold mb-6">
              {isEditing ? "Cập nhật khách mời" : "Thêm khách mời"}
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Email:
                </label>
                <input
                  type="text"
                  className={`mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm ${
                    isEditing ? "bg-gray-100 cursor-not-allowed" : ""
                  }`}
                  placeholder="Nhập email..."
                  value={currentGuest.email}
                  onChange={(e) =>
                    setCurrentGuest({ ...currentGuest, email: e.target.value })
                  }
                  disabled={isEditing} // Disable the field in edit mode
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Tên khách mời:
                </label>
                <input
                  type="text"
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="Nhập tên khách mời..."
                  value={currentGuest.ten}
                  onChange={(e) =>
                    setCurrentGuest({ ...currentGuest, ten: e.target.value })
                  }
                  required
                />
              </div>
            </div>
            <div className="flex justify-center items-center gap-4 mt-6">
              <button
                onClick={handleSave}
                className="text-sm bg-blue-500 text-white px-6 py-2 w-48 rounded-md shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 transition-all"
              >
                Lưu thay đổi
              </button>
              <button
                onClick={closeModal}
                className="text-sm bg-red-500 text-white px-6 py-2 w-48 rounded-md shadow-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-offset-2 transition-all"
              >
                Hủy
              </button>
            </div>
          </Modal>
        )}
      </div>

      {showConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center z-50">
          <div className="bg-white rounded-lg shadow-lg p-6 w-96 text-center">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              Bạn có chắc chắn muốn gửi lời mời cho tất cả khách mời?
            </h3>
            <div className="flex justify-center gap-4 mt-6">
              <button
                className="bg-green-600 text-white px-4 py-2 rounded-md shadow-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2 transition-all"
                onClick={() => {
                  handleSendInvitations();
                  setShowConfirm(false);
                }}
              >
                Có, gửi ngay
              </button>
              <button
                className="bg-gray-300 text-gray-800 px-4 py-2 rounded-md shadow-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 transition-all"
                onClick={() => setShowConfirm(false)}
              >
                Hủy
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Success Dialog */}
        {showSuccessDialog && (
          <Modal
            isOpen={showSuccessDialog}
            onRequestClose={() => setShowSuccessDialog(false)}
            contentLabel="Success"
            style={{
              content: {
                top: "50%",
                left: "50%",
                right: "auto",
                bottom: "auto",
                marginRight: "-50%",
                transform: "translate(-50%, -50%)",
                padding: "20px",
                borderRadius: "10px",
                boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
              },
            }}
          >
            <h2 className="text-xl font-semibold mb-4 text-center">Thành công</h2>
            <p className="text-center mb-6">Lời mời đã được gửi thành công!</p>
            <div className="flex justify-center">
              <button
                className="bg-blue-500 text-white px-6 py-2 rounded-md shadow-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2 transition-all"
                onClick={() => setShowSuccessDialog(false)}
              >
                Đóng
              </button>
            </div>
          </Modal>
        )}

        {/* Error Dialog */}
        {showErrorDialog && (
          <Modal
            isOpen={showErrorDialog}
            onRequestClose={() => setShowErrorDialog(false)}
            contentLabel="Error"
            style={{
              content: {
                top: "50%",
                left: "50%",
                right: "auto",
                bottom: "auto",
                marginRight: "-50%",
                transform: "translate(-50%, -50%)",
                padding: "20px",
                borderRadius: "10px",
                boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
              },
            }}
          >
            <h2 className="text-xl font-semibold mb-4 text-center">Lỗi</h2>
            <p className="text-center mb-6">{errorMessage}</p>
            <div className="flex justify-center">
              <button
                className="bg-red-500 text-white px-6 py-2 rounded-md shadow-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-offset-2 transition-all"
                onClick={() => setShowErrorDialog(false)}
              >
                Đóng
              </button>
            </div>
          </Modal>
        )}
    </div>
  );
}