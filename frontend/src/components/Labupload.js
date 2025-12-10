import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { FaUpload, FaFileCsv, FaFileExcel, FaCheckCircle } from 'react-icons/fa';
import { uploadLabResults } from '../api/api';
import { toast } from 'react-toastify';

const LabUpload = ({ onDataParsed }) => {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      toast.error('Please select a file first');
      return;
    }

    setUploading(true);
    try {
      const response = await uploadLabResults(file);
      if (response.data.success) {
        toast.success('Lab results uploaded successfully!');
        onDataParsed(response.data.data);
      }
    } catch (error) {
      toast.error('Failed to upload file: ' + (error.response?.data?.error || error.message));
    } finally {
      setUploading(false);
    }
  };

  return (
    <motion. div 
      className="lab-upload"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div 
        className={`upload-area ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        {! file ? (
          <>
            <FaUpload className="upload-icon" />
            <h3>Drag & Drop Lab Results File</h3>
            <p>or</p>
            <label className="file-input-label">
              <input
                type="file"
                accept=".csv,.xlsx,.xls"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
              <motion.span 
                className="btn btn-secondary"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Browse Files
              </motion.span>
            </label>
            <div className="supported-formats">
              <FaFileCsv /> <FaFileExcel /> CSV or Excel files
            </div>
          </>
        ) : (
          <div className="file-selected">
            <FaCheckCircle className="success-icon" />
            <p><strong>Selected:</strong> {file.name}</p>
            <div className="file-actions">
              <motion.button 
                className="btn btn-primary"
                onClick={handleUpload}
                disabled={uploading}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale:  0.95 }}
              >
                {uploading ? 'Uploading...' : 'Upload & Parse'}
              </motion.button>
              <motion.button 
                className="btn btn-outline"
                onClick={() => setFile(null)}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Change File
              </motion.button>
            </div>
          </div>
        )}
      </div>

      <div className="upload-instructions">
        <h4>File Format Instructions:</h4>
        <ul>
          <li>File should contain columns: Test Name, Value, Unit, Reference Range, Status</li>
          <li>Supported formats: CSV (. csv) or Excel (.xlsx, .xls)</li>
          <li>Maximum file size: 16MB</li>
        </ul>
      </div>
    </motion.div>
  );
};

export default LabUpload;