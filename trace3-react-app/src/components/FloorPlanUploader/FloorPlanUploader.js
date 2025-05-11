// src/components/FloorPlanUploader/FloorPlanUploader.js
import React, { useState } from 'react';
import './FloorPlanUploader.css';

function FloorPlanUploader() {
  const [buildingName, setBuildingName] = useState('');
  const [floorNumber, setFloorNumber] = useState('');
  const [floorPlanFile, setFloorPlanFile] = useState(null);
  const [message, setMessage] = useState('');

const handleSubmit = (e) => {
  e.preventDefault();
  setMessage(''); // Clear previous messages

  const formData = new FormData();
  formData.append('building_name', buildingName);
  formData.append('floor_number', floorNumber);
  formData.append('file', floorPlanFile);

  fetch('http://127.0.0.1:5000/process_floor_plan', {
    method: 'POST',
    body: formData,
  })
    .then((response) => {
      console.log('Response:', response);
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      const contentType = response.headers.get('content-type');
      if (contentType && contentType.includes('application/json')) {
        return response.json();
      } else {
        return response.text();
      }
    })
    .then((data) => {
      console.log('Data:', data);
      // Check if data is a string (from response.text())
      if (typeof data === 'string') {
        setMessage(data);
      } else if (data.status === 'success') {
        setMessage(data.message || 'Floor plan uploaded successfully!');
      } else {
        throw new Error(data.message || 'Unknown error occurred');
      }
      // Reset the form
      setBuildingName('');
      setFloorNumber('');
      setFloorPlanFile(null);
      document.getElementById('floorPlanFile').value = null;
    })
    .catch((error) => {
      console.error('Error:', error);
      setMessage(`Error uploading floor plan: ${error.message}`);
    });
};


  return (
    <form className="floor-plan-uploader" onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="buildingName">Building Name:</label>
        <input
          type="text"
          id="buildingName"
          value={buildingName}
          onChange={(e) => setBuildingName(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="floorNumber">Floor Number:</label>
        <input
          type="number"
          id="floorNumber"
          value={floorNumber}
          onChange={(e) => setFloorNumber(e.target.value)}
          required
        />
      </div>
      <div className="form-group">
        <label htmlFor="floorPlanFile">Floor Plan (PDF, JPEG, PNG):</label>
        <input
          type="file"
          id="floorPlanFile"
          accept=".pdf, .jpeg, .jpg, .png"
          onChange={(e) => setFloorPlanFile(e.target.files[0])}
          required
        />
      </div>
      <button type="submit">Upload Floor Plan</button>
      {message && <p className="message">{message}</p>}
    </form>
  );
}

export default FloorPlanUploader;
