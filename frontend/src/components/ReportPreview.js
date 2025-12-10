import React from 'react';
import { motion } from 'framer-motion';
import { FaDownload, FaCheckCircle, FaExclamationTriangle } from 'react-icons/fa';

const ReportPreview = ({ labResults, summary, reportUrl }) => {
  return (
    <motion.div 
      className="report-preview"
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity:  1, scale: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className="preview-header">
        <h2>Lab Results Preview</h2>
      </div>

      {labResults && labResults.length > 0 && (
        <div className="results-table-container">
          <table className="results-table">
            <thead>
              <tr>
                <th>Test Name</th>
                <th>Value</th>
                <th>Unit</th>
                <th>Reference Range</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {labResults.map((result, index) => (
                <motion.tr 
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className={result.status?.toLowerCase() !== 'normal' ? 'abnormal-row' : ''}
                >
                  <td>{result.test_name}</td>
                  <td>{result.value}</td>
                  <td>{result.unit}</td>
                  <td>{result.reference_range}</td>
                  <td>
                    <span className={`status-badge ${result.status?.toLowerCase()}`}>
                      {result.status?.toLowerCase() === 'normal' ? (
                        <><FaCheckCircle /> {result.status}</>
                      ) : (
                        <><FaExclamationTriangle /> {result.status}</>
                      )}
                    </span>
                  </td>
                </motion. tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {summary && (
        <motion.div 
          className="summary-section"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay:  0.3 }}
        >
          <h3>Clinical Summary</h3>
          <div className="summary-content">
            {summary.split('\n').map((line, index) => (
              <p key={index}>{line}</p>
            ))}
          </div>
        </motion.div>
      )}

      {reportUrl && (
        <motion.div 
          className="download-section"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
        >
          <a 
            href={reportUrl} 
            className="btn btn-success"
            download
          >
            <FaDownload /> Download PDF Report
          </a>
        </motion.div>
      )}
    </motion.div>
  );
};

export default ReportPreview;