import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // Import for navigation
import Sidebar from "../components/Sidebar.js";
import Modal from "react-modal";
import { useEffect } from "react";
import {fetchEvents, createEvent, updateEvent, deleteEvent} from "../services/EventService.js"; 
import "../styles/sidebar-style.css";

const routes = [
  { path: "/events", name: "Danh sách sự kiện" },
];

export default function Event() {
  const [showModal, setShowModal] = useState(false);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [currentEvent, setCurrentEvent] = useState({ name: "", date: "", location: "" });
  const [events, setEvents] = useState([]);
  const [eventToDelete, setEventToDelete] = useState(null);
  const navigate = useNavigate(); // Hook for navigation

  useEffect(() => {
    fetchEventsData();
  }, []);

  const fetchEventsData = async () => {
    const fetchedEvents = await fetchEvents();
    setEvents(fetchedEvents);
  };

  const openModal = (event = null) => {
    if (event) {
      setIsEditing(true);
      setCurrentEvent(event);
    } else {
      setIsEditing(false);
      setCurrentEvent({ name: "", date: "", location: "" });
    }
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setCurrentEvent({ name: "", date: "", location: "" });
  };

  const openConfirmModal = (event) => {
    setEventToDelete(event);
    setShowConfirmModal(true);
  };

  const closeConfirmModal = () => {
    setEventToDelete(null);
    setShowConfirmModal(false);
  };

  const handleDelete = async () => {

    await deleteEvent(eventToDelete.id); // Call the delete function from the service
    await fetchEventsData(); // Refresh the events list after deletion
    closeConfirmModal();
  };

  const handleSave = async () => {
    if (currentEvent.name && currentEvent.date && currentEvent.location) {
      if (isEditing) {
        await updateEvent(currentEvent.id, currentEvent);
        await fetchEventsData();
      } else {
        await createEvent(currentEvent);
        await fetchEventsData();
      }
      closeModal();
    } else {
      alert("Vui lòng điền đầy đủ thông tin sự kiện.");
    }
  };

  const navigateToDetail = (event) => {
    navigate(`/events/${event.id}/staffs`); // Pass eventId as part of the URL path
  };

  const customStyles = {
    content: {
      top: "50%",
      left: "50%",
      right: "auto",
      bottom: "auto",
      marginRight: "-50%",
      transform: "translate(-50%, -50%)",
    },
  };
  const [showNotification, setShowNotification] = useState(false);
  const notificationMessages = [
    "Người A đã đồng ý tham gia sự kiện.",
    "Người B không tham gia.",
    "Sự kiện C sắp diễn ra",
  ];
  return (
    <div className="sidebar-container">
      <Sidebar routes={routes} />

      <div className="main-container">
        {/* Sidebar */}
        <aside className="flex items-center justify-center">
          <h2 className="text-xl font-semibold text-gray-800">Nhóm 5</h2>
        </aside>

        {/* Add Event Button */}
        <div className="mt-2">
          <button
            onClick={() => openModal()}
            className="text-sm bg-indigo-600 text-white px-6 py-2 mb-4 rounded-md shadow-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-all"
          >
            Thêm sự kiện
          </button>
        </div>

        {/* Main Content */}
        <main className="flex-1 bg-gray-50 p-8">
          <div className="flex justify-between items-center mb-6">
            <h1 className="text-2xl font-bold text-gray-800 mb-6">Danh sách sự kiện</h1>
            <div className="flex items-center gap-2">
              <input
                type="text"
                placeholder="Lọc..."
                className="border border-gray-300 rounded px-3 py-1"
              />
            </div>
          </div>

          {/* Event Table */}
          <div className="bg-white rounded shadow p-4">
            <table className="w-full text-left">
              <thead>
                <tr className="border-b">
                  <th className="py-2 font-semibold text-gray-700">Tên sự kiện</th>
                  <th className="py-2 font-semibold text-gray-700">Ngày giờ</th>
                  <th className="py-2 font-semibold text-gray-700">Địa điểm</th>
                  <th className="py-2"></th>
                </tr>
              </thead>
              <tbody>
                {events.map((event, index) => (
                  <tr key={index} className="border-b hover:bg-gray-50">
                    <td className="py-2">{event.name}</td>
                    <td className="py-2">{event.date}</td>
                    <td className="py-2">{event.location}</td>
                    <td className="py-2 flex gap-2">
                      <button
                        onClick={() => navigateToDetail(event)}
                        className="text-sm bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
                      >
                        Chi tiết
                      </button>
                      <button
                        onClick={() => openModal(event)}
                        className="text-sm bg-yellow-400 text-white px-3 py-1 rounded hover:bg-yellow-500"
                      >
                        Sửa
                      </button>
                      <button
                        onClick={() => openConfirmModal(event)}
                        className="text-sm bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                      >
                        Xóa
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </main>

        {/* Modal Dialog */}
        {showModal && (
          <Modal
            isOpen={showModal}
            onRequestClose={closeModal}
            style={customStyles}
            contentLabel={isEditing ? "Edit Event" : "Add Event"}
          >
            <h2 className="text-xl font-semibold mb-6">
              {isEditing ? "Chỉnh sửa sự kiện" : "Thêm sự kiện mới"}
            </h2>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Tên sự kiện:
                </label>
                <input
                  type="text"
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="Nhập tên sự kiện..."
                  value={currentEvent.name}
                  onChange={(e) =>
                    setCurrentEvent({ ...currentEvent, name: e.target.value })
                  }
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Ngày giờ:
                </label>
                <input
                  type="datetime-local"
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  value={currentEvent.date}
                  onChange={(e) =>
                    setCurrentEvent({ ...currentEvent, date: e.target.value })
                  }
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700">
                  Địa điểm:
                </label>
                <input
                  type="text"
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                  placeholder="Nhập địa điểm..."
                  value={currentEvent.location}
                  onChange={(e) =>
                    setCurrentEvent({
                      ...currentEvent,
                      location: e.target.value,
                    })
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
                {isEditing ? "Lưu thay đổi" : "Thêm sự kiện"}
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

        {/* Confirm Delete Modal */}
        {showConfirmModal && (
          <Modal
            isOpen={showConfirmModal}
            onRequestClose={closeConfirmModal}
            style={customStyles}
            contentLabel="Confirm Delete"
          >
            <h2 className="text-xl font-semibold mb-6">Xác nhận xóa</h2>
            <p className="mb-6">Bạn có chắc chắn muốn xóa sự kiện này?</p>
            <div className="flex justify-center items-center gap-4">
              <button
                onClick={handleDelete}
                className="text-sm bg-red-500 text-white px-6 py-2 w-48 rounded-md shadow-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400 focus:ring-offset-2 transition-all"
              >
                Xóa
              </button>
              <button
                onClick={closeConfirmModal}
                className="text-sm bg-gray-500 text-white px-6 py-2 w-48 rounded-md shadow-md hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-400 focus:ring-offset-2 transition-all"
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