import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";

const rootElement = document.getElementById("root");
const root = ReactDOM.createRoot(rootElement);

const App = () => {
  return <div>Hello React</div>;
};

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
