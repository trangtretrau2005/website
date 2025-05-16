import React from "react";
import { Link, useLocation } from "react-router-dom";
import "../styles/style.css";

const Sidebar = ({ routes }) => {
  const location = useLocation();

  return (
    <aside className="sidebar">
      <nav>
        {routes.map((route, index) => (
          <Link
            key={index}
            to={route.path}
            className={location.pathname === route.path ? "active" : ""}
          >
            {route.name}
          </Link>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;