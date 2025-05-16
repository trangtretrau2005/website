import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Staff from "./pages/Staff";
import Event from "./pages/Event";
import Guest from "./pages/Guest";
import GuestResponse from "./pages/GuestResponse";

import EventListPage from "./pages/Event";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/events" element={<Event />} />
        <Route path="/events/:eventId/staffs" element={<Staff />} />
        <Route path="/events/:eventId/guests" element={<Guest />} />
        <Route path="/respond" element={<GuestResponse />} />
      </Routes>
    </Router>
  );
}

export default App;