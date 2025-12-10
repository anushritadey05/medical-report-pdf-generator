import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { toast } from 'react-toastify';
import { FaClipboardList } from 'react-icons/fa';
import { getPatients, generateReport, downloadReport } from '../api/api';
import LabUpload from '../components/Labupload.js';
import ReportPreview from '../components/ReportPreview';

const ReportPage = () => {
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState('');
  const [labResults, setLabResults] = useState(null);
  const [reportData, setReportData] = useState(null);
  const [generating, setGenerating] = useState(false);
  const [step, setStep] = useState(1);

  useEffect(() => {
    fetchPatients();
  }, []);

  const fetchPatients = async () => {
    try {
      const response = await getPatients();
      setPatients(response.data.patients);
    } catch (error) {
      toast.error('Failed to load patients');
    }
  };

  const handleDataParsed = (data) => {
    setLabResults(data);
    setStep(2);
    toast.success('Lab results parsed successfully!');
  };

  const handleGenerateReport = async () => {
    if (!selectedPatient) {
      toast.error('Please select a patient');
      return;
    }

    if (! labResults) {
      toast.error('Please upload lab results first');
      return;
    }

    setGenerating(true);
    try {
      const response = await generateReport({
        patient_id: selectedPatient,
        lab_results: labResults
      });

      if (response.data.success) {
        toast.success('Report generated successfully!');
        setReportData({
          summary: response.data.summary,
          reportUrl: downloadReport(response.data.report. id)
        });
        setStep(3);
      }
    } catch (error) {
      toast.error('Failed to generate report:  ' + (error.response?.data?.error || error.message));
    } finally {
      setGenerating(false);
    }
  };

  const resetForm = () => {
    setSelectedPatient('');
    setLabResults(null);
    setReportData(null);
    setStep(1);
  };

  return (
    <div className="report-page">
      <motion.div 
        className="page-header"
        initial={{ opacity: 0, y:  -20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1><FaClipboardList /> Generate Medical Report</h1>
      </motion.div>

      {/* Progress Steps */}
      <div className="progress-steps">
        <div className={`step ${step >= 1 ? 'active' : ''}`}>
          <div className="step-number">1</div>
          <div className="step-label">Select Patient & Upload</div>
        </div>
        <div className={`step ${step >= 2 ? 'active' : ''}`}>
          <div className="step-number">2</div>
          <div className="step-label">Review & Generate</div>
        </div>
        <div className={`step ${step >= 3 ? 'active' : ''}`}>
          <div className="step-number">3</div>
          <div className="step-label">Download Report</div>
        </div>
      </div>

      <div className="report-content">
        {step === 1 && (
          <motion. div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            {/* Patient Selection */}
            <div className="patient-selection">
              <h3>Select Patient</h3>
              <select
                value={selectedPatient}
                onChange={(e) => setSelectedPatient(e.target.value)}
                className="patient-select"
              >
                <option value="">-- Choose a patient --</option>
                {patients.map(patient => (
                  <option key={patient.id} value={patient.id}>
                    {patient.name} (Age: {patient.age}, {patient.gender})
                  </option>
                ))}
              </select>
            </div>

            {/* Lab Upload */}
            {selectedPatient && (
              <LabUpload onDataParsed={handleDataParsed} />
            )}
          </motion.div>
        )}

        {step === 2 && labResults && (
          <motion. div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <ReportPreview labResults={labResults} />
            <div className="action-buttons">
              <motion.button 
                className="btn btn-outline"
                onClick={resetForm}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Start Over
              </motion.button>
              <motion.button 
                className="btn btn-success"
                onClick={handleGenerateReport}
                disabled={generating}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {generating ? 'Generating PDF...' : 'Generate PDF Report'}
              </motion.button>
            </div>
          </motion.div>
        )}

        {step === 3 && reportData && (
          <motion. div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
          >
            <ReportPreview 
              labResults={labResults}
              summary={reportData.summary}
              reportUrl={reportData.reportUrl}
            />
            <div className="action-buttons">
              <motion.button 
                className="btn btn-primary"
                onClick={resetForm}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                Generate Another Report
              </motion.button>
            </div>
          </motion. div>
        )}
      </div>
    </div>
  );
};

export default ReportPage;