import './App.css';
import EconTable from './components/EconTable'
import { useEffect } from 'react';
import { useState } from 'react';
import NonEconTable from './components/NonEconTable';


function App() {

  const [selectedOption, setSelectedOption] = useState('');

  const handleOptionChange = (event) => {
    setSelectedOption(event.target.value);
  };

  return (
    
    <div className="App">
      <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css"></link>
      <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"></link>
      <script defer src="https://code.getmdl.io/1.3.0/material.min.js"></script>

      <h1>Country Reporter</h1>

      <select value={selectedOption} onChange={handleOptionChange}>
        <option value="">Select an option</option>
        <option value="option1">Option 1</option>
        <option value="option2">Option 2</option>
        <option value="option3">Option 3</option>
      </select>
      {selectedOption && <p>You selected: {selectedOption}</p>}
      
      <EconTable />
      <NonEconTable/>
    
    </div>
  );
}

export default App;
