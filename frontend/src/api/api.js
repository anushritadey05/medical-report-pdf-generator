import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Patient API calls
export const getPatients = () => api.get('/patients');
export const getPatient = (id) => api.get(`/patients/${id}`);
export const createPatient = (data) => api.post('/patients', data);
export const updatePatient = (id, data) => api.put(`/patients/${id}`, data);
export const deletePatient = (id) => api.delete(`/patients/${id}`);

// Report API calls
export const uploadLabResults = (file) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/upload-lab-results', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
};

export const generateReport = (data) => api.post('/generate-report', data);
export const getPatientReports = (patientId) => api.get(`/reports/${patientId}`);
export const downloadReport = (reportId) => {
  return `${API_BASE_URL}/reports/download/${reportId}`;
};

export default api;