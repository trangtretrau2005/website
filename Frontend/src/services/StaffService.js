import API_BASE_URL from "../config.js";

// Fetch personnel for an event
const fetchStaffs = async (eventId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/personnel/event/${eventId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
      },
    });

    const data = await response.json();

    const mappedData = data.map((staff) => ({
      ten: staff.name,
      mssv: staff.student_code,
      vaitro: staff.role,
    }));

    return mappedData;
  } catch (error) {
    console.error("Error fetching staffs:", error);
    throw error;
  }
};

// Add personnel to an event
const addStaff = async (staffData, eventId) => {
  try {
    const mappedData = {
      name: staffData.ten,
      student_code: staffData.mssv,
      role: staffData.vaitro,
      event_id: eventId,
    };

    const response = await fetch(`${API_BASE_URL}/personnel/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
      },
      body: JSON.stringify(mappedData),
    });

    if (!response.ok) {
      throw new Error("Failed to add staff");
    }

    const data = await response.json();
    return data; // Return the added staff data
  } catch (error) {
    console.error("Error adding staff:", error);
    throw error;
  }
};

const addStaffs = async (staffsData, eventId) => {
  try {
    // Map each staff to the API request
    const requests = staffsData.map((staff) => {
      const mappedData = {
        name: staff.ten,
        student_code: staff.mssv,
        role: staff.vaitro,
        event_id: eventId,
      };

      return fetch(`${API_BASE_URL}/personnel/create`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "69420"
        },
        body: JSON.stringify(mappedData),
      });
    });

    // Run all requests in parallel
    const responses = await Promise.all(requests);

    // Check for any failed requests
    const failedResponses = responses.filter((response) => !response.ok);
    if (failedResponses.length > 0) {
      throw new Error("Some staff could not be added.");
    }

    // Parse all successful responses
    const data = await Promise.all(responses.map((response) => response.json()));
    return data; // Return the added staff data
  } catch (error) {
    console.error("Error adding staffs:", error);
    throw error;
  }
};

// Update personnel information
const updateStaff = async (mssv, staffData, eventId) => {
  try {
    const mappedData = {
      name: staffData.ten,
      student_code: staffData.mssv,
      role: staffData.vaitro,
      event_id: eventId,
    };

    const response = await fetch(`${API_BASE_URL}/personnel/update/${mssv}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
      },
      body: JSON.stringify(mappedData),
    });

    if (!response.ok) {
      throw new Error("Failed to update staff");
    }

    const data = await response.json();
    return data; // Return the updated staff data
  } catch (error) {
    console.error("Error updating staff:", error);
    throw error;
  }
};

// Delete personnel
const deleteStaff = async (mssv) => {
  try {
    const response = await fetch(`${API_BASE_URL}/personnel/delete/${mssv}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
      },
    });

    if (!response.ok) {
      throw new Error("Failed to delete staff");
    }

    return true; // Return true if the staff was deleted successfully
  } catch (error) {
    console.error("Error deleting staff:", error);
    throw error;
  }
};

export { fetchStaffs, addStaff, addStaffs, updateStaff, deleteStaff };