import React, { useState, useEffect } from "react";
import Sidebar from "../components/Sidebar.js";
import Modal from "react-modal";
import { useParams } from "react-router-dom";
import { fetchStaffs, addStaff, addStaffs, updateStaff, deleteStaff } from "../services/StaffService.js";
import "../styles/staff-style.css";
import "../styles/sidebar-style.css";

function Staff() {
  const { eventId } = useParams(); 
  const [staffData, setStaffData] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [currentStaff, setCurrentStaff] = useState({ ten: "", mssv: "", vaitro: "" });
  const [routes, setRoutes] = useState([]);
  const [isEditing, setIsEditing] = useState(false);

  // Fetch staff data when the component mounts
  useEffect(() => {
    if (eventId) {
      loadStaffs();
      setRoutes([
        { path: `/events/${eventId}/staffs`, name: "Quản lý nhân sự" },
        { path: `/events/${eventId}/guests`, name: "Quản lý khách mời" },
      ]);
    }
  }, [eventId]);

  const openModal = (staff = null) => {
    setIsEditing(!!staff);
    if (staff) {
      setCurrentStaff(staff);
    } else {
      setCurrentStaff({ ten: "", mssv: "", vaitro: "" });
    }
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setCurrentStaff({ ten: "", mssv: "", vaitro: "" });
  };

  const handleSave = async () => {
    try {
      if (currentStaff.ten && currentStaff.mssv && currentStaff.vaitro) {
        if (staffData.some((staff) => staff.mssv === currentStaff.mssv)) {
          // Update existing staff
          await updateStaff(currentStaff.mssv, currentStaff, eventId);
          loadStaffs();
        } else {
          // Add new staff
          await addStaff(currentStaff, eventId);
          loadStaffs();
        }
        closeModal();
      } else {
        alert("Vui lòng điền đầy đủ thông tin!");
      }
    } catch (error) {
      console.error("Error saving staff:", error);
    }
  };

  const loadStaffs = async () => {
    try {
      const data = await fetchStaffs(eventId);
      setStaffData(data);
    } catch (error) {
      console.error("Error loading staff data:", error);
    }
  };

  const handleDelete = async (staffId) => {
    try {
      const isDeleted = await deleteStaff(staffId);
      if (isDeleted) {
        setStaffData((prevData) => prevData.filter((staff) => staff.mssv !== staffId));
      }
    } catch (error) {
      console.error("Error deleting staff:", error);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    const reader = new FileReader();
  
    reader.onload = async function (e) {
      const content = e.target.result;
      let newStaffs = [];
  
      if (file.name.endsWith('.json')) {
        try {
          const data = JSON.parse(content);
          if (Array.isArray(data)) {
            newStaffs = data;
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
  
          newStaffs = lines.slice(1).map(line => {
            const values = line.split(";");
            return {
              ten: values[0].trim(),
              mssv: values[1].trim(),
              vaitro: values[2].trim()
            };
          });  
        } catch (err) {
          alert("Lỗi khi đọc file CSV: " + err.message);
        }
      } else {
        alert("Vui lòng tải lên file .json hoặc .csv");
      }

      if (newStaffs.length > 0) {
        const filterNewStaffs = newStaffs.filter(staff => {
          return !staffData.some(existingStaff => existingStaff.mssv === staff.mssv);
        });
        await addStaffs(filterNewStaffs, eventId);
        loadStaffs();
      }
    };
  
    reader.readAsText(file, "UTF-8");
  };

  const renderTable = () => {
    return staffData.map((staff, index) => (
      <tr key={index}>
        <td>{staff.mssv}</td>
        <td>{staff.ten}</td>
        <td>{staff.vaitro}</td>
        <td className="flex gap-2">
          <button
            onClick={() => openModal(staff)}
            className="text-sm bg-yellow-400 text-white px-3 py-1 rounded hover:bg-yellow-500"
          >
            Cập nhật
          </button>
          <button
            onClick={() => handleDelete(staff.mssv)}
            className="text-sm bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
          >
            Xóa
          </button>
        </td>
      </tr>
    ));
  };

  return (
    <div className="sidebar-container">
      <Sidebar routes={routes} />

      <div className="main-container">
        <div className="header">
          <h2>Quản lý nhân sự</h2>
        </div>

        <div className="actions">
          <label>
            <button
              onClick={() => document.getElementById("fileInput").click()}
              className="text-sm bg-gray-600 text-white px-6 py-2 mb-4 rounded-md shadow-md hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 transition-all h-12"
            >
              Tải danh sách nhân sự
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
            Thêm nhân sự
          </button>
        </div>

        <table id="staffTable">
          <thead>
            <tr>
              <th>Mã sinh viên</th>
              <th>Tên</th>
              <th>Vai trò</th>
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
            contentLabel="Edit Staff"
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
              {isEditing ? "Cập nhật nhân sự" : "Thêm nhân sự"}
            </h2>
            <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                  Mã sinh viên:
                </label>
                <input
                  type="text"
                  className={`mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm ${
                    isEditing ? "bg-gray-100 cursor-not-allowed" : ""
                  }`}
                  placeholder="Nhập mã sinh viên..."
                  value={currentStaff.mssv}
                  onChange={(e) =>
                    setCurrentStaff({ ...currentStaff, mssv: e.target.value })
                  }
                  disabled={!!isEditing} // Disable the field in edit mode
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Họ tên:
                </label>
                <input
                  type="text"
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="Nhập tên..."
                  value={currentStaff.ten}
                  onChange={(e) =>
                    setCurrentStaff({ ...currentStaff, ten: e.target.value })
                  }
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Vai trò:
                </label>
                <input
                  type="text"
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="Nhập vai trò..."
                  value={currentStaff.vaitro}
                  onChange={(e) =>
                    setCurrentStaff({ ...currentStaff, vaitro: e.target.value })
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
    </div>
  );
}

export default Staff;