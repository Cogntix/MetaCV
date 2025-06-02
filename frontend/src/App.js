import React, { useState } from "react";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import UploadPage from "./Pages/UploadPage";
import QAFormPage from "./Pages/QAForm";

function App() {
  const [currentPage, setCurrentPage] = useState("upload");
  const [qaData, setQaData] = useState(null);

  const handleUploadComplete = (extractedData) => {
    setQaData(extractedData);
    setCurrentPage("qa");
  };

  const handleBackToUpload = () => {
    setCurrentPage("upload");
    setQaData(null);
  };

  return (
    <div>
      {currentPage === "upload" ? (
        <UploadPage onUploadComplete={handleUploadComplete} />
      ) : (
        <QAFormPage qaData={qaData} onBackToUpload={handleBackToUpload} />
      )}

      <ToastContainer position="top-right" autoClose={3000} theme="dark" />
    </div>
  );
}

export default App;
