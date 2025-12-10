import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { FaPlus, FaEdit, FaTrash, FaFileAlt } from 'react-icons/fa';
import { toast } from 'react-toastify';
import { getPatients, createPatient, deletePatient } from '../api/api';
import PatientForm from '../components/PatientForm';

const Dashboard = () => {
  const [patients, setPatients] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    try {
      const response = await getPatients();
      setPatients(response.data.patients);
    } catch (error) {
      toast.error('Failed to load patients');
    } finally {
      setLoading(false);
    }
  };

  const handleCreatePatient = async (formData) => {
    try {
      await createPatient(formData);
      toast.success('Patient added successfully! ');
      setShowForm(false);
      fetchPatients();
    } catch (error) {
      toast.error('Failed to create patient');
    }
  };

  const handleDeletePatient = async (id) => {
    if (window.confirm('Are you sure you want to delete this patient?')) {
      try {
        await deletePatient(id);
        toast.success('Patient deleted successfully! ');
        fetchPatients();
      } catch (error) {
        toast.error('Failed to delete patient');
      }
    }
  };

  return (
    <div className="dashboard-page">
      <motion.div 
        className="page-header"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity:  1, y: 0 }}
      >
        <h1>Patient Dashboard</h1>
        <motion.button 
          className="btn btn-primary"
          onClick={() => setShowForm(! showForm)}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <FaPlus /> Add New Patient
        </motion.button>
      </motion.div>

      {showForm && (
        <motion.div 
          className="form-container"
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height:  'auto' }}
          exit={{ opacity: 0, height:  0 }}
        >
          <PatientForm onSubmit={handleCreatePatient} />
        </motion.div>
      )}

      <div className="patients-grid">
        {loading ?  (
          <div className="loading">Loading patients...</div>
        ) : patients.length === 0 ? (
          <div className="empty-state">
            <p>No patients found.  Add your first patient to get started!</p>
          </div>
        ) : (
          patients.map((patient, index) => (
            <motion.div 
              key={patient.id}
              className="patient-card"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity:  1, y: 0 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ y: -5, boxShadow: '0 10px 30px rgba(0,0,0,0.15)' }}
            >
              <div className="patient-header">
                <h3>{patient.name}</h3>
                <span className="patient-id">#{patient.id}</span>
              </div>
              <div className="patient-info">
                <p><strong>Age:</strong> {patient.age} years</p>
                <p><strong>Gender:</strong> {patient.gender}</p>
                <p><strong>Phone:</strong> {patient.phone || 'N/A'}</p>
                <p><strong>Email:</strong> {patient.email || 'N/A'}</p>
              </div>
              <div className="patient-actions">
                <motion.button 
                  className="btn btn-icon btn-primary"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  title="View Reports"
                >
                  <FaFileAlt />
                </motion.button>
                <motion.button 
                  className="btn btn-icon btn-secondary"
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  title="Edit Patient"
                >
                  <FaEdit />
                </motion.button>
                <motion.button 
                  className="btn btn-icon btn-danger"
                  onClick={() => handleDeletePatient(patient.id)}
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  title="Delete Patient"
                >
                  <FaTrash />
                </motion.button>
              </div>
            </motion. div>
          ))
        )}
      </div>
    </div>
  );
};

export default Dashboard;