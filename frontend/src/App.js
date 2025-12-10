import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import { FaHospital, FaHome, FaFileAlt } from 'react-icons/fa';

import Dashboard from './pages/Dashboard';
import ReportPage from './pages/ReportPage';
import './styles/App.css';

function App() {
  const [activePage, setActivePage] = useState('dashboard');

  return (
    <Router>
      <div className="App">
        <ToastContainer 
          position="top-right"
          autoClose={3000}
          hideProgressBar={false}
          newestOnTop
          closeOnClick
          rtl={false}
          pauseOnFocusLoss
          draggable
          pauseOnHover
          theme="light"
        />
        
        {/* Header */}
        <motion.header 
          className="app-header"
          initial={{ y: -100 }}
          animate={{ y:  0 }}
          transition={{ type: 'spring', stiffness: 100 }}
        >
          <div className="header-content">
            <div className="logo">
              <FaHospital className="logo-icon" />
              <h1>MediReport</h1>
            </div>
            <nav className="nav-menu">
              <Link 
                to="/" 
                className={activePage === 'dashboard' ? 'nav-link active' : 'nav-link'}
                onClick={() => setActivePage('dashboard')}
              >
                <FaHome /> Dashboard
              </Link>
              <Link 
                to="/report" 
                className={activePage === 'report' ? 'nav-link active' : 'nav-link'}
                onClick={() => setActivePage('report')}
              >
                <FaFileAlt /> Generate Report
              </Link>
            </nav>
          </div>
        </motion.header>

        {/* Main Content */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/report" element={<ReportPage />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="app-footer">
          <p>&copy; 2025 MediReport. All rights reserved.</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;