import './App.css';
// import { useEffect } from 'react';
// import { useState } from 'react';
import EconTable from './components/EconTable'
import NonEconTable from './components/NonEconTable';
import CountryReportForm from './components/CountryReportForm';


function App() {

  // const [selectedOption, setSelectedOption] = useState('');

  // const handleOptionChange = (event) => {
  //   setSelectedOption(event.target.value);
  // };

  return (
    
    <div className="App">
      <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css"></link>
      <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"></link>
      <script defer src="https://code.getmdl.io/1.3.0/material.min.js"></script>

      <h1>Country Reporter</h1>
      <CountryReportForm />
      <EconTable />
      <NonEconTable/>
    
    </div>
  );
}

export default App;
