import React, { useState } from "react";
import clients from "../api/clients";

function DocumentUpload({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await clients.post("api/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",// Add JWT token
        },
        withCredentials: true,
      });
      onUploadSuccess(response.data.id); // pass the document id
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white p-6 shadow-lg rounded w-96">
      <h2 className="text-xl font-semibold mb-4">Upload Document</h2>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button
        onClick={handleUpload}
        disabled={loading}
        className="bg-indigo-600 text-white px-4 py-2 mt-4 rounded"
      >
        {loading ? "Uploading..." : "Upload"}
      </button>
    </div>
  );
}

export default DocumentUpload;
