import API_BASE_URL from "../config.js";

const fetchEvents = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/events`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "69420"
        },
      });

      const data = await response.json();

      const mappedData = data.map((event) => ({
        ...event,
        date: event.event_date,
      }));
  
      return mappedData;
    } catch (error) {
      console.error("Error fetching events:", error);
      throw error;
    }
  };

  // Create a new event
async function createEvent(eventData) {
    try {
        const mappedData = {
            ...eventData,
            event_date: eventData.date,
            description: '',
        };
      const response = await fetch(`${API_BASE_URL}/events/create`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "69420"
        },
        body: JSON.stringify(mappedData),
      });
  
      if (!response.ok) {
        throw new Error("Failed to create event");
      }
  
      const data = await response.json();
      return data; // Return the created event data
    } catch (err) {
      console.error("Error during event creation:", err);
      throw err;
    }
  }

  // Update an existing event
async function updateEvent(eventId, eventData) {
    try {
        const mappedData = {
            ...eventData,
            event_date: eventData.date,
            description: '',
        };
      const response = await fetch(`${API_BASE_URL}/events/${eventId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "69420"
        },
        body: JSON.stringify(mappedData),
      });
  
      if (!response.ok) {
        throw new Error("Failed to update event");
      }
  
      const data = await response.json();
      return data; // Return the updated event data
    } catch (err) {
      console.error("Error during event update:", err);
      throw err;
    }
  }
  //delete event
async function deleteEvent(eventId) {
    try {
      const response = await fetch(`${API_BASE_URL}/events/${eventId}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "69420"
        },
      });
  
      if (!response.ok) {
        throw new Error("Failed to delete event");
      }
  
      return true; // Return true if the event was deleted successfully
    } catch (err) {
      console.error("Error during event deletion:", err);
      throw err;
    }
  }

export { fetchEvents, createEvent, updateEvent, deleteEvent };