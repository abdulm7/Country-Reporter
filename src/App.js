// Abdul Mahmoud
// Country Reporter Web Application
// AWS Cloud Native Application with React Front-end
// Version 1.0, July 3, 2023
// Testing Automation

import './App.css';
import EconTable from './components/EconTable'
import NonEconTable from './components/NonEconTable';
import ReportTables from './components/ReportTables';


function App() {

  return (
    
    <div className="App">
      <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css"></link>
      <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"></link>
      <script defer src="https://code.getmdl.io/1.3.0/material.min.js"></script>

      <h1>Country Reporter V1.4</h1>

      <ReportTables/>
      <EconTable />
      <NonEconTable/>
      <br/>
    
    </div>
  );
}

export default App;
