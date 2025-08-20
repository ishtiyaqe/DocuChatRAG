import React, { useState } from "react";
import axios from "axios";

function DocumentUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/api/upload/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      onUploadSuccess(response.data.doc_id);
    } catch (error) {
      console.error(error);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white shadow-lg rounded-2xl p-6 w-96">
      <h2 className="text-xl font-semibold mb-4">Upload Document</h2>
      <input type="file" onChange={handleFileChange} className="mb-4" />
      <button
        onClick={handleUpload}
        disabled={loading}
        className="bg-indigo-600 text-white px-4 py-2 rounded-xl hover:bg-indigo-700 disabled:bg-gray-400"
      >
        {loading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
}

export default DocumentUpload;
