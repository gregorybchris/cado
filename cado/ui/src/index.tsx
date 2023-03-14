import "@fontsource/sen/400.css";
import "@fontsource/sen/700.css";
import "@fontsource/sen/800.css";
import "./index.css";

import App from "./components/App";
import React from "react";
import ReactDOM from "react-dom/client";

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
