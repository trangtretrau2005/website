import API_BASE_URL from "../config.js";

// Fetch guests for an event
const fetchGuests = async (eventId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/guests/event/${eventId}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
      },
    });

    const data = await response.json();

    const mappedData = data.map((guest) => ({
      id: guest.id,
      ten: guest.name,
      email: guest.email,
      status: guest.response_status,
    }));

    return mappedData;
  } catch (error) {
    console.error("Error fetching guests:", error);
    throw error;
  }
};

// Add a guest to an event
const addGuest = async (guestData, eventId) => {
  try {
    const mappedData = {
      name: guestData.ten,
      email: guestData.email,
      event_id: eventId,
    };

    const response = await fetch(`${API_BASE_URL}/guests/create`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
      },
      body: JSON.stringify(mappedData),
    });

    if (!response.ok) {
      throw new Error("Failed to add guest");
    }

    const data = await response.json();
    return data; // Return the added guest data
  } catch (error) {
    console.error("Error adding guest:", error);
    throw error;
  }
};

// Add multiple guests to an event
const addGuests = async (guestsData, eventId) => {
  try {
    // Map each guest to the API request
    const requests = guestsData.map((guest) => {
      const mappedData = {
        name: guest.ten,
        email: guest.email,
        event_id: eventId,
      };

      return fetch(`${API_BASE_URL}/guests/create`, {
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
      throw new Error("Some guests could not be added.");
    }

    // Parse all successful responses
    const data = await Promise.all(responses.map((response) => response.json()));
    return data; // Return the added guests data
  } catch (error) {
    console.error("Error adding guests:", error);
    throw error;
  }
};

// Update guest information
const updateGuest = async (guestId, guestData, eventId) => {
  try {
    const mappedData = {
      name: guestData.ten,
      email: guestData.email,
      event_id: eventId,
    };

    const response = await fetch(`${API_BASE_URL}/guests/update/${guestId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
      },
      body: JSON.stringify(mappedData),
    });

    if (!response.ok) {
      throw new Error("Failed to update guest");
    }

    const data = await response.json();
    return data; // Return the updated guest data
  } catch (error) {
    console.error("Error updating guest:", error);
    throw error;
  }
};

// Delete a guest
const deleteGuest = async (guestId) => {
  try {
    const response = await fetch(`${API_BASE_URL}/guests/delete/${guestId}`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
      },
    });

    if (!response.ok) {
      throw new Error("Failed to delete guest");
    }

    return true; // Return true if the guest was deleted successfully
  } catch (error) {
    console.error("Error deleting guest:", error);
    throw error;
  }
};

const sendInvitations = async (guests, eventId) => {
  try {
    const filterGuests = guests.filter(guest => !!guest.id && guest.status !== "Đồng ý" && guest.status !== "Không đồng ý");
    const response = await fetch(`${API_BASE_URL}/guests/send-invitations`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "ngrok-skip-browser-warning": "69420"
      },
      body: JSON.stringify({ "guest_ids": filterGuests.map(guest => guest.id), "event_id": eventId }),
    });

    if (!response.ok) {
      throw new Error("Failed to send invitations");
    }

    return true; // Return true if invitations were sent successfully
  } catch (error) {
    console.error("Error sending invitations:", error);
    throw error;
  }
};

export { fetchGuests, addGuest, addGuests, updateGuest, deleteGuest, sendInvitations };