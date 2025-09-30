// src/main.jsx
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./pages/css/dashboard.css";
import Dashboard from "./pages/javascript/dashboard";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <Dashboard />
  </StrictMode>
);
