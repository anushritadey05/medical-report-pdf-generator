# Medical Report PDF Generator

A full-stack web application for generating professional medical laboratory reports in PDF format.

## Features

- ✨ Patient Management (CRUD operations)
- 📊 Lab Results Upload (CSV/Excel)
- 🤖 AI-Powered Report Summarization (Optional)
- 📄 Professional PDF Report Generation
- 🎨 Beautiful, Modern UI with Animations
- 📱 Fully Responsive Design

## Tech Stack

### Backend
- Flask (Python Web Framework)
- SQLAlchemy (Database ORM)
- ReportLab (PDF Generation)
- Pandas (Data Processing)
- OpenAI API (Optional - for AI summarization)

### Frontend
- React 18
- Framer Motion (Animations)
- Axios (HTTP Client)
- React Router (Routing)
- React Toastify (Notifications)

## Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## Installation

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the backend server
python app.py
```

Backend will run on `http://localhost:5000`

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will run on `http://localhost:3000`

## Sample Lab Results CSV Format

Create a CSV file with the following columns:

```csv
Test Name,Value,Unit,Reference Range,Status
Hemoglobin,14.5,g/dL,13.5-17.5,Normal
White Blood Cells,7.2,10^3/µL,4.5-11.0,Normal
Platelets,250,10^3/µL,150-400,Normal
Glucose,110,mg/dL,70-100,High
Cholesterol,180,mg/dL,<200,Normal
```

## Optional: AI Summarization Setup

1. Get an OpenAI API key from https://platform.openai.com/
2. Create a `.env` file in the `backend` folder:

```env
OPENAI_API_KEY=your-api-key-here
SECRET_KEY=your-secret-key-here
```

## Usage

1. **Add Patients**:  Go to Dashboard and click "Add New Patient"
2. **Upload Lab Results**: Navigate to "Generate Report" and select a patient
3. **Upload CSV/Excel**: Drag and drop or browse for your lab results file
4. **Generate Report**: Review the parsed data and click "Generate PDF Report"
5. **Download**:  Download your professionally formatted PDF report

## Project Structure

```
medical-report-pdf-generator/
├── backend/
│   ├── app. py
│   ├── config.py
│   ├── models/
│   ├── routes/
│   └── utils/
└── frontend/
    └── src/
        ├── api/
        ├── components/
        ├── pages/
        └── styles/
```

## License

MIT License

## Author

Created with ❤️ by anushritadey05
```