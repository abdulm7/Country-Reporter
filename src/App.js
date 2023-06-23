import './App.css';
import EconTable from './components/EconTable'
import { useEffect } from 'react';
import { useState } from 'react';
import NonEconTable from './components/NonEconTable';


function App() {


  return (
    
    <div className="App">
      <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css"></link>
      <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons"></link>
      <script defer src="https://code.getmdl.io/1.3.0/material.min.js"></script>

      <h1>Country Reporter</h1>
      
      <EconTable />
      <NonEconTable/>
    
    </div>
  );
}

export default App;
